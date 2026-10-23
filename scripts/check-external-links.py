#!/usr/bin/env python3
"""Manual check that blog reference links still resolve. Not part of CI (network-dependent).

Exit code 1 only for links that are genuinely broken (404/410 or unresolvable host).
Anti-bot responses (403/429), server errors and timeouts are reported as UNVERIFIED after retries.
"""
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = "Mozilla/5.0 (X11; Linux x86_64) Chrome/120 (link check for bangunancerdas.github.io)"
RETRIES, TIMEOUT = 3, 25


def reference_urls():
    urls = {}
    for page in sorted((ROOT / "blog").glob("*.html")):
        section = re.search(r'<section class="references".*?</section>', page.read_text(encoding="utf-8"), re.S)
        for url in re.findall(r'<a href="(https://[^"]+)"', section.group(0) if section else ""):
            urls.setdefault(url.replace("&amp;", "&"), []).append(page.name)
    return urls


def probe(url):
    last = "no attempt"
    for attempt in range(RETRIES):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                return "OK", resp.status
        except urllib.error.HTTPError as err:
            if err.code in (404, 410):
                return "BROKEN", err.code
            last = f"HTTP {err.code}"
        except urllib.error.URLError as err:
            last = f"network: {err.reason}"
        except TimeoutError:
            last = "timeout"
        time.sleep(2 * (attempt + 1))
    return "UNVERIFIED", last


def main():
    urls = reference_urls()
    results = {url: probe(url) for url in urls}
    for url, (status, detail) in results.items():
        print(f"{status:10} {detail!s:12} {url}")
    return 1 if any(s == "BROKEN" for s, _ in results.values()) else 0


if __name__ == "__main__":
    sys.exit(main())
