"""Download the certificate images used by the certifications timeline.

Every slide in `assets/timeline.json` points at a Google Drive file. Drive's
preview iframe letterboxes the page on a black background, and Google refuses
(HTTP 429) to serve its thumbnails to browsers hotlinking them from another
site, so each certificate is saved once as `assets/certificates/<drive id>.jpg`
and served with the static site. `web/timeline_data.py` uses the local image
when it exists and links it to the Drive file.

Run from the repo root after adding certificates; existing files are skipped:

    uv run python utils/fetch_certificates.py
"""

import json
import re
import sys
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parent.parent
TIMELINE_JSON = ROOT / "assets" / "timeline.json"
CERTIFICATES_DIR = ROOT / "assets" / "certificates"

DRIVE_FILE = re.compile(r"^https://drive\.google\.com/file/d/([\w-]+)")
# 800px wide JPEG at quality 75: sharp at the timeline's media width, ~80 KB each.
IMAGE_URL = "https://lh3.googleusercontent.com/d/{file_id}=w800-rj-l75"


def drive_ids() -> list[str]:
    data = json.loads(TIMELINE_JSON.read_text(encoding="utf-8"))
    ids = []
    for slide in data.get("events", []):
        match = DRIVE_FILE.match((slide.get("media") or {}).get("url", ""))
        if match and match.group(1) not in ids:
            ids.append(match.group(1))
    return ids


def main() -> int:
    CERTIFICATES_DIR.mkdir(parents=True, exist_ok=True)
    failed = []
    with httpx.Client(timeout=30, follow_redirects=True) as client:
        for file_id in drive_ids():
            target = CERTIFICATES_DIR / f"{file_id}.jpg"
            if target.exists():
                continue
            response = client.get(IMAGE_URL.format(file_id=file_id))
            if response.status_code != 200 or response.headers.get("content-type") != "image/jpeg":
                failed.append(f"{file_id}: HTTP {response.status_code}")
                continue
            target.write_bytes(response.content)
            print(f"saved {target.relative_to(ROOT)}")
    for line in failed:
        print(f"failed {line}", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
