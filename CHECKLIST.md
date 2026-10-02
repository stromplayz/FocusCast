# FocusLinks Listen · Focus Cast — Production Checklist

> **FocusLinks Listen** · listen.focuslinks.in — *Listen. Learn. See better.*
> Show: **Focus Cast by focuslinks** · Series 1 = Season 1 + Season 2 (20 episodes)
> Track every artifact here. Tick a box only when the thing is real and verified.

---

## 1 · Platform & Branding

- [x] Show name locked: **Focus Cast** (part of the FocusLinks Listen platform)
- [x] Platform name locked: **FocusLinks Listen** — home `listen.focuslinks.in`
- [x] Tagline locked: *Listen. Learn. See better.*
- [x] Spoken brand rule: audio says **"Focus Cast by focuslinks"** — never "focuslinks dot in" (TTS mispronounces the domain; `.in` is written-only branding)
- [x] No named/fictional doctor personas (old "Dr. Meera" removed as misleading) → dual narration is **Host + Guide** (Guide is a role, never named, never claims credentials)
- [x] License switched MIT → **FocusLinks Proprietary License** (all rights reserved, nothing permitted without written permission)
- [x] Domain shortlist documented (final platform home: `listen.focuslinks.in`)

## 2 · Pipeline (workbench)

- [x] Repo: `stromplayz/FocusCast`
- [x] Renderer `scripts/generate_tts.py` — kokoro + voxcpm, header parsing, dual-narrator voice presets
- [x] Driver `scripts/kaggle_render_driver.py` — batch push → T4 render → pull → hierarchy `rendered/series-NN/season-NN/ep-NN/`, calibrated ETA
- [x] Catalog `scripts/update_master.py` — rebuilds `library/master.json` (raw URLs, durations, metadata), drops stale entries
- [x] Workflow `.github/workflows/kaggle.yml` — estimate → render → catalog → commit + timing report
- [x] Presets `library/presets/voices.json` — Host (af_heart), Guide (am_michael), Narrator (af_nova) + ~30 voicepacks
- [x] Series bible `library/series/series-01-optometry-foundations/series.json` — Series 1 locked: 10 seasons × 10 episodes (100 topics), anti-repetition rule
- [x] `library/master.json` reset after test-batch deletion (0 episodes — rebuilds on next render)

## 3 · Quality gates (every script)

- [x] Header has all of: `Title`, `Series`, `Series No`, `Season`, `Season No`, `Episode No`, `Engine`, `Narration`, `Language`, `Keywords`, `Description`
- [x] SEO `Description` (3–5 sentences) + 8–12 `Keywords`
- [x] Speakers are ONLY `Host:` and `Guide:` (or single `Narrator:`) — no named doctors, no credentials claimed
- [x] Brand line said exactly as "Focus Cast by focuslinks" (intro + outro); zero occurrences of `focuslinks.in` / "dot in"
- [x] Written for the ear: no symbols (write "percent", "twenty twenty"), no slashes/ampersands, no URLs
- [x] Target length 4,000–4,500 words ≈ 28–30 min at 150 wpm
- [x] Anti-repetition: one concept → one primary teaching home (checked against series.json)

## 4 · Series 1 · Season 1 — "Understanding Optometry"

| # | Episode | Script | Rendered | In master.json |
|---|---------|--------|----------|----------------|
| 01 | What Is Optometry? | [x] | [ ] | [ ] |
| 02 | What Does an Optometrist Do? | [x] | [ ] | [ ] |
| 03 | The Scope of Optometric Practice | [x] | [ ] | [ ] |
| 04 | Optometry and Eye Care | [x] | [ ] | [ ] |
| 05 | Optometrist, Ophthalmologist and Optician | [x] | [ ] | [ ] |
| 06 | The Optometrist's Role in Patient Care | [x] | [ ] | [ ] |
| 07 | Major Areas of Optometry | [x] | [ ] | [ ] |
| 08 | Clinical and Community Optometry | [x] | [ ] | [ ] |
| 09 | The Modern Optometry Practice | [x] | [ ] | [ ] |
| 10 | Your Journey Through Optometry | [x] | [ ] | [ ] |

Scripts live in `library/series/series-01-optometry-foundations/season-01/` as `S01E01-<slug>.txt` … `S01E10-<slug>.txt`.

## 5 · Series 1 · Season 2 — "The Eye as a Visual Organ"

| # | Episode | Script | Rendered | In master.json |
|---|---------|--------|----------|----------------|
| 01 | Why Do We Have Eyes? | [x] | [ ] | [ ] |
| 02 | From Light to Vision | [x] | [ ] | [ ] |
| 03 | The Eye as an Optical System | [x] | [ ] | [ ] |
| 04 | The Front of the Eye | [x] | [ ] | [ ] |
| 05 | The Back of the Eye | [x] | [ ] | [ ] |
| 06 | The Retina as the Sensory Layer | [x] | [ ] | [ ] |
| 07 | The Optic Nerve and Visual Information | [x] | [ ] | [ ] |
| 08 | The Macula and Central Vision | [x] | [ ] | [ ] |
| 09 | Peripheral Vision | [x] | [ ] | [ ] |
| 10 | Following the Path of Vision | [x] | [ ] | [ ] |

Scripts live in `library/series/series-01-optometry-foundations/season-02/` as `S02E01-<slug>.txt` … `S02E10-<slug>.txt`.

## 6 · Release tasks

- [x] Old 5-episode test batch deleted (scripts + rendered audio + catalog entries)
- [x] 20/20 scripts written and validated
- [ ] Render Season 1 batch via workflow (kokoro, ~ETA shown in run summary)
- [ ] Render Season 2 batch via workflow
- [ ] master.json shows 20 episodes with raw mp3 URLs
- [ ] Demo renders (`rendered/demos/`) kept as engine samples only

## 7 · Series 1 roadmap (Seasons 3–10, planned — do NOT script before S1–S2 are rendered & locked)

- [ ] Season 3 — Understanding Vision
- [ ] Season 4 — Optometric Terminology
- [ ] Season 5 — The Optometry Examination
- [ ] Seasons 6–10 — see `series.json` (single source of truth)
