# 🎙️ Focus Cast — Optometry Audio Library Workbench

> **Focus Cast by focuslinks.in** — an automated audio-library factory for optometry education.
> Plain-text scripts in, finished podcast episodes out — rendered on Kaggle's free GPU,
> organized, catalogued, and committed back to this repo by GitHub Actions. Hands-off.

![series](https://img.shields.io/badge/series-01_Optometry_Foundations-8A2BE2)
![episodes](https://img.shields.io/badge/episodes-100_planned_·_5_scripted-00B4D8)
![engine](https://img.shields.io/badge/engine-Kokoro_82M_·_voicepacks-FF6B6B)
![compute](https://img.shields.io/badge/compute-GitHub_Actions_%E2%86%92_Kaggle_T4-181717)
![license](https://img.shields.io/badge/license-MIT-green)

---

## 🏭 How the automation works (the whole loop, zero clicks after launch)

```
 library/series/…/S01E01-….txt          # scripts carry their own metadata + engine tag
        │
        ▼  Actions: Render Episodes (Kaggle GPU)
 [1] estimate  ──► calibrated ETA printed to the run summary
 [2] push      ──► one Kaggle GPU kernel (Tesla T4) receives every episode
 [3] render    ──► per-script tags choose engine (kokoro) + voices (presets)
                   single narrator or dual narrator (Host + Dr. Meera)
 [4] pull      ──► audio lands in the library hierarchy
                   rendered/series-01-optometry-foundations/season-01/ep-01-what-is-optometry/
        │
        ▼
 [5] catalog   ──► library/master.json auto-updated (raw mp3 URLs + durations + all metadata)
 [6] commit    ──► rendered/ + master.json committed · artifact uploaded · timing report posted
```

Run it: **Actions → Focus Cast · Render Episodes (Kaggle GPU) → Run workflow** →
edit the episode list (or leave the default = all of Series 1, Season 1) → **Run**.
Typical wall time for a 5 × 30-minute batch: **~15–25 min** (render ≈ 25× realtime + queue).

Requires repo secrets `KAGGLE_USERNAME` / `KAGGLE_KEY` (configured ✓) on a
**phone-verified** Kaggle account (GPU gate — unverified accounts silently get CPU-only kernels).

---

## 📜 The Script folder — where episodes live

```
library/
├── series/series-01-optometry-foundations/
│   ├── series.json                       # 🔒 LOCKED Series-01 manifest (100 eps, 10 seasons,
│   │                                     #    core idea, anti-repetition master rule)
│   └── season-01-understanding-optometry/
│       ├── S01E01-what-is-optometry.txt
│       ├── S01E02-what-does-an-optometrist-do.txt
│       ├── S01E03-the-scope-of-optometric-practice.txt
│       ├── S01E04-optometry-and-eye-care.txt
│       └── S01E05-optometrist-ophthalmologist-and-optician.txt
├── presets/voices.json                   # 🎭 premade character→voice presets (voicepacks)
└── master.json                           # 📇 auto-updated library catalogue
```

### Every script carries its own automation instructions (metadata header)

```text
# Title: What Is Optometry?
# Series: Optometry Foundations
# Series No: 1
# Season: Understanding Optometry
# Season No: 1
# Episode No: 1
# Engine: kokoro              ← the model tag: kokoro (default) or voxcpm
# Narration: dual             ← dual narrator (speaker prefixes) or single
# Host: Host                  ← binds "Host:" lines to a preset character
# Expert: Dr. Meera           ← binds "Dr. Meera:" lines to a preset character
# Language: en
# Keywords: what is optometry, optometry definition, …      ← SEO
# Description: What is optometry, really? … Season 1 of Focus Cast by
#              focuslinks.in …                             ← SEO description
```

The body is dialogue. A speaker tag picks the voice — **no tag = default narrator**:

```text
Host: Welcome to Focus Cast, the audio library by focuslinks.in…
Dr. Meera: The word is built from two Greek roots…
```

That's the whole contract. Drop a new `.txt` in the folder with a header and it is
renderable — no code changes, ever.

---

## 🎭 Premade presets — consistent voices across the whole library

`library/presets/voices.json` binds **characters** (not scripts) to Kokoro voices, so
Episode 1 and Episode 95 share the same narrator identity:

| Character | Voice (Kokoro-82M) | Style |
|---|---|---|
| **Host** (default) | `af_heart` | warm, curious host |
| **Dr. Meera** | `am_michael` | calm optometry professor |
| **Dr. Arjun** | `bm_george` | British clinical lecturer (case files) |
| **Narrator** | `af_nova` | documentary single-narrator episodes |

Need a new character? Add one line to `voices.json` (choose from ~30 voicepacks listed
inside the file — American/British × male/female), reference the character in a script,
done. **Single-narrator episodes** simply omit speaker tags (or use the `Narrator`
preset). **VoxCPM** (tokenizer-free, zero-shot cloning) stays available for special
immersive episodes via `# Engine: voxcpm`.

---

## 📇 master.json — the library catalogue (auto-maintained)

After every render the workflow runs `scripts/update_master.py`, which rebuilds
`library/master.json`:

```json
{
  "library": "Focus Cast by focuslinks.in",
  "episode_count": 5,
  "episodes": [{
    "id": "S01E01",
    "series": "Optometry Foundations",
    "season_no": 1,
    "title": "What Is Optometry?",
    "keywords": ["what is optometry", "…"],
    "description": "SEO description…",
    "narration": "dual",
    "engine": "kokoro",
    "voices": { "Host": "af_heart", "Dr. Meera": "am_michael" },
    "audio": {
      "mp3": "rendered/series-01-optometry-foundations/season-01/…/S01E01-what-is-optometry.mp3",
      "raw_url": "https://raw.githubusercontent.com/stromplayz/FocusCast/main/rendered/…mp3",
      "duration_min": 28.4
    }
  }]
}
```

Idempotent by design: re-runs update in place, stale entries drop out, anything
without library tags (demos) is ignored. Point any player, app, or website at this
one JSON file and it always knows the whole library.

---

## ⏱ Time estimation (calibrated, not guessed)

The estimator is calibrated against real Kaggle-T4 runs and printed at three moments:
before launch (workflow summary), after completion (estimate vs actual table), and as
`rendered/<slug>.timing.json` committed next to the audio.

| Engine | Model | Throughput (measured) | 30-min episode |
|---|---|---|---|
| **kokoro** (default) | Kokoro-82M, 24 kHz | ~25–30× realtime on T4 | ~2–4 min render |
| **voxcpm** (special) | VoxCPM2, 48 kHz | 20.7 s/chunk on T4 | ~20–25 min render |

Legacy calibration (VoxCPM2, 56 chunks, cochlea): predicted 21.7 min → actual 21.7 min.

---

## 🗂 Rendered output hierarchy

```
rendered/
├── series-01-optometry-foundations/
│   └── season-01-understanding-optometry/
│       ├── ep-01-what-is-optometry/     S01E01-….mp3 · .meta.json
│       ├── ep-02-…/                     …
│       └── ep-05-…/
├── demos/                               # pre-FocusCast engine demos (retina, cochlea)
└── focuscast-batch.timing.json          # latest batch timing report
```

MP3s are committed at 96 kbps mono (spoken-word transparent, repo-friendly);
WAVs stay on Kaggle + in the 30-day Actions artifact (`--no-wav` keeps them out of git).

---

## 🔒 Series 01 — locked draft & the anti-repetition master rule

**Series 01 · Optometry Foundations** — 100 episodes, 10 seasons — is locked as the
foundation database (full list in `series.json`). The rule that governs all future series:

> **One concept → one primary teaching home.** Later appearances must add a different
> learning purpose (depth, technique, interpretation, clinical application, or cases) —
> never a re-record. Series 01 E33 *Myopia* → Series 06 *Myopic Refraction: full clinical
> management* → Series 27 *Case: progressive myopia* → Series 28 *Viva: myopia questions*
> are all **different learning purposes**, not duplicates.

Do not start Series 02 until Series 01's scope is fully locked; Series 02 must explicitly
exclude everything covered here.

---

## 💻 Local / CLI use (optional)

```bash
pip install kokoro soundfile numpy espeak-ng ffmpeg   # kokoro path
python scripts/generate_tts.py --episode library/series/…/S01E01-what-is-optometry.txt --outdir /tmp
python scripts/kaggle_render_driver.py --estimate-only --episode library/series/…/S01E01-….txt
python scripts/kaggle_render_driver.py --episode library/…/S01E01-….txt --episode library/…/S01E02-….txt --no-wav
python scripts/update_master.py                       # rebuild the catalogue manually
```

## 📁 Repo layout

```
├── library/                     # 🧠 the Workbench (scripts, presets, catalogue)
├── rendered/                    # 🎧 finished audio in library hierarchy
├── scripts/
│   ├── generate_tts.py          # renderer: headers, dual narration, kokoro/voxcpm, mp3
│   ├── kaggle_render_driver.py  # batch push/poll/pull + ETA + hierarchy mapping
│   └── update_master.py         # master.json builder (idempotent)
├── .github/workflows/kaggle.yml # ⚡ the factory (estimate → render → catalogue → commit)
├── .github/workflows/generate.yml  # legacy single-episode CPU renderer
└── .devcontainer/               # Codespaces one-click environment
```

## 🔐 Security notes

- Kaggle credentials live only in encrypted repo Actions secrets — never in code.
- Phone-verify the Kaggle account or kernels silently lose GPU + internet.
- Rotate any credential that ever appears in chat history.
