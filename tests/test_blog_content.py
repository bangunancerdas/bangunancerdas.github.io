"""Editorial guard rails for blog articles: references, citations, honesty labels."""
import re
import unittest

from tests import site

MIN_BODY_WORDS = 500
MIN_REFERENCES = 3
PERCENT_CLAIM = re.compile(r"\d+(?:[.,]\d+)?\s?(?:%|persen)", re.IGNORECASE)


def descendants(dom, node):
    return [e for e in dom.elements if node in e.ancestors()]


def references(dom):
    sections = [s for s in dom.find_all("section") if "references" in s.attrs.get("class", "").split()]
    return sections[0] if sections else None


class ArticleReferences(unittest.TestCase):
    def test_every_article_has_a_references_section_with_enough_entries(self):
        for page in site.blog_pages():
            dom = site.load(page)
            with self.subTest(page=page):
                section = references(dom)
                self.assertIsNotNone(section, "missing section.references")
                heading = [e for e in descendants(dom, section) if e.tag == "h2"]
                self.assertEqual([h.text for h in heading], ["Referensi"])
                items = [e for e in descendants(dom, section) if e.tag == "li"]
                self.assertGreaterEqual(len(items), MIN_REFERENCES)
                self.assertEqual([i.attrs.get("id") for i in items], [f"ref-{n}" for n in range(1, len(items) + 1)])

    def test_each_reference_links_to_one_https_source_safely(self):
        for page in site.blog_pages():
            dom = site.load(page)
            section = references(dom)
            urls = []
            for item in [e for e in descendants(dom, section) if e.tag == "li"]:
                links = [e for e in descendants(dom, item) if e.tag == "a"]
                with self.subTest(page=page, ref=item.attrs.get("id")):
                    self.assertEqual(len(links), 1)
                    link = links[0]
                    self.assertTrue(link.attrs["href"].startswith("https://"))
                    self.assertFalse(link.text.lower().startswith("http"), "use descriptive link text")
                    self.assertEqual(link.attrs.get("target"), "_blank")
                    self.assertTrue({"noopener", "noreferrer"} <= set(link.attrs.get("rel", "").split()))
                    self.assertIn("Diakses", item.text, "access date missing")
                    urls.append(link.attrs["href"])
            self.assertEqual(len(urls), len(set(urls)), f"duplicate reference URL on {page}")

    def test_citations_point_to_existing_references_and_every_reference_is_cited(self):
        for page in site.blog_pages():
            dom = site.load(page)
            ref_ids = {i.attrs["id"] for i in descendants(dom, references(dom)) if i.tag == "li"}
            cites = [a for a in dom.find_all("a") if "cite" in a.attrs.get("class", "").split()]
            with self.subTest(page=page):
                self.assertTrue(cites, "article has no inline citations")
                for cite in cites:
                    self.assertIn(cite.attrs["href"].lstrip("#"), ref_ids)
                    self.assertTrue(cite.attrs.get("aria-label", "").startswith("Referensi"))
                cited = {c.attrs["href"].lstrip("#") for c in cites}
                self.assertEqual(cited, ref_ids, "uncited references or orphan citations")

    def test_no_raw_urls_in_article_prose(self):
        for page in site.blog_pages():
            dom = site.load(page)
            section = references(dom)
            article = dom.find_all("article")[0]
            prose = [e for e in descendants(dom, article)
                     if e.tag in ("p", "li") and section not in e.ancestors()]
            for el in prose:
                with self.subTest(page=page, line=el.line):
                    self.assertNotRegex(el.text, r"https?://")


class ArticleHonesty(unittest.TestCase):
    def test_percentage_claims_carry_a_citation(self):
        for page in site.blog_pages():
            dom = site.load(page)
            article = dom.find_all("article")[0]
            for el in descendants(dom, article):
                if el.tag not in ("p", "li"):
                    continue
                if any("illustrative" in a.attrs.get("class", "").split() for a in el.ancestors()):
                    continue
                if PERCENT_CLAIM.search(el.text):
                    with self.subTest(page=page, line=el.line):
                        cites = [d for d in descendants(dom, el) if "cite" in d.attrs.get("class", "").split()]
                        self.assertTrue(cites, f"uncited percentage claim: {el.text[:80]}")

    def test_illustrative_examples_are_labeled_as_not_real_projects(self):
        for page in site.blog_pages():
            dom = site.load(page)
            blocks = [e for e in dom.find_all("aside") if "illustrative" in e.attrs.get("class", "").split()]
            for block in blocks:
                with self.subTest(page=page, line=block.line):
                    self.assertIn("bukan proyek nyata", block.text.lower())

    def test_articles_do_not_present_invented_customer_evidence(self):
        for page in site.blog_pages():
            text = site.load(page).find_all("article")[0].text.lower()
            with self.subTest(page=page):
                for phrase in ("testimoni", "klien kami", "pelanggan kami", "proyek kami"):
                    self.assertNotIn(phrase, text)


class ArticleDepth(unittest.TestCase):
    def test_articles_have_a_summary_structure_and_substance(self):
        for page in site.blog_pages():
            dom = site.load(page)
            article = dom.find_all("article")[0]
            outside = ("references", "article-more", "article-cta")
            body = [e for e in descendants(dom, article) if e.tag in ("p", "li", "h2")
                    and not any(set(a.attrs.get("class", "").split()) & set(outside) for a in e.ancestors())]
            body_words = len(" ".join(e.text for e in body if e.tag != "li" or e.parent.tag in ("ul", "ol")).split())
            with self.subTest(page=page):
                self.assertTrue([p for p in dom.find_all("p") if "summary" in p.attrs.get("class", "").split()])
                self.assertGreaterEqual(len([h for h in dom.find_all("h2")]), 4)
                self.assertGreaterEqual(body_words, MIN_BODY_WORDS)


if __name__ == "__main__":
    unittest.main()
