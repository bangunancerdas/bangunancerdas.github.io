"""Structural sanity beyond what the HTML parser tolerates.

This is NOT a substitute for the Nu HTML Checker, which CI runs separately.
"""
import unittest

from tests import site


class HtmlStructure(unittest.TestCase):
    def test_tags_are_balanced(self):
        for page in site.published_pages():
            with self.subTest(page=page):
                self.assertEqual(site.load(page).errors, [])

    def test_ids_are_unique(self):
        for page in site.published_pages():
            ids = site.load(page).ids
            with self.subTest(page=page):
                self.assertEqual(len(ids), len(set(ids)))

    def test_no_inline_event_handlers_or_javascript_urls(self):
        for page in site.published_pages():
            for el in site.load(page).elements:
                with self.subTest(page=page, tag=el.tag, line=el.line):
                    self.assertFalse([k for k in el.attrs if k.startswith("on")])
                    self.assertFalse(el.attrs.get("href", "").lower().startswith("javascript:"))

    def test_external_scripts_come_only_from_this_site(self):
        for page in site.published_pages():
            for attrs, _text in site.load(page).scripts:
                src = attrs.get("src")
                with self.subTest(page=page, src=src):
                    if src:
                        self.assertTrue(src.startswith("/"), "third-party script found")

    def test_one_main_landmark_and_labelled_navigation(self):
        for page in site.published_pages():
            if page == "google360f4755a1aefbdb.html":
                continue
            dom = site.load(page)
            with self.subTest(page=page):
                self.assertEqual(len(dom.find_all("main")), 1)
                for nav in dom.find_all("nav"):
                    self.assertTrue(nav.attrs.get("aria-label"))

    def test_theme_toggle_has_an_accessible_name(self):
        for page in site.published_pages():
            if page == "google360f4755a1aefbdb.html":
                continue
            with self.subTest(page=page):
                toggle = site.load(page).find_all("button", id="theme-toggle")
                self.assertEqual(len(toggle), 1)
                self.assertTrue(toggle[0].attrs.get("aria-label"))


class ResponsiveCss(unittest.TestCase):
    """Static guard rails; real viewport checks need a browser (see README)."""

    @classmethod
    def setUpClass(cls):
        cls.css = (site.ROOT / "styles.css").read_text(encoding="utf-8")

    def test_mobile_navigation_is_not_removed(self):
        import re
        mobile_blocks = re.findall(r"@media\s*\(max-width:\s*\d+px\)\s*\{(.*?)\n\}", self.css, re.S)
        self.assertTrue(mobile_blocks)
        for block in mobile_blocks:
            self.assertNotRegex(block, r"nav\s*\{\s*display:\s*none")

    def test_focus_indicator_and_reduced_motion_are_defined(self):
        self.assertIn(":focus-visible", self.css)
        self.assertIn("prefers-reduced-motion", self.css)

    def test_logo_is_visible_without_javascript(self):
        self.assertIn(".no-js .logo-light", self.css)


if __name__ == "__main__":
    unittest.main()
