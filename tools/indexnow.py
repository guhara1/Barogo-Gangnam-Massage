#!/usr/bin/env python3
"""IndexNow 즉시 색인 통보 — 빙(Bing)·네이버(Naver)에 URL을 바로 알린다.

빙, 네이버, 얀덱스, Seznam 등이 IndexNow에 참여한다.
(구글은 IndexNow 미참여 — 구글은 tools/google_indexing.py 또는 Search Console 사용)

사용법:
    python3 tools/indexnow.py                # sitemap.xml 의 모든 URL 통보
    python3 tools/indexnow.py --dry-run      # 보내지 않고 대상만 출력
    python3 tools/indexnow.py URL [URL ...]  # 특정 URL만 통보 (글 1개 올렸을 때)

동작:
  - 사이트 루트의 sitemap.xml 에서 URL 목록을 읽는다(인자가 없으면).
  - 루트의 IndexNow 키 파일({key}.txt)에서 키를 자동으로 찾는다.
  - 빙·네이버 IndexNow 엔드포인트에 JSON 으로 일괄 제출한다.
표준 라이브러리만 사용한다(설치 불필요).
"""
import json
import os
import re
import sys
import urllib.error
import urllib.request
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# IndexNow 참여 엔드포인트 (한 곳에만 보내도 참여 엔진끼리 공유되지만,
# 네이버는 자체 엔드포인트 사용을 권장하므로 둘 다 보낸다.)
ENDPOINTS = [
    ("Bing", "https://www.bing.com/indexnow"),
    ("Naver", "https://searchadvisor.naver.com/indexnow"),
]


def find_key():
    for fn in os.listdir(ROOT):
        if re.fullmatch(r"[0-9a-fA-F]{8,128}\.txt", fn):
            with open(os.path.join(ROOT, fn), encoding="utf-8") as f:
                return fn[:-4], fn
    raise SystemExit("IndexNow 키 파일({hex}.txt)을 찾을 수 없습니다. 먼저 python3 build.py 실행.")


def sitemap_urls():
    p = os.path.join(ROOT, "sitemap.xml")
    if not os.path.exists(p):
        raise SystemExit("sitemap.xml 이 없습니다. 먼저 python3 build.py 실행.")
    return re.findall(r"<loc>(.*?)</loc>", open(p, encoding="utf-8").read())


def submit(host, key, key_loc, urls):
    payload = json.dumps(
        {"host": host, "key": key, "keyLocation": key_loc, "urlList": urls}
    ).encode("utf-8")
    for name, ep in ENDPOINTS:
        req = urllib.request.Request(
            ep, data=payload,
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                print(f"  [{name}] {r.status} {r.reason}  ({len(urls)}건)")
        except urllib.error.HTTPError as e:
            # 200/202 외에도 일부 엔진은 202/200 대신 다른 코드를 줄 수 있다.
            print(f"  [{name}] HTTP {e.code} {e.reason}")
        except Exception as e:  # noqa: BLE001
            print(f"  [{name}] 실패: {e}")


def main(argv):
    dry = "--dry-run" in argv
    args = [a for a in argv if not a.startswith("-")]
    urls = args if args else sitemap_urls()
    if not urls:
        raise SystemExit("통보할 URL이 없습니다.")
    host = urlparse(urls[0]).netloc
    key, keyfn = find_key()
    key_loc = f"https://{host}/{keyfn}"

    print(f"호스트: {host}")
    print(f"키 위치: {key_loc}")
    print(f"URL {len(urls)}건:")
    for u in urls:
        print(f"  - {u}")
    if dry:
        print("\n[dry-run] 실제 전송하지 않았습니다.")
        return
    print("\nIndexNow 제출:")
    submit(host, key, key_loc, urls)
    print("\n완료. (빙·네이버가 키 파일을 확인한 뒤 색인합니다.)")


if __name__ == "__main__":
    main(sys.argv[1:])
