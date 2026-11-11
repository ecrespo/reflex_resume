"""Check the English translations of the blog posts against their Spanish originals.

    uv run python utils/check_translations.py                 # every post
    uv run python utils/check_translations.py FILE.md [...]   # only these posts (file names)

The posts are written in Spanish (`content/posts/`); each one has an English
translation with the same file name in `content/posts_en/`. A translation must
keep everything that is not prose exactly as it is, so the check compares:

- the header: same `Slug` and `Date`, `lang: en`, a `Title` and a `Summary`;
- fenced code blocks: identical, in the same order;
- inline code spans: the same multiset;
- link, image and HTML `href`/`src` targets: the same multiset;
- length: the prose stays within a sane ratio of the original;
- language: flags a translation where Spanish function words remain common.

Exit 1 when a post fails, listing the reasons.
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ES_DIR = ROOT / "content" / "posts"
EN_DIR = ROOT / "content" / "posts_en"

# CommonMark fences: an opening line has no closing run after it (```x``` is inline
# code), and only a bare fence closes a block (```python inside one is content).
OPEN_FENCE = re.compile(r"^\s{0,3}(`{3,}|~{3,})(?!.*`{3})")
CLOSE_FENCE = re.compile(r"^\s{0,3}(`{3,}|~{3,})\s*$")
INLINE = re.compile(r"(?<!`)`([^`\n]+)`(?!`)")
TARGET = re.compile(r"\]\(\s*<?([^)\s>]+)|\b(?:href|src)\s*=\s*[\"']([^\"']+)")
HEADER = re.compile(r"^([A-Za-z_]+):\s*(.*)$")
SPANISH = re.compile(
    r"\b(el|los|las|que|para|con|una|del|por|como|este|esta|pero|también|cuando|puede|"
    r"siguiente|archivo|ahora|está|son|sobre)\b",
    re.I,
)
ENGLISH = re.compile(r"\b(the|and|that|with|for|this|from|which|can|is|are|to|of)\b", re.I)


def split(text: str) -> tuple[dict[str, str], str]:
    """Header fields (lower-case keys) and the body."""
    header, lines = {}, text.splitlines()
    i = 0
    for i, line in enumerate(lines):
        if not line.strip():
            i += 1
            break
        m = HEADER.match(line)
        if not m:
            break
        header[m[1].lower()] = m[2].strip()
    else:
        i = len(lines)
    return header, "\n".join(lines[i:])


def parts(body: str) -> tuple[list[str], str]:
    """Fenced code blocks (with their fence lines) and the prose outside them."""
    blocks, prose, current, fenced, opener = [], [], [], False, ""
    for line in body.splitlines():
        if not fenced and (match := OPEN_FENCE.match(line)):
            current.append(line.rstrip())
            fenced, opener = True, match.group(1)
        elif (
            fenced
            and (match := CLOSE_FENCE.match(line))
            # A closing fence uses the opener's character, at least as many times:
            # ```` can wrap a block that contains ``` fences.
            and match.group(1)[0] == opener[0]
            and len(match.group(1)) >= len(opener)
        ):
            current.append(line.rstrip())
            blocks.append("\n".join(current))
            current, fenced = [], False
        elif fenced:
            current.append(line.rstrip())
        else:
            prose.append(line)
    if current:
        blocks.append("\n".join(current))
    return blocks, "\n".join(prose)


def targets(text: str) -> Counter:
    return Counter(next(g for g in m.groups() if g) for m in TARGET.finditer(text))


def check(name: str) -> list[str]:
    es_path, en_path = ES_DIR / name, EN_DIR / name
    if not en_path.exists():
        return ["missing translation"]
    es_head, es_body = split(es_path.read_text(encoding="utf-8"))
    en_head, en_body = split(en_path.read_text(encoding="utf-8"))
    problems = []

    for key in ("slug", "date"):
        if es_head.get(key, "") != en_head.get(key, ""):
            problems.append(f"header {key!r} changed: {es_head.get(key)!r} -> {en_head.get(key)!r}")
    if en_head.get("lang", "") != "en":
        problems.append("header lang is not 'en'")
    for key in ("title", "summary"):
        if es_head.get(key) and not en_head.get(key):
            problems.append(f"header {key!r} missing")

    es_blocks, es_prose = parts(es_body)
    en_blocks, en_prose = parts(en_body)
    if es_blocks != en_blocks:
        if len(es_blocks) != len(en_blocks):
            problems.append(
                f"code blocks: {len(es_blocks)} in Spanish, {len(en_blocks)} in English"
            )
        else:
            changed = [
                i + 1 for i, (a, b) in enumerate(zip(es_blocks, en_blocks, strict=True)) if a != b
            ]
            problems.append(f"code blocks changed: #{', #'.join(map(str, changed))}")

    es_inline, en_inline = Counter(INLINE.findall(es_prose)), Counter(INLINE.findall(en_prose))
    if es_inline != en_inline:
        lost = list((es_inline - en_inline).elements())[:5]
        added = list((en_inline - es_inline).elements())[:5]
        problems.append(f"inline code differs: missing {lost}, extra {added}")

    es_targets, en_targets = targets(es_body), targets(en_body)
    if es_targets != en_targets:
        lost = list((es_targets - en_targets).elements())[:5]
        added = list((en_targets - es_targets).elements())[:5]
        problems.append(f"links differ: missing {lost}, extra {added}")

    es_words = len(INLINE.sub("", es_prose).split())
    en_words = len(INLINE.sub("", en_prose).split())
    if es_words > 30 and not 0.6 <= en_words / es_words <= 1.6:
        problems.append(f"prose length {en_words} words vs {es_words} in Spanish")

    plain = INLINE.sub("", en_prose)
    spanish, english = len(SPANISH.findall(plain)), len(ENGLISH.findall(plain))
    if spanish > 8 and spanish > 0.25 * english:
        problems.append(
            f"looks untranslated: {spanish} Spanish vs {english} English function words"
        )
    return problems


def main(argv: list[str]) -> int:
    names = [Path(a).name for a in argv] or sorted(p.name for p in ES_DIR.glob("*.md"))
    failed = 0
    for name in names:
        problems = check(name)
        if problems:
            failed += 1
            print(f"FAIL {name}")
            for problem in problems:
                print(f"     {problem}")
    print(f"{len(names) - failed}/{len(names)} translations pass")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
