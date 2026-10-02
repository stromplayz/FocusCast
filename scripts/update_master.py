#!/usr/bin/env python3
"""Focus Cast — build/update library/master.json from rendered/ outputs.

Scans rendered/**/ for <stem>.meta.json files written by the renderer. Every
library episode (tagged with Title/Series/Season/Episode No in its script
header) becomes or updates one entry in master.json with:
  - all script metadata (title, series, season, episode no, keywords, description)
  - engine + voices actually used
  - mp3 path inside the repo + its raw.githubusercontent.com URL
  - duration (minutes/seconds) of the mp3

Idempotent: safe to run after every render; existing entries are updated,
missing ones appended, and stale ones (audio no longer present) are dropped.
Demo renders without library tags are skipped.

Spoken-brand rule: catalog text keeps the spoken brand line
"Focus Cast by focuslinks" (never "focuslinks dot in" inside audio scripts).
"""
from __future__ import annotations

import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RENDERED = ROOT / "rendered"
MASTER = ROOT / "library" / "master.json"


def repo_slug() -> str:
    env = os.environ.get("GITHUB_REPOSITORY")
    if env:
        return env
    try:
        url = subprocess.run(["git", "config", "--get", "remote.origin.url"],
                             capture_output=True, text=True, check=True,
                             cwd=ROOT).stdout.strip()
        m = re.search(r"github\.com[:/](.+?)(?:\.git)?$", url)
        if m:
            return m.group(1)
    except Exception:
        pass
    return "stromplayz/FocusCast"


def slugify(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return re.sub(r"-{2,}", "-", s)


def find_script(stem: str) -> str | None:
    hits = list((ROOT / "library" / "series").rglob(f"{stem}.txt"))
    return str(hits[0].relative_to(ROOT)) if hits else None


def main() -> None:
    repo = repo_slug()
    now = datetime.now(timezone.utc).isoformat()

    master = {"library": "FocusLinks Listen · Focus Cast",
              "repo": repo,
              "updated_at": now, "episode_count": 0, "episodes": []}
    if MASTER.exists():
        try:
            old = json.loads(MASTER.read_text(encoding="utf-8"))
            # keep only entries whose mp3 is still on disk (drop stale renders)
            kept = []
            for e in old.get("episodes", []):
                mp3_rel = (e.get("audio") or {}).get("mp3")
                if mp3_rel and (ROOT / mp3_rel).exists():
                    kept.append(e)
                else:
                    print(f"[master] drop stale entry {e.get('id')}: mp3 missing")
            master["episodes"] = kept
        except Exception:
            pass

    by_id = {e.get("id"): e for e in master["episodes"]}

    found = 0
    for meta_path in sorted(RENDERED.rglob("*.meta.json")):
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        # library episodes carry a Title + numeric Episode No header; demos don't
        if not meta.get("title") or meta.get("episode_no") in (None, ""):
            continue
        stem = meta.get("stem") or meta_path.stem.replace(".meta", "")
        folder = meta_path.parent
        mp3 = next((f for f in meta.get("files", []) if f.endswith(".mp3")), None)
        mp3_path = folder / mp3 if mp3 else None
        if not mp3_path or not mp3_path.exists():
            print(f"[master] skip {stem}: no mp3 present")
            continue

        try:
            season_no = int(str(meta.get("season_no", 0)).split(" ")[0])
            episode_no = int(str(meta.get("episode_no", 0)).split(" ")[0])
            series_no = int(str(meta.get("series_no", 0)).split(" ")[0])
        except ValueError:
            print(f"[master] skip {stem}: unparseable numbering")
            continue

        ep_id = f"S{season_no:02d}E{episode_no:02d}"
        rel_mp3 = mp3_path.relative_to(ROOT).as_posix()
        entry = {
            "id": ep_id,
            "series_no": series_no,
            "series": meta.get("series", ""),
            "season_no": season_no,
            "season": meta.get("season", ""),
            "episode_no": episode_no,
            "title": meta.get("title", ""),
            "keywords": meta.get("keywords", []),
            "description": meta.get("description", ""),
            "language": meta.get("language", "en"),
            "narration": meta.get("narration", ""),
            "engine": meta.get("engine", ""),
            "voices": meta.get("voices", {}),
            "script": find_script(stem),
            "audio": {
                "mp3": rel_mp3,
                "raw_url": f"https://raw.githubusercontent.com/{repo}/main/{rel_mp3}",
                "bytes": mp3_path.stat().st_size,
                "duration_sec": meta.get("duration_sec"),
                "duration_min": meta.get("duration_min"),
                "sample_rate": meta.get("sample_rate"),
            },
            "generated_at_utc": meta.get("generated_at_utc", now),
        }
        by_id[ep_id] = entry
        found += 1
        print(f"[master] {ep_id} · {entry['title'][:48]} · "
              f"{entry['audio']['duration_min']} min · {entry['audio']['raw_url']}")

    episodes = sorted(by_id.values(),
                      key=lambda e: (e.get("series_no", 0), e.get("season_no", 0),
                                     e.get("episode_no", 0)))
    master["episodes"] = episodes
    master["episode_count"] = len(episodes)
    master["updated_at"] = now
    MASTER.parent.mkdir(parents=True, exist_ok=True)
    MASTER.write_text(json.dumps(master, indent=2) + "\n", encoding="utf-8")
    print(f"[master] library/master.json written — {len(episodes)} episode(s), "
          f"{found} updated this run")


if __name__ == "__main__":
    main()
