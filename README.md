# 🎙️ TTS Beta FL

> Realistic, emotional, open-source text-to-speech — rendered entirely on **free GitHub compute**.

![engine](https://img.shields.io/badge/engine-VoxCPM--0.5B-8A2BE2)
![fallback](https://img.shields.io/badge/fallback-Kokoro--82M-00B4D8)
![compute](https://img.shields.io/badge/compute-GitHub_Actions_%2B_Codespaces-181717)
![license](https://img.shields.io/badge/license-MIT-green)

**TTS Beta FL** turns a plain-text episode script into a fully narrated audio file using
[VoxCPM](https://github.com/OpenBMB/VoxCPM) — OpenBMB's tokenizer-free, context-aware TTS —
with **zero paid infrastructure**. A GitHub Actions workflow does the synthesis, commits the
finished audio back to this repo, and uploads it as a downloadable artifact. The exact same
pipeline runs one-command inside GitHub Codespaces.

```
 episode .txt ──►  VoxCPM-0.5B (tokenizer-free TTS)  ──►  WAV ──►  MP3 ──┬──► committed to output/
 (script w/ emotion)     sentence chunks · cfg jitter                    ├──► Actions artifact
                         paragraph pauses · 16 kHz                       └──► downloadable in 1 click
```

## 📻 Episode 01 — *The Retina: The Camera That Thinks*

The first fully-on-GitHub production: a **~10 minute** narrated deep-dive into the human
retina — brain tissue hanging outside your skull, the backwards wiring of the eye, rods and
cones, the blind-spot illusion, retinal computing, melanopsin and your body clock, and
bionic retinas.

Generated files (produced by the Actions run):

| File | Purpose |
|------|---------|
| `output/retina.mp3` | The episode — ready for any player |
| `output/retina.wav` | Lossless master (16 kHz PCM) |
| `output/retina.meta.json` | Generation stats: engine, duration, params |

## 🚀 Run it on GitHub Actions (no computer involved)

1. Open the **Actions** tab → **Generate Episode (TTS)**.
2. Click **Run workflow**, optionally tweak the inputs:

| Input | Default | Notes |
|-------|---------|-------|
| `episode_file` | `scripts/episodes/retina.txt` | any `.txt` under `scripts/episodes/` |
| `engine` | `voxcpm` | `kokoro` = fast fallback · `auto` = try both |
| `model_id` | `openbmb/VoxCPM-0.5B` | swap to `openbmb/VoxCPM2` for 48 kHz flagship quality |
| `inference_timesteps` | `8` | 4 = fast draft, 10 = max quality |
| `cfg_value` | `2.0` | guidance scale — higher clings harder to the text |
| `kokoro_voice` | `af_heart` | fallback voice id |

3. Wait ~20–45 min (CPU synthesis of a 10-minute episode + model download).
4. Grab the audio from the run's **Artifacts** or straight from `output/` in the repo.

The Hugging Face model cache is persisted with `actions/cache`, so re-runs are much faster.

## 🔓 The Codespaces loophole (free 4-core compute)

GitHub gives personal accounts **120 core-hours/month free**. This repo ships a devcontainer,
so you can render episodes on Microsoft's dime instead of your laptop:

1. On the repo home, press **`.`** (or **Code → Codespaces → Create codespace**).
2. The devcontainer auto-installs Python 3.11, torch (CPU), espeak-ng, ffmpeg and all deps.
3. In the terminal:

   ```bash
   bash scripts/run_codespace.sh                      # default: retina episode
   TTS_MODEL_ID=openbmb/VoxCPM2 bash scripts/run_codespace.sh   # 48 kHz flagship
   ```

4. When it finishes, commit the audio back:

   ```bash
   git add output/ && git commit -m "feat(audio): episode rendered in Codespaces" && git push
   ```

A 4-core codespace typically renders a 10-minute episode in ~15–30 min ≈ **1–2 core-hours**
of your free allowance. ~60 episodes per month, free.

## 😡🎭 Emotion & voice control

VoxCPM conveys emotion through the text itself (punctuation, dashes, questions) and through
**zero-shot voice/style cloning**. To narrate with any voice you like:

1. Drop a **5–20 second expressive sample** into the repo, e.g. `scripts/prompts/narrator.wav`
2. Render with cloning:

   ```bash
   python scripts/generate_tts.py --episode scripts/episodes/retina.txt \
       --reference-wav scripts/prompts/narrator.wav --outdir output
   ```

The model transfers the timbre *and the emotional colouring* of the reference clip. Also
built in: per-sentence guidance jitter (cfg ±0.15) so long narrations never sound metronomic.

## 🧠 Engines

| Engine | Model | Params | SR | License | Role |
|--------|-------|--------|----|---------|------|
| [VoxCPM](https://github.com/OpenBMB/VoxCPM) | `openbmb/VoxCPM-0.5B` | 0.5 B | 16 kHz | Apache-2.0 | primary — context-aware, tokenizer-free, cloneable |
| [VoxCPM2](https://huggingface.co/openbmb/VoxCPM2) | `openbmb/VoxCPM2` | ~1.5 B | 48 kHz | Apache-2.0 | flagship option (`--model-id`) |
| [Kokoro](https://huggingface.co/hexgrad/Kokoro-82M) | Kokoro-82M | 82 M | 24 kHz | Apache-2.0 | automatic fallback if VoxCPM hiccups |

## 💻 Local run (optional)

```bash
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
sudo apt install espeak-ng ffmpeg   # kokoro fallback + mp3
python scripts/generate_tts.py --episode scripts/episodes/retina.txt --outdir output
```

## 📁 Repo layout

```
├── .github/workflows/generate.yml   # the whole factory: install → synthesize → commit
├── .devcontainer/devcontainer.json  # one-click Codespaces environment (4-core)
├── scripts/
│   ├── generate_tts.py              # engine wrapper: chunking, cfg jitter, pauses, mp3, meta
│   ├── run_codespace.sh             # one-command Codespaces renderer
│   └── episodes/retina.txt          # Episode 01 script (~1,470 words ≈ 10 min)
├── output/                          # generated audio (committed by Actions / Codespaces)
├── requirements.txt
└── LICENSE
```

## 🔐 Security notes

- Never commit a personal access token to any repo. If a PAT leaks, **revoke it immediately**
  (Settings → Developer settings → Personal access tokens) and prefer fine-grained tokens or
  `gh auth login` over pasting secrets into terminals.
- This repo needs no secrets at all: Actions uses the built-in `GITHUB_TOKEN`
  (`permissions: contents: write`) to commit audio back.

## 📄 Licenses

Code: MIT. Model weights: VoxCPM / VoxCPM2 / Kokoro — Apache-2.0 (see table above).
