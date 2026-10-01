# 🎙️ TTS Beta FL

> Realistic, emotional, open-source text-to-speech — rendered entirely on **free GitHub compute**.

![engine](https://img.shields.io/badge/engine-VoxCPM2_48kHz-8A2BE2)
![fallback](https://img.shields.io/badge/fallback-Kokoro--82M-00B4D8)
![compute](https://img.shields.io/badge/compute-GitHub_Actions_%E2%86%92_Kaggle_T4-181717)
![license](https://img.shields.io/badge/license-MIT-green)

**TTS Beta FL** turns a plain-text episode script into a fully narrated audio file using
[VoxCPM](https://github.com/OpenBMB/VoxCPM) — OpenBMB's tokenizer-free, context-aware TTS —
with **zero paid infrastructure**. A GitHub Actions workflow does the synthesis, commits the
finished audio back to this repo, and uploads it as a downloadable artifact. The exact same
pipeline runs one-command inside GitHub Codespaces.

```
 episode .txt ──► GitHub Actions workflow ──► Kaggle free GPU (Tesla T4)
 (script w/         estimates the time          VoxCPM2 · 48 kHz · voice anchor
  emotion)          (calibrated ETA)                │
                        ▲                          ▼
 rendered/ ◄── commit + artifact ◄── download ◄── render ~20 min
```

## 📻 Episodes

| # | Title | Script | Audio | Rendered on |
|---|-------|--------|-------|-------------|
| 01 | *The Retina — The Camera That Thinks* | `scripts/episodes/retina.txt` | `output/retina.mp3` | GitHub Actions CPU (VoxCPM-0.5B) |
| 02 | *The Cochlea — The Piano Inside Your Head* | `scripts/episodes/cochlea.txt` | `rendered/cochlea.mp3` | Kaggle T4 GPU (VoxCPM2, 48 kHz) · **21.7 min render** |

The `scripts/episodes/` folder is the **Script folder** — drop any `.txt` there (blank line
between paragraphs, `#` lines are comments) and it becomes a renderable episode.

## ⚡ Full automation — GitHub Actions → Kaggle free GPU → `rendered/`

GitHub Actions CPU needs ~75-90 min for a 10-minute episode. Kaggle hands out **free GPU
sessions** (Tesla T4, ~30 h/week), so the **Render Episode (Kaggle GPU)** workflow does the
whole loop with zero clicks after launch:

1. **Estimates the render time** before launching (estimator calibrated on real T4 runs:
   `words/26.5 chunks × 20.7 s + 2.4 min` — predicted 21.7 min, measured 21.7 min).
2. **Pushes a private kernel** pinned to this repo's exact commit SHA (GitHub → Kaggle).
3. **Polls** until the kernel finishes (Kaggle renders on GPU: VoxCPM2, 48 kHz, voice anchor,
   timesteps=10).
4. **Pulls the audio back** into `rendered/` (GitHub ← Kaggle), keeping only the
   deliverables: `<name>.wav`, `<name>.mp3`, `<name>.meta.json`, `<name>.timing.json`.
5. **Commits `rendered/` to the repo**, uploads a 30-day artifact, and posts a
   **timing report** (estimated vs actual) to the run's summary page.

To use it: **Actions tab → Render Episode (Kaggle GPU) → Run workflow** → pick the episode.
Repo **Settings → Secrets → Actions** must contain `KAGGLE_USERNAME` / `KAGGLE_KEY`
(configured ✓). Typical wall time: **~22-27 min** total (render ~20 min + queue + download).

CLI equivalent (works anywhere with `~/.kaggle/kaggle.json`):

```bash
pip install kaggle
python scripts/kaggle_render_driver.py --estimate-only --episode scripts/episodes/retina.txt
python scripts/kaggle_render_driver.py --episode scripts/episodes/retina.txt --out rendered
```

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
├── .github/workflows/generate.yml   # legacy CPU factory: install → synthesize → commit
├── .github/workflows/kaggle.yml     # ⚡ GitHub→Kaggle GPU loop: estimate → push → wait → pull → commit
├── .devcontainer/devcontainer.json  # one-click Codespaces environment (4-core)
├── scripts/
│   ├── generate_tts.py              # engines, voice anchor, chunking, fades, mp3, meta
│   ├── kaggle_render_driver.py      # ETA estimator + push/poll/pull + timing.json
│   ├── run_codespace.sh             # one-command Codespaces renderer
│   └── episodes/                    # 📜 the Script folder
│       ├── retina.txt               #   Episode 01 (~1,550 words ≈ 10 min)
│       └── cochlea.txt              #   Episode 02 (~1,490 words ≈ 10 min)
├── rendered/                        # 🎧 final GPU renders + timing reports (committed)
├── output/                          # legacy CPU renders (retina)
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
