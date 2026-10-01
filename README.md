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

## 📻 Episodes

| # | Title | Script | Audio | Rendered on |
|---|-------|--------|-------|-------------|
| 01 | *The Retina — The Camera That Thinks* | `scripts/episodes/retina.txt` | `output/retina.mp3` | GitHub Actions CPU (VoxCPM-0.5B) · re-rendered on Kaggle GPU (VoxCPM2) |
| 02 | *The Cochlea — The Piano Inside Your Head* | `scripts/episodes/cochlea.txt` | `output/cochlea.mp3` | Kaggle GPU (VoxCPM2) |

The `scripts/episodes/` folder is the **Script folder** — drop any `.txt` there (blank line
between paragraphs, `#` lines are comments) and it becomes a renderable episode.

## ⚡ Fast path — render on Kaggle's free GPU (10-15× faster than Actions CPU)

GitHub Actions CPU needs ~75-90 min for a 10-minute episode. Kaggle hands out **free GPU
sessions** (P100/T4, ~30 h/week), so this repo ships a pipeline where **GitHub sends the job
to Kaggle, Kaggle renders on GPU, GitHub pulls the audio back and commits it**:

1. Repo **Settings → Secrets and variables → Actions** must contain `KAGGLE_USERNAME` and
   `KAGGLE_KEY` (from kaggle.com → Settings → API → Create New Token). Already configured ✓.
   ⚠️ Kaggle requires a **phone-verified account** for GPU accelerators.
2. Actions tab → **Render Episode (Kaggle GPU)** → Run workflow.
3. The workflow pushes a private kernel that pins this repo's exact commit SHA, renders with
   **VoxCPM2 (48 kHz)** + voice anchor, then downloads the audio and commits it to `output/`.
4. Typical wall time: **~10-25 min** including queue (vs ~75-90 min on Actions CPU).

Monitor progress any time at `kaggle.com/code` — the kernel appears as `tts-fl-<episode>`.

> ⚠️ **Kaggle requirement — phone verification.** Kaggle silently denies GPU *and*
> internet to accounts without a verified phone number (kernels run CPU-only and offline).
> Verify at **kaggle.com → Settings → Phone Verification**; the GPU + internet flags of this
> workflow unlock immediately after — no code changes needed. (Diagnosed empirically:
> probe kernels with `enable_gpu/internet: true` received CPU-only, no-DNS sessions.)

## 🚀 Run it on GitHub Actions (CPU fallback — no computer involved)

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

3. Wait ~30–90 min (CPU synthesis of a 10-minute episode + model download). For the fast
   path use the **Kaggle GPU workflow** above instead.
4. Grab the audio from the run's **Artifacts** or straight from `output/` in the repo.

The Hugging Face model cache is persisted with `actions/cache`, so re-runs are much faster.

## 🔓 The Codespaces loophole (fastest path available today: 16-core)

GitHub gives personal accounts **120 core-hours/month free** — and you can pick a
**16-core machine** when creating the Codespace, which renders a 10-minute episode in
**~15-25 min** (the runner script automatically uses every core):

1. Repo home → **Code → Codespaces → Create codespace on main** → machine size dropdown →
   **16-core** (costs 16 core-hours/hour of your free allowance).
2. The devcontainer auto-installs Python 3.11, torch (CPU), espeak-ng, ffmpeg and all deps.
3. In the terminal:

   ```bash
   bash scripts/run_codespace.sh                                    # retina episode
   bash scripts/run_codespace.sh scripts/episodes/cochlea.txt       # Episode 02
   TTS_MODEL_ID=openbmb/VoxCPM2 bash scripts/run_codespace.sh       # 48 kHz flagship
   ```

4. When it finishes, commit the audio back:

   ```bash
   git add output/ && git commit -m "feat(audio): episode rendered in Codespaces" && git push
   ```

16 core-hours per hour means your free 120 core-hours buy **~7 hours of 16-core rendering
per month ≈ 15-20 episodes** — or stick to 4-core machines for ~60 slower renders.

## 😡🎭 Emotion & voice control (v2 — consistent narrator)

Three layers of control, all live in `scripts/generate_tts.py`:

1. **Voice anchor (new)** — one chunk is synthesised first, saved, and then cloned for
   *every* other chunk, so the whole episode keeps a single narrator timbre. This removes
   the chunk-to-chunk voice drift of zero-voice generation. Disable with `--no-anchor`.
2. **Zero-shot voice/style cloning** — drop a 5-20 s expressive sample into
   `scripts/prompts/` and pass `--reference-wav` (overrides the anchor; timbre *and* emotion
   transfer from the clip).
3. **Guidance jitter** — per-sentence cfg ±0.15 keeps long narrations from sounding metronomic.

Cleanup is baked in too: 6 ms cosine fades at every chunk boundary (no clicks) and an ffmpeg
chain (`highpass + loudnorm`) on the MP3 export (tune with `--mp3-filter`).

## 🧠 Engines

| Engine | Model | Params | SR | License | Role |
|--------|-------|--------|----|---------|------|
| [VoxCPM](https://github.com/OpenBMB/VoxCPM) | `openbmb/VoxCPM-0.5B` | 0.5 B | 16 kHz | Apache-2.0 | primary — context-aware, tokenizer-free, cloneable |
| [VoxCPM2](https://huggingface.co/openbmb/VoxCPM2) | `openbmb/VoxCPM2` | ~1.5 B | 48 kHz | Apache-2.0 | flagship option (`--model-id`) — cleaner, default on Kaggle GPU |
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
├── .github/workflows/generate.yml   # Actions CPU factory: install → synthesize → commit
├── .github/workflows/kaggle.yml     # Kaggle GPU factory: push kernel → wait → pull audio
├── .devcontainer/devcontainer.json  # one-click Codespaces environment (4-core)
├── scripts/
│   ├── generate_tts.py              # engines, voice anchor, chunking, fades, mp3, meta
│   ├── kaggle_render_driver.py      # pushes kernel to Kaggle, polls, downloads audio
│   ├── run_codespace.sh             # one-command Codespaces renderer
│   └── episodes/                    # 📜 the Script folder
│       ├── retina.txt               #   Episode 01 (~1,550 words ≈ 10 min)
│       └── cochlea.txt              #   Episode 02 (~1,490 words ≈ 10 min)
├── output/                          # generated audio (committed by Actions / Kaggle loop)
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
