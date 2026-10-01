#!/usr/bin/env python3
"""TTS Beta FL — realistic, emotional open-source episode renderer.

Engines
-------
Primary : VoxCPM (OpenBMB) — tokenizer-free, context-aware TTS.
          Default checkpoint: openbmb/VoxCPM-0.5B (16 kHz, CPU-friendly).
          Pass --model-id openbmb/VoxCPM2 for the 48 kHz flagship.
Fallback: Kokoro-82M (hexgrad, Apache-2.0) — only needs the espeak-ng binary.

Emotion & style
---------------
* cfg_value jitter per sentence (base --cfg, ±0.15) → natural prosody variance.
* Optional zero-shot voice/style cloning: --reference-wav my_voice.wav
  (a 5-20 s expressive sample works best) + optional --reference-text.
* Expressive punctuation in the script (dashes, questions, exclamations)
  drives emphasis and pacing.

Output: WAV + MP3 + a small .meta.json with duration and generation stats.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import traceback
import zlib
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import soundfile as sf


# --------------------------------------------------------------------------- helpers

def log(msg: str) -> None:
    print(f"[tts-beta-fl] {msg}", flush=True)


def read_paragraphs(path: Path) -> list[str]:
    """Read the episode file; lines starting with '#' are comments and skipped."""
    raw = path.read_text(encoding="utf-8")
    lines = [ln for ln in raw.splitlines() if not ln.strip().startswith("#")]
    text = "\n".join(lines).strip()
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    if not paragraphs:
        raise SystemExit(f"No speakable content found in {path}")
    return paragraphs


def sentence_chunks(paragraph: str, max_chars: int = 220) -> list[str]:
    """Split a paragraph into TTS-sized chunks (<= max_chars) on sentence bounds."""
    sentences = [s.strip() for s in re.split(r"(?<=[.!?…])\s+", paragraph) if s.strip()]
    chunks: list[str] = []
    buf = ""
    for s in sentences:
        if buf and len(buf) + len(s) + 1 > max_chars:
            chunks.append(buf)
            buf = s
        else:
            buf = f"{buf} {s}".strip()
    if buf:
        chunks.append(buf)
    return chunks


def silence(seconds: float, sr: int) -> np.ndarray:
    return np.zeros(int(seconds * sr), dtype=np.float32)


def fade(audio: np.ndarray, sr: int, ms: float = 6.0) -> np.ndarray:
    """Tiny cosine fade in/out — removes clicks at chunk boundaries."""
    n = min(len(audio), int(sr * ms / 1000))
    if n <= 1:
        return audio
    ramp = 0.5 * (1.0 - np.cos(np.linspace(0.0, np.pi, n, dtype=np.float32)))
    out = audio.copy()
    out[:n] *= ramp
    out[-n:] *= ramp[::-1]
    return out


# --------------------------------------------------------------------------- engines

def synth_voxcpm(args: argparse.Namespace, paragraphs: list[str], out_wav: Path) -> tuple[float, int]:
    import torch
    from voxcpm import VoxCPM

    device = "cuda" if torch.cuda.is_available() else "cpu"
    log(f"loading {args.model_id} (first run downloads the checkpoint from Hugging Face)…")
    t0 = time.time()
    model = VoxCPM.from_pretrained(
        hf_model_id=args.model_id,
        load_denoiser=False,   # skip the ModelScope denoiser download (not needed for synthesis)
        optimize=False,        # no torch.compile (slow warm-up; device autodetect already gives GPU speed)
        device=device,
    )
    if device == "cuda":
        log(f"GPU detected: {torch.cuda.get_device_name(0)}")
    sr = int(getattr(model.tts_model, "sample_rate", 16000))
    log(f"model ready in {time.time() - t0:.1f}s · sample_rate={sr} Hz")

    ref_path = Path(args.reference_wav).resolve() if args.reference_wav else None
    if ref_path and not ref_path.exists():
        raise SystemExit(f"--reference-wav not found: {ref_path}")
    if ref_path:
        log(f"voice/style cloning enabled via reference: {ref_path.name}")
        args.anchor_used = False

    # ---- voice anchor: lock ONE narrator voice and clone it for every chunk.
    # Without an anchor, each zero-voice chunk invents its own timbre -> the
    # "inconsistent voice" effect. The anchor fixes identity across the episode.
    anchor_path = None
    if ref_path is None and getattr(args, "anchor", True):
        anchor_text = sentence_chunks(paragraphs[0])[0]
        log(f"locking narrator voice with anchor line: \u201c{anchor_text[:60]}\u2026\u201d")
        awav = model.generate(
            text=anchor_text,
            prompt_wav_path=None,
            prompt_text=None,
            cfg_value=float(args.cfg),
            inference_timesteps=int(args.timesteps),
            max_len=4096,
            normalize=bool(args.normalize),
            retry_badcase=True,
        )
        awav = np.clip(np.asarray(awav, dtype=np.float32).reshape(-1), -1.0, 1.0)
        anchor_path = os.path.join(tempfile.gettempdir(), f"ttsfl_anchor_{os.getpid()}.wav")
        sf.write(anchor_path, fade(awav, sr), sr, subtype="PCM_16")
        args.anchor_used = True
        log("anchor voice saved — every chunk now clones this narrator")

    n_total = sum(len(sentence_chunks(p)) for p in paragraphs)
    pieces: list[np.ndarray] = []
    t_start = time.time()
    done = 0

    for pi, par in enumerate(paragraphs, 1):
        for ci, chunk in enumerate(sentence_chunks(par), 1):
            done += 1
            cfg = args.cfg + ((zlib.crc32(chunk.encode("utf-8")) % 7) - 3) * 0.05
            remaining = (time.time() - t_start) / done * (n_total - done)
            log(f"  chunk {done}/{n_total} · cfg={cfg:.2f} · ETA≈{remaining / 60:.1f} min · “{chunk[:46]}…”")
            wav = model.generate(
                text=chunk,
                prompt_wav_path=None,
                prompt_text=None,
                reference_wav_path=str(ref_path) if ref_path else anchor_path,
                cfg_value=float(cfg),
                inference_timesteps=int(args.timesteps),
                max_len=4096,
                normalize=bool(args.normalize),
                retry_badcase=True,
            )
            wav = np.asarray(wav, dtype=np.float32).reshape(-1)
            pieces.append(fade(wav, sr))
            pieces.append(silence(args.pause_sentence, sr))
        pieces.append(silence(args.pause_paragraph, sr))

    audio = np.concatenate(pieces).astype(np.float32)
    np.clip(audio, -1.0, 1.0, out=audio)
    sf.write(out_wav, audio, sr, subtype="PCM_16")
    return len(audio) / sr, sr


def synth_kokoro(args: argparse.Namespace, paragraphs: list[str], out_wav: Path) -> tuple[float, int]:
    from kokoro import KPipeline

    sr = 24000
    log("loading Kokoro-82M fallback engine…")
    pipe = KPipeline(lang_code="a")  # 'a' = American English
    pieces: list[np.ndarray] = []

    for pi, par in enumerate(paragraphs, 1):
        for chunk in sentence_chunks(par, max_chars=280):
            log(f"  [{pi}/{len(paragraphs)}] “{chunk[:46]}…”")
            try:
                gen = pipe(chunk, voice=args.voice, speed=float(args.speed))
            except TypeError:  # older kokoro without speed kwarg
                gen = pipe(chunk, voice=args.voice)
            for result in gen:
                audio = getattr(result, "audio", None)
                if audio is None:
                    continue
                if hasattr(audio, "detach"):
                    audio = audio.detach().cpu().numpy()
                pieces.append(fade(np.asarray(audio, dtype=np.float32).reshape(-1), sr))
                pieces.append(silence(args.pause_sentence, sr))
        pieces.append(silence(args.pause_paragraph, sr))

    audio = np.concatenate(pieces).astype(np.float32)
    np.clip(audio, -1.0, 1.0, out=audio)
    sf.write(out_wav, audio, sr, subtype="PCM_16")
    return len(audio) / sr, sr


# --------------------------------------------------------------------------- packaging

def to_mp3(wav: Path, mp3: Path, af_filter: str | None = None) -> None:
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(wav)]
    if af_filter:
        cmd += ["-af", af_filter]
    cmd += ["-codec:a", "libmp3lame", "-qscale:a", "3", str(mp3)]
    subprocess.run(cmd, check=True)


def main() -> None:
    ap = argparse.ArgumentParser(description="TTS Beta FL episode renderer")
    ap.add_argument("--episode", required=True, help="path to the episode .txt script")
    ap.add_argument("--outdir", default="output")
    ap.add_argument("--engine", default="voxcpm", choices=["voxcpm", "kokoro", "auto"],
                    help="voxcpm = primary (kokoro auto-fallback) · kokoro = force fallback · auto = try voxcpm then kokoro")
    ap.add_argument("--model-id", default="openbmb/VoxCPM-0.5B",
                    help="VoxCPM checkpoint: openbmb/VoxCPM-0.5B (fast) or openbmb/VoxCPM2 (48 kHz flagship)")
    ap.add_argument("--timesteps", default=8, type=int, help="VoxCPM inference timesteps (4 fast → 10 quality)")
    ap.add_argument("--cfg", default=2.0, type=float, help="VoxCPM guidance scale (1.5–3.0)")
    ap.add_argument("--normalize", dest="normalize", action="store_true", default=True,
                    help="use VoxCPM text normalization (default: on)")
    ap.add_argument("--no-normalize", dest="normalize", action="store_false")
    ap.add_argument("--reference-wav", default=None,
                    help="optional 5-20 s voice/style sample for zero-shot cloning")
    ap.add_argument("--anchor", dest="anchor", action="store_true", default=True,
                    help="lock one narrator voice and clone it for every chunk (default: on)")
    ap.add_argument("--no-anchor", dest="anchor", action="store_false")
    ap.add_argument("--mp3-filter", default="highpass=f=60,loudnorm=I=-16:TP=-1.5:LRA=11",
                    help="ffmpeg -af chain applied when exporting MP3 (empty string disables)")
    ap.add_argument("--voice", default="af_heart", help="Kokoro voice id (fallback engine)")
    ap.add_argument("--speed", default=1.0, type=float, help="Kokoro speed (fallback engine)")
    ap.add_argument("--pause-sentence", default=0.18, type=float)
    ap.add_argument("--pause-paragraph", default=0.55, type=float)
    args = ap.parse_args()

    episode_path = Path(args.episode)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    stem = episode_path.stem

    paragraphs = read_paragraphs(episode_path)
    words = sum(len(p.split()) for p in paragraphs)
    log(f"episode: {episode_path} · paragraphs={len(paragraphs)} · words={words} · "
        f"est ≈{words / 150:.1f} min @150 wpm")

    engines = ["voxcpm", "kokoro"] if args.engine == "auto" else [args.engine]
    if args.engine == "voxcpm":
        engines.append("kokoro")  # automatic safety net
    engines = list(dict.fromkeys(engines))

    meta: dict = {
        "episode": str(episode_path),
        "words": words,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    duration, sr = 0.0, 0
    for engine in engines:
        out_wav = outdir / f"{stem}.wav"
        try:
            log(f"=== engine: {engine} ===")
            if engine == "voxcpm":
                duration, sr = synth_voxcpm(args, paragraphs, out_wav)
                meta.update(engine=engine, model_id=args.model_id,
                            inference_timesteps=args.timesteps, cfg=args.cfg,
                            reference_wav=args.reference_wav or None,
                            anchor_voice=bool(getattr(args, "anchor_used", False)))
            else:
                duration, sr = synth_kokoro(args, paragraphs, out_wav)
                meta.update(engine=engine, model_id="hexgrad/Kokoro-82M",
                            voice=args.voice, speed=args.speed)
            meta.update(sample_rate=sr, duration_sec=round(duration, 1),
                        duration_min=round(duration / 60, 2))
            break
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            log(f"engine '{engine}' failed:\n{traceback.format_exc()}")
            if engine == engines[-1]:
                sys.exit(1)
            log("falling back to the next engine…")

    out_mp3 = outdir / f"{stem}.mp3"
    try:
        to_mp3(out_wav, out_mp3, args.mp3_filter or None)
        meta["files"] = [out_wav.name, out_mp3.name]
    except Exception as exc:
        log(f"ffmpeg mp3 conversion skipped ({exc}); keeping WAV only")
        meta["files"] = [out_wav.name]

    meta_path = outdir / f"{stem}.meta.json"
    meta_path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

    log(f"DONE · duration {duration / 60:.2f} min ({duration:.1f}s) · sr={sr} Hz")
    log(f"files: {out_wav} · {out_mp3} · {meta_path}")


if __name__ == "__main__":
    main()
