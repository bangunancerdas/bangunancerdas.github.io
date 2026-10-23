"""Every WhatsApp CTA: number, encoding, context, accessibility, tracking hooks."""
import re
import unittest
from urllib.parse import parse_qs, quote, urlsplit

from tests import site

TRACK_EVENTS = {"whatsapp_click", "service_cta_click", "portfolio_click"}


def whatsapp_links(page):
    return [a for a in site.load(page).find_all("a") if site.WA_RE.match(a.attrs.get("href", ""))]


class WhatsAppLinks(unittest.TestCase):
    def test_every_published_content_page_has_a_cta(self):
        for page in site.content_pages() + ["404.html"]:
            with self.subTest(page=page):
                self.assertTrue(whatsapp_links(page))

    def test_number_is_the_verified_e164_number_without_punctuation(self):
        for page in site.published_pages():
            for a in whatsapp_links(page):
                with self.subTest(page=page, href=a.attrs["href"]):
                    path = urlsplit(a.attrs["href"]).path.strip("/")
                    self.assertEqual(path, site.WHATSAPP_NUMBER)
                    self.assertRegex(path, r"^62\d{8,13}$")

    def test_no_legacy_or_placeholder_whatsapp_hosts(self):
        for page in site.published_pages():
            text = (site.ROOT / page).read_text(encoding="utf-8")
            with self.subTest(page=page):
                self.assertNotIn("api.whatsapp.com", text)
                self.assertNotRegex(text, r"wa\.me/(?!%s)" % site.WHATSAPP_NUMBER)

    def test_message_is_strictly_encoded_indonesian_text(self):
        for page in site.published_pages():
            for a in whatsapp_links(page):
                href = a.attrs["href"]
                with self.subTest(page=page, href=href):
                    query = urlsplit(href).query
                    self.assertNotIn(" ", href)
                    params = parse_qs(query, strict_parsing=True)
                    self.assertEqual(list(params), ["text"])
                    text = params["text"][0]
                    self.assertTrue(text.startswith("Halo Bangunan Cerdas"))
                    self.assertEqual(query, "text=" + quote(text, safe=""), "message is not canonically percent-encoded")

    def test_messages_match_their_context(self):
        index = {a.attrs["data-cta-id"]: parse_qs(urlsplit(a.attrs["href"]).query)["text"][0]
                 for a in whatsapp_links("index.html")}
        self.assertRegex(index["hero"], r"(?i)smart home.*smart building")
        self.assertRegex(index["service-smart-device"], r"(?i)smart device")
        self.assertRegex(index["service-home-assistant"], r"Home Assistant")
        self.assertEqual(len(set(index.values())), len(index), "each CTA needs its own contextual message")
        for page in site.blog_pages():
            dom = site.load(page)
            title = dom.find_all("h1")[0].text
            texts = [parse_qs(urlsplit(a.attrs["href"]).query)["text"][0] for a in whatsapp_links(page)]
            with self.subTest(page=page):
                self.assertTrue(any(title in t for t in texts), "blog CTA must mention the article title")

    def test_links_are_accessible_and_safe(self):
        for page in site.published_pages():
            for a in whatsapp_links(page):
                with self.subTest(page=page, href=a.attrs["href"]):
                    self.assertTrue(a.attrs.get("aria-label") or a.text)
                    self.assertEqual(a.attrs.get("target"), "_blank")
                    self.assertTrue({"noopener", "noreferrer"} <= set(a.attrs.get("rel", "").split()))
                    label = (a.attrs.get("aria-label") or a.text).lower()
                    if a.attrs.get("target") == "_blank":
                        self.assertIn("whatsapp", label)

    def test_links_work_without_javascript_handlers(self):
        for page in site.published_pages():
            for a in whatsapp_links(page):
                with self.subTest(page=page, href=a.attrs["href"]):
                    self.assertFalse([k for k in a.attrs if k.startswith("on")])

    def test_links_carry_stable_tracking_attributes(self):
        for page in site.published_pages():
            ids = []
            for a in whatsapp_links(page):
                with self.subTest(page=page, href=a.attrs["href"]):
                    self.assertIn(a.attrs.get("data-track"), TRACK_EVENTS)
                    cta = a.attrs.get("data-cta-id", "")
                    self.assertRegex(cta, r"^[a-z0-9-]{1,40}$")
                    ids.append(cta)
            self.assertEqual(len(ids), len(set(ids)), f"duplicate data-cta-id on {page}")

    def test_visible_number_matches_link(self):
        text = site.load("index.html").root.text
        self.assertIn("+62 896-8085-8462", text)
        self.assertEqual(re.sub(r"\D", "", "+62 896-8085-8462"), site.WHATSAPP_NUMBER)


if __name__ == "__main__":
    unittest.main()
