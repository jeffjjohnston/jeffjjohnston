"""Fetch the latest blog posts from the Atom feed and update README.md."""

import urllib.request
import xml.etree.ElementTree as ET

FEED_URL = "https://jeffjjohnston.github.io/feed.xml"
README_PATH = "README.md"
NUM_POSTS = 5
START_MARKER = "<!-- BLOG-POSTS:START -->"
END_MARKER = "<!-- BLOG-POSTS:END -->"
ATOM_NS = "{http://www.w3.org/2005/Atom}"


def fetch_latest_posts():
    with urllib.request.urlopen(FEED_URL) as resp:
        tree = ET.parse(resp)
    entries = tree.findall(f"{ATOM_NS}entry")[:NUM_POSTS]
    posts = []
    for entry in entries:
        title = entry.find(f"{ATOM_NS}title").text
        link = entry.find(f"{ATOM_NS}link").get("href")
        posts.append(f"- [{title}]({link})")
    return "\n".join(posts)


def update_readme(posts_md):
    with open(README_PATH) as f:
        content = f.read()
    start = content.index(START_MARKER) + len(START_MARKER)
    end = content.index(END_MARKER)
    updated = content[:start] + "\n" + posts_md + "\n" + content[end:]
    with open(README_PATH, "w") as f:
        f.write(updated)


if __name__ == "__main__":
    posts_md = fetch_latest_posts()
    update_readme(posts_md)
    print("README.md updated with latest posts.")
