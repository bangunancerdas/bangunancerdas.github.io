"""Shared helpers for the static-site checks (standard library only)."""
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
SITE_URL = "https://bangunancerdas.github.io"
# Number used by every WhatsApp CTA: +62 896-8085-8462 in wa.me format.
WHATSAPP_NUMBER = "6289680858462"
VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "source", "track", "wbr",
}
# Files that are published but are not content pages.
NON_CONTENT_PAGES = {"404.html", "google360f4755a1aefbdb.html"}


def published_pages():
    """Every HTML page that GitHub Pages serves, relative to the repo root."""
    pages = [p for p in ROOT.glob("*.html")] + sorted((ROOT / "blog").glob("*.html"))
    return sorted(p.relative_to(ROOT).as_posix() for p in pages)


def content_pages():
    """Indexable pages: the home page and the blog articles."""
    return [p for p in published_pages() if p not in NON_CONTENT_PAGES]


def blog_pages():
    return [p for p in published_pages() if p.startswith("blog/")]


def canonical_url(page):
    if page == "index.html":
        return SITE_URL + "/"
    return f"{SITE_URL}/{page}"


class Element:
    def __init__(self, tag, attrs, line):
        self.tag = tag
        self.attrs = {k: (v if v is not None else "") for k, v in attrs}
        self.line = line
        self.parent = None
        self.text_parts = []
        self.children = []

    @property
    def text(self):
        parts = list(self.text_parts)
        for child in self.children:
            parts.append(child.text)
        return " ".join(" ".join(parts).split())

    def ancestors(self):
        node = self.parent
        while node is not None:
            yield node
            node = node.parent


class Page(HTMLParser):
    """Light DOM builder that also records structural problems."""

    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.root = Element("#document", [], 0)
        self.stack = [self.root]
        self.elements = []
        self.scripts = []  # (attrs, text)
        self.comments = []
        self.errors = []
        self._script = None
        self.feed((ROOT / path).read_text(encoding="utf-8"))
        self.close()
        for open_el in self.stack[1:]:
            self.errors.append(f"<{open_el.tag}> opened at line {open_el.line} never closed")

    def handle_starttag(self, tag, attrs):
        el = Element(tag, attrs, self.getpos()[0])
        el.parent = self.stack[-1]
        el.parent.children.append(el)
        self.elements.append(el)
        if tag in VOID_TAGS:
            return
        self.stack.append(el)
        if tag == "script":
            self._script = (el, [])

    def handle_startendtag(self, tag, attrs):
        el = Element(tag, attrs, self.getpos()[0])
        el.parent = self.stack[-1]
        el.parent.children.append(el)
        self.elements.append(el)

    def handle_endtag(self, tag):
        if tag in VOID_TAGS:
            return
        if tag == "script" and self._script:
            el, chunks = self._script
            self.scripts.append((el.attrs, "".join(chunks)))
            self._script = None
        if self.stack[-1].tag == tag:
            self.stack.pop()
        else:
            self.errors.append(
                f"unexpected </{tag}> at line {self.getpos()[0]} (open: <{self.stack[-1].tag}>)"
            )

    def handle_data(self, data):
        if self._script:
            self._script[1].append(data)
        else:
            self.stack[-1].text_parts.append(data)

    def handle_comment(self, data):
        self.comments.append(data)

    # --- queries -----------------------------------------------------
    def find_all(self, tag, **attrs):
        return [
            el for el in self.elements
            if el.tag == tag and all(el.attrs.get(k.replace("_", "-")) == v for k, v in attrs.items())
        ]

    def meta(self, key, value="name"):
        for el in self.find_all("meta"):
            if el.attrs.get(value) == key:
                return el.attrs.get("content")
        return None

    def link_rel(self, rel):
        return [el.attrs.get("href") for el in self.find_all("link") if el.attrs.get("rel") == rel]

    @property
    def title(self):
        titles = self.find_all("title")
        return titles[0].text if titles else None

    @property
    def ids(self):
        return [el.attrs["id"] for el in self.elements if "id" in el.attrs]

    def json_ld(self):
        blocks = []
        for attrs, text in self.scripts:
            if attrs.get("type") == "application/ld+json":
                blocks.append(json.loads(text))
        return blocks

    def inline_scripts(self):
        return [t for a, t in self.scripts if "src" not in a and a.get("type") in (None, "")]


_cache = {}


def load(page):
    if page not in _cache:
        _cache[page] = Page(page)
    return _cache[page]


def resolve_local(page, url):
    """Map a link found in `page` to (file Path, fragment); None if external."""
    split = urlsplit(url)
    if split.scheme or split.netloc:
        if split.netloc == "bangunancerdas.github.io" and split.scheme in ("http", "https"):
            path = split.path or "/"
        else:
            return None
    else:
        path = split.path
    fragment = unquote(split.fragment)
    if path == "":
        target = ROOT / page
    elif path.startswith("/"):
        target = ROOT / unquote(path).lstrip("/")
    else:
        target = (ROOT / page).parent / unquote(path)
    if target.is_dir() or path.endswith("/"):
        target = target / "index.html"
    return target.resolve(), fragment


WA_RE = re.compile(r"^https://wa\.me/")
