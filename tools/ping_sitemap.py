#!/usr/bin/env python3
"""sitemap ping (참고용) — 현실적 한계를 명확히 알려주는 스크립트.

⚠ 중요: 전통적인 sitemap ping은 대부분 폐지되었습니다.
  - 구글: 2023년 6월 sitemap ping 엔드포인트(/ping?sitemap=) 폐지 → 호출해도 404.
  - 빙:   ping 대신 IndexNow 사용을 권장(사실상 폐지 수순).
  => 따라서 "즉시 색인"의 실효 수단은:
       · 빙·네이버:  tools/indexnow.py   (IndexNow, 실제 동작)
       · 구글:        Search Console sitemap 제출 + tools/google_indexing.py(보조)

이 스크립트는 남아있을 수 있는 ping 엔드포인트에 best-effort로 시도하고,
응답 코드를 있는 그대로 보여줍니다(대개 404/410이 정상입니다).

사용법:
    python3 tools/ping_sitemap.py
"""
import os
import re
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sitemap_url():
    p = os.path.join(ROOT, "sitemap.xml")
    locs = re.findall(r"<loc>(.*?)</loc>", open(p, encoding="utf-8").read())
    if not locs:
        raise SystemExit("sitemap.xml URL을 읽을 수 없습니다.")
    netloc = urllib.parse.urlparse(locs[0]).netloc
    return f"https://{netloc}/sitemap.xml"


def main():
    sm = sitemap_url()
    enc = urllib.parse.quote(sm, safe="")
    targets = [
        ("Google(폐지됨)", f"https://www.google.com/ping?sitemap={enc}"),
        ("Bing(폐지 수순)", f"https://www.bing.com/ping?sitemap={enc}"),
    ]
    print(f"sitemap: {sm}\n")
    for name, url in targets:
        try:
            with urllib.request.urlopen(url, timeout=20) as r:
                print(f"  [{name}] {r.status} {r.reason}")
        except urllib.error.HTTPError as e:  # noqa: F821
            print(f"  [{name}] HTTP {e.code} (폐지된 엔드포인트면 정상입니다)")
        except Exception as e:  # noqa: BLE001
            print(f"  [{name}] {e}")
    print(
        "\n권장: 빠른 색인은 tools/indexnow.py(빙·네이버) + "
        "Search Console sitemap 제출(구글)을 사용하세요."
    )


if __name__ == "__main__":
    import urllib.error  # noqa: E402  (HTTPError 참조용)
    main()
