import os
import sys

# ElementTree is only used to build the feed, never to parse untrusted XML.
import xml.etree.ElementTree as ET  # nosec B405
from datetime import UTC, datetime
from pathlib import Path

# Add parent directory to path to allow imports
sys.path.append(os.getcwd())

from web.blog.paths import sorted_posts

# The blog lives under the main site since the move off blog.seraph.to.
SITE = "https://www.seraph.to"

# One Atom feed per language, next to the pages it describes: English at
# /feed.xml (the /blog pages), Spanish at /es/feed.xml (the /es/blog pages).
FEEDS = {
    "en": ("feed.xml", "", "Seraph/Lille's blog"),
    "es": ("es/feed.xml", "/es", "Blog de Seraph/Lille"),
}


def feed_url(lang: str) -> str:
    """The site path of the feed in `lang`: `/feed.xml` or `/es/feed.xml`."""
    return "/" + FEEDS[lang][0]


def build_feed(lang: str) -> bytes:
    """The Atom feed of every post in `lang` (the English translation, or the original)."""
    path, prefix, title = FEEDS[lang]
    feed = ET.Element("feed", xmlns="http://www.w3.org/2005/Atom")
    feed.set("xml:lang", lang)
    ET.SubElement(feed, "title").text = title

    link_self = ET.SubElement(feed, "link")
    link_self.set("href", f"{SITE}/{path}")
    link_self.set("rel", "self")

    link_alt = ET.SubElement(feed, "link")
    link_alt.set("href", f"{SITE}{prefix}/blog")
    link_alt.set("rel", "alternate")

    ET.SubElement(feed, "id").text = f"{SITE}{prefix}/blog"

    updated_time = datetime.now(UTC)
    if sorted_posts:
        latest = sorted_posts[0].date
        updated_time = latest if latest.tzinfo else latest.replace(tzinfo=UTC)
    ET.SubElement(feed, "updated").text = updated_time.isoformat()

    author = ET.SubElement(feed, "author")
    ET.SubElement(author, "name").text = "Ernesto Crespo"
    ET.SubElement(author, "email").text = "ecrespo@gmail.com"

    for post in sorted_posts:
        card = post.card(lang)
        entry = ET.SubElement(feed, "entry")
        ET.SubElement(entry, "title").text = card["title"]

        # The id is the post's page in this language. English keeps the ids the
        # single feed at /feed.xml always had, so its readers see no new entries.
        post_url = f"{SITE}{prefix}/blog/{post.slug}"
        ET.SubElement(entry, "link").set("href", post_url)
        ET.SubElement(entry, "id").text = post_url

        dt = post.date if post.date.tzinfo else post.date.replace(tzinfo=UTC)
        ET.SubElement(entry, "published").text = dt.isoformat()
        ET.SubElement(entry, "updated").text = dt.isoformat()
        ET.SubElement(entry, "summary").text = card["summary"]

        author_entry = ET.SubElement(entry, "author")
        ET.SubElement(author_entry, "name").text = post.author

        for term in [card["category"], *card["tags"]]:
            ET.SubElement(entry, "category").set("term", term)

    return b'<?xml version="1.0" encoding="utf-8"?>\n' + ET.tostring(feed, encoding="utf-8")


def generate_feeds() -> None:
    """Write `assets/feed.xml` (English) and `assets/es/feed.xml` (Spanish)."""
    for lang, (path, _, _) in FEEDS.items():
        output = Path("assets") / path
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(build_feed(lang))
        print(f"Atom feed ({lang}) generated at {output}")


if __name__ == "__main__":
    generate_feeds()
