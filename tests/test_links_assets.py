"""Internal links, fragment identifiers, local assets and placeholder rules."""
import unittest

from tests import site

LINK_ATTRS = (("a", "href"), ("link", "href"), ("script", "src"), ("img", "src"))
REMOTE_PLACEHOLDER_HOSTS = ("images.unsplash.com", "placehold.co", "via.placeholder.com", "picsum.photos")


class InternalLinks(unittest.TestCase):
    def iter_local_refs(self, page):
        dom = site.load(page)
        for tag, attr in LINK_ATTRS:
            for el in dom.find_all(tag):
                url = el.attrs.get(attr)
                if not url:
                    continue
                resolved = site.resolve_local(page, url)
                if resolved is not None:
                    yield tag, url, resolved

    def test_every_local_reference_exists(self):
        for page in site.published_pages():
            for tag, url, (target, _fragment) in self.iter_local_refs(page):
                with self.subTest(page=page, url=url):
                    self.assertTrue(target.exists(), f"{page}: <{tag}> -> {url} does not exist")

    def test_every_fragment_points_to_an_existing_id(self):
        for page in site.published_pages():
            for tag, url, (target, fragment) in self.iter_local_refs(page):
                if tag != "a" or not fragment or target.suffix != ".html":
                    continue
                with self.subTest(page=page, url=url):
                    ids = site.load(target.relative_to(site.ROOT).as_posix()).ids
                    self.assertIn(fragment, ids, f"{page}: {url} has no matching id")

    def test_no_local_references_to_markdown_drafts(self):
        for page in site.published_pages():
            for _tag, url, (target, _f) in self.iter_local_refs(page):
                with self.subTest(page=page, url=url):
                    self.assertNotEqual(target.suffix, ".md", f"{page} links to a draft: {url}")

    def test_no_localhost_references(self):
        for page in site.published_pages():
            text = (site.ROOT / page).read_text(encoding="utf-8")
            with self.subTest(page=page):
                for needle in ("localhost", "127.0.0.1", "0.0.0.0"):
                    self.assertNotIn(needle, text)

    def test_external_targets_blank_links_use_noopener(self):
        for page in site.published_pages():
            for a in site.load(page).find_all("a"):
                if a.attrs.get("target") == "_blank":
                    with self.subTest(page=page, href=a.attrs.get("href")):
                        rel = set(a.attrs.get("rel", "").split())
                        self.assertTrue({"noopener", "noreferrer"} <= rel)


class PlaceholderContent(unittest.TestCase):
    def test_no_remote_placeholder_images(self):
        for page in site.published_pages():
            for img in site.load(page).find_all("img"):
                src = img.attrs.get("src", "")
                with self.subTest(page=page, src=src):
                    for host in REMOTE_PLACEHOLDER_HOSTS:
                        self.assertNotIn(host, src)

    def test_no_todo_comments_in_published_html(self):
        for page in site.published_pages():
            for comment in site.load(page).comments:
                with self.subTest(page=page):
                    self.assertNotRegex(comment, r"(?i)\b(todo|fixme|placeholder)\b")

    def test_portfolio_items_declare_kind_and_stay_honest(self):
        """Portfolio rule: every item is either a real project (with a local
        image) or a labeled concept without outcome claims."""
        dom = site.load("index.html")
        items = [el for el in dom.elements if "portfolio-item" in el.attrs.get("class", "").split()]
        self.assertTrue(items, "portfolio section has no items")
        for item in items:
            kind = item.attrs.get("data-kind")
            title = next((c.text for c in item.children if c.tag == "h3"), "?")
            with self.subTest(item=title):
                self.assertIn(kind, {"project", "concept"})
                descendants = [e for e in dom.elements if item in e.ancestors()]
                images = [e for e in descendants if e.tag == "img"]
                outcomes = [e for e in descendants if "result" in e.attrs.get("class", "").split()]
                if kind == "concept":
                    self.assertIn("konsep", item.text.lower(), "concept items must be labeled as concepts")
                    self.assertFalse(outcomes, "concept items must not claim results")
                    self.assertFalse(images)
                else:
                    self.assertTrue(images, "project items need a real image")
                    for img in images:
                        target, _ = site.resolve_local("index.html", img.attrs["src"])
                        self.assertTrue(target.exists())
                        self.assertTrue(img.attrs.get("alt"))

    def test_no_unsubstantiated_percentage_claims(self):
        text = site.load("index.html").root.text
        self.assertNotRegex(text, r"\d+\s?%", "unverified percentage claim on the home page")


class AssetDimensions(unittest.TestCase):
    def test_images_declare_alt_and_dimensions(self):
        for page in site.published_pages():
            for img in site.load(page).find_all("img"):
                with self.subTest(page=page, src=img.attrs.get("src")):
                    self.assertIn("alt", img.attrs)
                    self.assertTrue(img.attrs.get("width") and img.attrs.get("height"))


if __name__ == "__main__":
    unittest.main()
