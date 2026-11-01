"""Check and fix the links of the blog posts in `content/posts/`.

    uv run python utils/validate_links.py             # fix internal links in place, report the rest
    uv run python utils/validate_links.py --check     # report only, write nothing (exit 1 if broken)
    uv run python utils/validate_links.py --external  # also curl every external link and mark
                                                      # the dead ones "(enlace roto)"

The blog now lives at `www.seraph.to/blog/<slug>` (the slug the app gives each
post: `Slug:` or the file name, see `web/blog/paths.py`). Older posts link to
where the blog used to be, and those links are rewritten to the current route:

- Pelican on `www.seraph.to` / `ecrespo.github.io`: `/<title-slug>.html`,
  `/tag/<tag>.html`, `/category/<name>.html`;
- Blogger on `blog.crespo.org.ve` / `ernesto-ecrespo.blogspot.com`:
  `/YYYY/MM/<truncated-title>.html` and `/search/label/<label>`.

It also repairs references the page cannot follow: external links written
without `https://` (a browser takes them as paths of this site), image paths
in quotes or in `./imagenes/`. Fenced code blocks are left alone.
"""

from __future__ import annotations

import argparse
import difflib
import re
import subprocess  # nosec B404
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from web.blog.paths import blog_data  # noqa: E402

POSTS = ROOT / "content" / "posts"
IMAGES = {p.name for p in (ROOT / "assets" / "blog" / "images").iterdir()}

# Domains where the blog lived. Only post, tag, category and label URLs are
# rewritten; a bare domain (a historical mention) is reported, not changed.
OLD_BLOG = re.compile(
    r"^(https?:)?//(www\.seraph\.to|seraph\.to|blog\.seraph\.to|ecrespo\.github\.io|"
    r"blog\.crespo\.org\.ve|ernesto-ecrespo\.blogspot\.com)(?=/|$)",
    re.I,
)
BROKEN_MARK = " (enlace roto)"
# Blog index pages that are routes of their own, not posts.
BLOG_PAGES = {"archives", "categories", "tags"}
# A host-like start: `pypi.python.org/…`, `www.cencoex.gob.ve`.
SCHEMELESS = re.compile(
    r"^(www\.|[a-z0-9-]+(\.[a-z0-9-]+)*\.(org|com|net|ve|io|ch|gov|edu)\b)", re.I
)

MD_LINK = re.compile(
    r"(!?\[(?P<text>[^\]]*)\])\((?P<url>[^)\s]+|\"[^\"]*\"|<[^>]*>)(?P<title>\s+\"[^\"]*\")?\)"
)
HTML_ATTR = re.compile(r"(?P<attr>\b(?:href|src)\s*=\s*)(?P<q>[\"'])(?P<url>[^\"']+)(?P=q)")
FENCE = re.compile(r"^\s*(```|~~~)")


def slugify(text: str) -> str:
    """Pelican's slug of a title."""
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[-\s_]+", "-", text).strip("-")


def _key(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", text.lower())


def _title_key(post) -> str:
    return _key(slugify(post.title))


KEYS: dict[str, str] = {}
for _slug, _post in blog_data.items():
    for _k in (_title_key(_post), _key(_post.metadata.get("slug", "")), _key(_slug)):
        if _k:
            KEYS.setdefault(_k, _slug)


def resolve_old(url: str) -> str | None:
    """The current route for a URL of the old blog, or None."""
    path = OLD_BLOG.sub("", url).split("#")[0].split("?")[0].strip("/")
    if not path:
        return None
    if path.startswith(("tag/", "search/label/")):
        return "/blog/tags"
    if path.startswith("category/"):
        return "/blog/categories"
    base = _key(path.rsplit("/", 1)[-1].removesuffix(".html"))
    if base in KEYS:
        return f"/blog/{KEYS[base]}"
    # Blogger: /YYYY/MM/<title truncated to ~40 characters>.html
    month = re.match(r"(\d{4})/(\d{2})/", path)
    if not month or len(base) < 10:
        return None
    candidates = [
        (slug, _title_key(post))
        for slug, post in blog_data.items()
        if post.date.strftime("%Y/%m") == f"{month[1]}/{month[2]}"
    ]
    scored = [
        (difflib.SequenceMatcher(None, base, key[: len(base) + 5]).ratio(), slug)
        for slug, key in candidates
    ]
    score, slug = max(scored, default=(0.0, ""))
    return f"/blog/{slug}" if score >= 0.85 else None


def fix_url(url: str, text: str) -> tuple[str, str | None]:
    """(new url, problem): the URL the page can follow, or the problem left to report."""
    bare = url.strip('"<>')
    if OLD_BLOG.match(bare):
        new = resolve_old(bare)
        return (new, None) if new else (bare, "old blog URL without a match")
    if bare.startswith("/blog/"):
        slug = bare[len("/blog/") :].split("#")[0].rstrip("/")
        if slug.startswith("images/"):
            return bare, None if slug[7:] in IMAGES else "missing image"
        return bare, None if slug in blog_data or slug in BLOG_PAGES else "unknown post"
    for prefix in ("./images/", "images/", "./imagenes/", "imagenes/"):
        if bare.startswith(prefix):
            name = bare[len(prefix) :]
            if name in IMAGES:
                return f"./images/{name}", None
            return bare, "missing image"
    if SCHEMELESS.match(bare):
        return f"https://{bare}", None
    return bare, None


def fix_text(text: str, path: Path, problems: list[str]) -> str:
    def md(m: re.Match) -> str:
        label, url = m["text"], m["url"]
        new, problem = fix_url(url, label)
        if problem:
            problems.append(f"{path.name}: {problem}: {url}")
            return m[0]
        if new == url:
            return m[0]
        head = m[1]
        if BROKEN_MARK in label:
            head = head.replace(BROKEN_MARK, "")
        return f"{head}({new}{m['title'] or ''})"

    def html(m: re.Match) -> str:
        new, problem = fix_url(m["url"], "")
        if problem:
            problems.append(f"{path.name}: {problem}: {m['url']}")
        return f"{m['attr']}{m['q']}{new}{m['q']}"

    out, block, fenced = [], [], False
    for line in text.splitlines(keepends=True):
        if FENCE.match(line):
            if not fenced:
                out.append(HTML_ATTR.sub(html, MD_LINK.sub(md, "".join(block))))
                block = []
            fenced = not fenced
            out.append(line)
        elif fenced:
            out.append(line)
        else:
            block.append(line)
    out.append(HTML_ATTR.sub(html, MD_LINK.sub(md, "".join(block))))
    return "".join(out)


def check_external(text: str, path: Path) -> str:
    """Mark external links that do not answer as "(enlace roto)"."""

    def md(m: re.Match) -> str:
        url, label = m["url"], m["text"]
        if not url.startswith("http") or BROKEN_MARK in label or "localhost" in url:
            return m[0]
        ok = (
            subprocess.run(  # nosec B603 B607
                ["curl", "-I", "-L", "--max-time", "8", "--fail", "-s", "-o", "/dev/null", url],
                check=False,
            ).returncode
            == 0
        )
        if ok:
            return m[0]
        print(f"{path.name}: dead external link: {url}")
        return m[0].replace(f"[{label}]", f"[{label}{BROKEN_MARK}]", 1)

    return MD_LINK.sub(md, text)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="report only, write nothing")
    parser.add_argument("--external", action="store_true", help="also curl external links")
    args = parser.parse_args()

    changed, problems = 0, []
    for path in sorted(POSTS.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        new = fix_text(text, path, problems)
        if args.external:
            new = check_external(new, path)
        if new != text:
            changed += 1
            if args.check:
                print(f"{path.name}: needs fixing")
            else:
                path.write_text(new, encoding="utf-8")
    verb = "need fixing" if args.check else "fixed"
    print(f"{changed} posts {verb}; {len(problems)} links left to review")
    for problem in problems:
        print("  " + problem)
    return 1 if args.check and (changed or problems) else 0


if __name__ == "__main__":
    raise SystemExit(main())
