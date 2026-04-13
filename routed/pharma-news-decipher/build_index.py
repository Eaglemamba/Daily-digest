#!/usr/bin/env python3
"""
build_index.py — Pharma News Decipher Index Generator

Scans docs/*.html for meta tags and regenerates the articles array
in docs/index.html between the AUTO-GENERATED markers.
"""

import glob
import os
import re
import json
from html.parser import HTMLParser


class MetaExtractor(HTMLParser):
    """Extract doc-* meta tags from HTML files."""

    META_FIELDS = {
        "doc-date", "doc-title", "doc-source",
        "doc-tags", "doc-rating", "doc-summary", "doc-file"
    }

    def __init__(self):
        super().__init__()
        self.meta = {}

    def handle_starttag(self, tag, attrs):
        if tag == "meta":
            attrs_dict = dict(attrs)
            name = attrs_dict.get("name", "")
            content = attrs_dict.get("content", "")
            if name in self.META_FIELDS:
                self.meta[name] = content


def extract_meta(filepath):
    """Extract metadata from a single HTML file."""
    parser = MetaExtractor()
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            # Only parse the head section for performance
            content = f.read()
            head_match = re.search(r"<head>(.*?)</head>", content, re.DOTALL)
            if head_match:
                parser.feed(head_match.group(1))
            else:
                parser.feed(content)
    except Exception as e:
        print(f"  [WARN] Failed to parse {filepath}: {e}")
        return None

    meta = parser.meta
    # Validate required fields
    required = {"doc-date", "doc-title", "doc-file"}
    if not required.issubset(meta.keys()):
        missing = required - meta.keys()
        print(f"  [SKIP] {filepath} — missing: {', '.join(missing)}")
        return None

    return {
        "date": meta.get("doc-date", ""),
        "title": meta.get("doc-title", ""),
        "source": meta.get("doc-source", ""),
        "tags": [t.strip() for t in meta.get("doc-tags", "").split(",") if t.strip()],
        "rating": meta.get("doc-rating", ""),
        "summary": meta.get("doc-summary", ""),
        "file": meta.get("doc-file", ""),
    }


def build_articles_js(articles):
    """Build the const articles = [...] JavaScript string."""
    lines = ["const articles = ["]
    for i, a in enumerate(articles):
        comma = "," if i < len(articles) - 1 else ""
        tags_str = json.dumps(a["tags"], ensure_ascii=False)
        lines.append("  {")
        lines.append(f'    date: "{a["date"]}",')
        lines.append(f'    title: {json.dumps(a["title"], ensure_ascii=False)},')
        lines.append(f'    source: {json.dumps(a["source"], ensure_ascii=False)},')
        lines.append(f"    tags: {tags_str},")
        lines.append(f'    rating: "{a["rating"]}",')
        lines.append(f'    summary: {json.dumps(a["summary"], ensure_ascii=False)},')
        lines.append(f'    file: {json.dumps(a["file"], ensure_ascii=False)}')
        lines.append("  }" + comma)
    lines.append("];")
    return "\n".join(lines)


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    docs_dir = os.path.join(script_dir, "docs")
    index_path = os.path.join(docs_dir, "index.html")

    # Find all article HTML files (exclude index.html)
    html_files = sorted(glob.glob(os.path.join(docs_dir, "*.html")))
    html_files = [f for f in html_files if os.path.basename(f) != "index.html"]

    print(f"Scanning {len(html_files)} HTML files in docs/...")

    articles = []
    for filepath in html_files:
        meta = extract_meta(filepath)
        if meta:
            articles.append(meta)
            print(f"  [OK] {meta['date']} — {meta['title']}")

    # Sort newest first
    articles.sort(key=lambda a: a["date"], reverse=True)

    print(f"\nTotal articles: {len(articles)}")

    # Generate JS block
    js_block = build_articles_js(articles)

    # Read index.html
    if not os.path.exists(index_path):
        print(f"[ERROR] {index_path} not found!")
        return

    with open(index_path, "r", encoding="utf-8") as f:
        index_content = f.read()

    # Replace between markers
    start_marker = "// AUTO-GENERATED START"
    end_marker = "// AUTO-GENERATED END"

    pattern = re.compile(
        re.escape(start_marker) + r".*?" + re.escape(end_marker),
        re.DOTALL
    )

    if not pattern.search(index_content):
        print("[ERROR] AUTO-GENERATED markers not found in index.html!")
        return

    replacement = f"{start_marker}\n{js_block}\n{end_marker}"
    new_content = pattern.sub(replacement, index_content)

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"\nIndex updated: {index_path}")
    print("Done!")


if __name__ == "__main__":
    main()
