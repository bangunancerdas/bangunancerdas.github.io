"""sitemap.xml must list exactly the indexable pages."""
import unittest
import xml.etree.ElementTree as ET
from urllib.parse import urlsplit

from tests import site

NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


class Sitemap(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = ET.parse(site.ROOT / "sitemap.xml").getroot()
        cls.locs = [e.text.strip() for e in cls.root.findall("sm:url/sm:loc", NS)]

    def test_namespace_and_root(self):
        self.assertEqual(self.root.tag, "{%s}urlset" % NS["sm"])

    def test_urls_are_public_https_without_fragments_or_duplicates(self):
        self.assertEqual(len(self.locs), len(set(self.locs)))
        for loc in self.locs:
            with self.subTest(loc=loc):
                parts = urlsplit(loc)
                self.assertEqual((parts.scheme, parts.netloc), ("https", "bangunancerdas.github.io"))
                self.assertEqual(parts.fragment, "")
                self.assertEqual(parts.query, "")

    def test_lists_exactly_the_indexable_pages(self):
        expected = {site.canonical_url(p) for p in site.content_pages()}
        self.assertEqual(set(self.locs), expected)

    def test_every_url_maps_to_an_existing_file(self):
        for loc in self.locs:
            with self.subTest(loc=loc):
                target, _ = site.resolve_local("index.html", loc)
                self.assertTrue(target.exists())

    def test_excludes_404_drafts_and_verification_file(self):
        joined = "\n".join(self.locs)
        for forbidden in ("404", ".md", "google360f4755a1aefbdb"):
            self.assertNotIn(forbidden, joined)

    def test_lastmod_is_absent_or_valid_iso_date(self):
        for lastmod in self.root.findall("sm:url/sm:lastmod", NS):
            self.assertRegex(lastmod.text.strip(), r"^\d{4}-\d{2}-\d{2}")


class BlogDiscoverability(unittest.TestCase):
    def test_every_article_is_linked_from_the_home_page(self):
        hrefs = {a.attrs["href"] for a in site.load("index.html").find_all("a") if "href" in a.attrs}
        for page in site.blog_pages():
            with self.subTest(page=page):
                self.assertIn("/" + page, hrefs)

    def test_every_article_has_a_matching_draft_with_the_same_title(self):
        for page in site.blog_pages():
            draft = (site.ROOT / page).with_suffix(".md")
            with self.subTest(page=page):
                self.assertTrue(draft.exists())
                first_line = draft.read_text(encoding="utf-8").splitlines()[0]
                self.assertEqual(first_line, "# " + site.load(page).find_all("h1")[0].text)

    def test_every_article_links_home_and_to_other_articles(self):
        for page in site.blog_pages():
            hrefs = [a.attrs.get("href", "") for a in site.load(page).find_all("a")]
            with self.subTest(page=page):
                self.assertIn("/#blog", hrefs)
                related = [h for h in hrefs if h.startswith("/blog/") and h != "/" + page]
                self.assertGreaterEqual(len(related), 2)
                self.assertIn("/#layanan", hrefs)


if __name__ == "__main__":
    unittest.main()
