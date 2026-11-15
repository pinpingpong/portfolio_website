"""
Rebuild the AI Twin's Pinecone index from the PUBLIC content of index.html only.

Each project/agent/tool/workflow card, each experience entry, the hero and the
education/skills blocks become one chunk. Everything is written to the "website"
namespace, which is wiped and rebuilt on every run, so removed cards disappear too.

Private documents (resume, raw performance reviews) must never go into this index:
the chatbot is public and can quote anything it retrieves.

Optional second namespace, "working-style": a curated, approved summary of colleague
feedback (themes plus short anonymous quotes) kept OUTSIDE this public repo, by default at
~/Document/resume/how_i_work.md (override with HOW_I_WORK_PATH). It is rebuilt only when that
file exists, so a run without it (e.g. CI) leaves the namespace untouched.

Setup:
  pip install pinecone google-genai

Usage:
  PINECONE_API_KEY=xxx GEMINI_API_KEY=xxx python scripts/build_public_index.py [--dry-run]
"""

import os
import re
import sys
import time
from html.parser import HTMLParser
from pathlib import Path

INDEX_HTML = Path(__file__).resolve().parent.parent / "index.html"
PINECONE_INDEX = "pinxiu-portfolio"
NAMESPACE = "website"
STYLE_NAMESPACE = "working-style"
STYLE_PATH = Path(os.environ.get("HOW_I_WORK_PATH", "~/Document/resume/how_i_work.md")).expanduser()
EMBED_MODEL = "gemini-embedding-001"
DIMENSION = 3072

# Elements whose text becomes one chunk each
CHUNK_CLASSES = {"project-card", "workflow-card", "timeline-item", "edu-card", "skills-section", "hero-inner"}
SKIP_TAGS = {"script", "style", "svg"}
SECTION_NAMES = {
    "hero": "Intro",
    "projects": "Live App",
    "agents": "AI Agent",
    "tools": "Tool built with AI",
    "workflow": "AI Workflow",
    "experience": "Experience",
}


class ChunkParser(HTMLParser):
    """Collects text of each CHUNK_CLASSES element, tagged with its enclosing <section id>."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.section = None
        self.stack = []          # tag names currently open inside a chunk
        self.buf = None          # text parts of the chunk being collected
        self.skip_depth = 0
        self.chunks = []         # (section_id, text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "section" and attrs.get("id"):
            self.section = attrs["id"]
        if tag in SKIP_TAGS:
            self.skip_depth += 1
        classes = set((attrs.get("class") or "").split())
        if self.buf is None and classes & CHUNK_CLASSES:
            self.buf, self.stack = [], [tag]
            return
        if self.buf is not None and tag not in {"br", "img", "input", "meta", "link", "path", "line", "polyline", "polygon"}:
            self.stack.append(tag)
        if self.buf is not None and tag in {"div", "li", "p", "br"}:
            self.buf.append("\n")

    def handle_endtag(self, tag):
        if tag in SKIP_TAGS:
            self.skip_depth = max(0, self.skip_depth - 1)
        if self.buf is None:
            return
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        if not self.stack:
            text = re.sub(r"[ \t]+", " ", "".join(self.buf))
            text = "\n".join(line.strip() for line in text.splitlines() if line.strip())
            if text:
                self.chunks.append((self.section, text))
            self.buf = None

    def handle_data(self, data):
        if self.buf is not None and not self.skip_depth:
            self.buf.append(data)


def build_chunks():
    parser = ChunkParser()
    parser.feed(INDEX_HTML.read_text())
    out = []
    for i, (section, text) in enumerate(parser.chunks):
        kind = SECTION_NAMES.get(section, section or "Site")
        title = text.splitlines()[0] if section != "hero" else "About Pin Xiu"
        # Card numbers like "PROJECT — 01" are noise; use the title line instead
        lines = text.splitlines()
        if re.match(r"^(PROJECT|AGENT|TOOL)\s", lines[0]) and len(lines) > 1:
            title = lines[1]
        elif section == "workflow" and len(lines) > 1:   # first line is the category tag
            title = lines[1]
        elif re.match(r"^[A-Z][a-z]{2} \d{4} ", lines[0]) and len(lines) > 1:  # timeline: date, then company
            title = f"{lines[1]} ({lines[0]})"
        slug = re.sub(r"[^a-z0-9]+", "-", f"{section}-{title}".lower()).strip("-")[:80]
        out.append({
            "id": f"{NAMESPACE}__{i:02d}__{slug}",
            "source": f"{kind}: {title}",
            "text": f"{kind}: {title}\n{text}",
        })
    return out


def build_style_chunks():
    """One chunk for the summary and one per '### ' theme of how_i_work.md."""
    if not STYLE_PATH.exists():
        return None
    text = STYLE_PATH.read_text()
    parts = re.split(r"^(?=## Summary|### )", text, flags=re.M)[1:]
    out = []
    for i, part in enumerate(parts):
        title = re.sub(r"^#+\s*(\d+\.\s*)?", "", part.splitlines()[0]).strip()
        body = "\n".join(l for l in part.splitlines()[1:] if l.strip() and not l.startswith("## Themes"))
        slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:60]
        out.append({
            "id": f"{STYLE_NAMESPACE}__{i:02d}__{slug}",
            "source": f"Working style (colleague feedback, GXS Bank 2022-2025): {title}",
            "text": f"Working style, from anonymous colleague feedback at GXS Bank (2022-2025): {title}\n{body}",
        })
    return out


def embed_all(client, types, chunks):
    vectors = []
    for c in chunks:
        emb = client.models.embed_content(
            model=EMBED_MODEL,
            contents=c["text"],
            config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT"),
        ).embeddings[0].values
        vectors.append({"id": c["id"], "values": emb,
                        "metadata": {"source": c["source"], "text": c["text"]}})
        time.sleep(0.3)  # free tier rate limit
    return vectors


def replace_namespace(index, namespace, vectors):
    """Full refresh: wipe the namespace, then upload."""
    if namespace in index.describe_index_stats().namespaces:
        index.delete(delete_all=True, namespace=namespace)
    for i in range(0, len(vectors), 100):
        index.upsert(vectors=vectors[i:i + 100], namespace=namespace)


def main():
    chunks = build_chunks()
    print(f"Built {len(chunks)} chunks from {INDEX_HTML.name}")
    for c in chunks:
        print(f"  {c['id']}  ({len(c['text'])} chars)")
    style = build_style_chunks()
    if style is None:
        print(f"No {STYLE_PATH}; leaving '{STYLE_NAMESPACE}' namespace untouched")
    else:
        print(f"Built {len(style)} working-style chunks from {STYLE_PATH.name}")
        for c in style:
            print(f"  {c['id']}  ({len(c['text'])} chars)")
    if "--dry-run" in sys.argv:
        return

    from google import genai
    from google.genai import types
    from pinecone import Pinecone, ServerlessSpec

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])

    if PINECONE_INDEX not in pc.list_indexes().names():
        pc.create_index(name=PINECONE_INDEX, dimension=DIMENSION, metric="cosine",
                        spec=ServerlessSpec(cloud="aws", region="us-east-1"))
        time.sleep(10)
    index = pc.Index(PINECONE_INDEX)

    replace_namespace(index, NAMESPACE, embed_all(client, types, chunks))
    if style:
        replace_namespace(index, STYLE_NAMESPACE, embed_all(client, types, style))

    time.sleep(5)
    print(index.describe_index_stats())


if __name__ == "__main__":
    main()
