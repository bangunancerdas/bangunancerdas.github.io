"""Metadata, canonical URLs, structured data and indexability."""
import json
import re
import unittest

from tests import site


class PageMetadata(unittest.TestCase):
    def test_document_basics(self):
        for page in site.published_pages():
            if page == "google360f4755a1aefbdb.html":
                continue
            dom = site.load(page)
            with self.subTest(page=page):
                html = dom.find_all("html")[0]
                self.assertEqual(html.attrs.get("lang"), "id")
                self.assertEqual(dom.find_all("meta", charset="UTF-8") and "UTF-8", "UTF-8")
                self.assertIn("width=device-width", dom.meta("viewport") or "")
                self.assertTrue(dom.title)
                self.assertTrue(dom.meta("description"))

    def test_titles_are_unique(self):
        titles = [site.load(p).title for p in site.published_pages() if p != "google360f4755a1aefbdb.html"]
        self.assertEqual(len(titles), len(set(titles)), titles)

    def test_descriptions_are_unique_and_reasonable(self):
        seen = {}
        for page in site.content_pages():
            desc = site.load(page).meta("description")
            with self.subTest(page=page):
                self.assertTrue(50 <= len(desc) <= 175, f"{len(desc)} chars: {desc}")
                self.assertNotIn(desc, seen, f"duplicate of {seen.get(desc)}")
            seen[desc] = page

    def test_exactly_one_h1(self):
        for page in site.published_pages():
            if page == "google360f4755a1aefbdb.html":
                continue
            with self.subTest(page=page):
                self.assertEqual(len(site.load(page).find_all("h1")), 1)

    def test_heading_levels_do_not_skip(self):
        for page in site.published_pages():
            if page == "google360f4755a1aefbdb.html":
                continue
            levels = [int(e.tag[1]) for e in site.load(page).elements if re.fullmatch(r"h[1-6]", e.tag)]
            with self.subTest(page=page):
                for prev, cur in zip(levels, levels[1:]):
                    self.assertLessEqual(cur, prev + 1, f"heading levels {levels}")


class CanonicalAndSocial(unittest.TestCase):
    def test_canonical_matches_the_page_url(self):
        for page in site.content_pages():
            with self.subTest(page=page):
                self.assertEqual(site.load(page).link_rel("canonical"), [site.canonical_url(page)])

    def test_open_graph_is_complete_and_consistent(self):
        for page in site.content_pages():
            dom = site.load(page)
            with self.subTest(page=page):
                for prop in ("og:title", "og:description", "og:type", "og:url", "og:image", "og:locale", "og:site_name"):
                    self.assertTrue(dom.meta(prop, "property"), f"missing {prop}")
                self.assertEqual(dom.meta("og:url", "property"), site.canonical_url(page))
                self.assertTrue(dom.meta("og:image", "property").startswith(site.SITE_URL + "/"))
                self.assertEqual(dom.meta("og:locale", "property"), "id_ID")
                expected_type = "website" if page == "index.html" else "article"
                self.assertEqual(dom.meta("og:type", "property"), expected_type)
                self.assertTrue(dom.meta("twitter:card"))

    def test_og_image_exists_locally(self):
        for page in site.content_pages():
            url = site.load(page).meta("og:image", "property")
            with self.subTest(page=page):
                target, _ = site.resolve_local(page, url)
                self.assertTrue(target.exists(), url)

    def test_pages_declare_favicons(self):
        """Without them browsers request /favicon.ico, which 404s."""
        for page in site.published_pages():
            if page == "google360f4755a1aefbdb.html":
                continue
            with self.subTest(page=page):
                self.assertTrue(site.load(page).link_rel("icon"))


class Indexability(unittest.TestCase):
    def test_content_pages_are_not_noindex(self):
        for page in site.content_pages():
            with self.subTest(page=page):
                self.assertNotIn("noindex", (site.load(page).meta("robots") or "").lower())

    def test_404_is_noindex_without_canonical(self):
        dom = site.load("404.html")
        self.assertIn("noindex", dom.meta("robots"))
        self.assertEqual(dom.link_rel("canonical"), [])

    def test_robots_txt_points_to_the_sitemap_and_does_not_block_the_site(self):
        text = (site.ROOT / "robots.txt").read_text(encoding="utf-8")
        self.assertIn(f"Sitemap: {site.SITE_URL}/sitemap.xml", text)
        self.assertNotRegex(text, r"(?im)^disallow:\s*/\s*$")


class StructuredData(unittest.TestCase):
    def test_json_ld_parses_on_every_page(self):
        for page in site.published_pages():
            with self.subTest(page=page):
                for block in site.load(page).json_ld():
                    self.assertEqual(block["@context"], "https://schema.org")

    def test_home_page_has_one_consistent_local_business(self):
        blocks = site.load("index.html").json_ld()
        self.assertEqual([b["@type"] for b in blocks], ["LocalBusiness"])
        business = blocks[0]
        self.assertEqual(business["name"], "Bangunan Cerdas")
        self.assertEqual(business["url"], site.SITE_URL + "/")
        self.assertEqual(business["telephone"], "+" + site.WHATSAPP_NUMBER)
        for invented in ("address", "openingHours", "openingHoursSpecification", "aggregateRating", "review", "priceRange"):
            self.assertNotIn(invented, business)

    def test_blog_posts_have_matching_blogposting_data(self):
        for page in site.blog_pages():
            dom = site.load(page)
            with self.subTest(page=page):
                blocks = dom.json_ld()
                self.assertEqual([b["@type"] for b in blocks], ["BlogPosting"])
                post = blocks[0]
                self.assertEqual(post["headline"], dom.find_all("h1")[0].text)
                self.assertEqual(post["mainEntityOfPage"]["@id"], site.canonical_url(page))
                self.assertEqual(post["description"], dom.meta("description"))
                self.assertEqual(post["inLanguage"], "id")
                self.assertEqual(post["publisher"]["name"], "Bangunan Cerdas")
                # No dates or authors can be verified from the repository.
                for unverifiable in ("datePublished", "dateModified"):
                    self.assertNotIn(unverifiable, post)


if __name__ == "__main__":
    unittest.main()
