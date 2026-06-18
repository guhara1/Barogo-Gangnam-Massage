#!/usr/bin/env python3
"""구글 Indexing API 통보 (선택) — 구글은 IndexNow에 참여하지 않으므로 별도 경로.

⚠ 솔직한 한계 고지
  - 구글 Indexing API의 공식 지원 대상은 JobPosting·BroadcastEvent 구조화 페이지뿐입니다.
  - 일반 페이지 URL도 기술적으로는 호출이 통과하지만, 구글이 공식 보장하는 용도는 아닙니다.
  - 일반 사이트의 가장 확실한 구글 색인 경로는 여전히
      (1) Search Console에 sitemap.xml 제출  (2) URL 검사 → 색인 요청 입니다.
  - 이 스크립트는 보조 수단입니다.

준비물
  1) Google Cloud 프로젝트에서 "Indexing API" 사용 설정
  2) 서비스 계정 생성 + JSON 키 다운로드
  3) Search Console 속성에 그 서비스 계정 이메일을 "소유자"로 추가
  4) 의존성 설치:
        pip install google-auth requests

사용법
    GOOGLE_APPLICATION_CREDENTIALS=service_account.json \
        python3 tools/google_indexing.py                 # sitemap 전체
    GOOGLE_APPLICATION_CREDENTIALS=service_account.json \
        python3 tools/google_indexing.py URL [URL ...]    # 특정 URL
    (참고: Indexing API는 프로젝트당 일일 200건 기본 할당량)
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
SCOPES = ["https://www.googleapis.com/auth/indexing"]


def sitemap_urls():
    p = os.path.join(ROOT, "sitemap.xml")
    if not os.path.exists(p):
        raise SystemExit("sitemap.xml 이 없습니다. 먼저 python3 build.py 실행.")
    return re.findall(r"<loc>(.*?)</loc>", open(p, encoding="utf-8").read())


def main(argv):
    cred = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not cred or not os.path.exists(cred):
        raise SystemExit(
            "GOOGLE_APPLICATION_CREDENTIALS 환경변수에 서비스 계정 JSON 경로를 지정하세요."
        )
    try:
        import requests
        from google.oauth2 import service_account
        from google.auth.transport.requests import AuthorizedSession
    except ImportError:
        raise SystemExit("의존성이 없습니다:  pip install google-auth requests")

    args = [a for a in argv if not a.startswith("-")]
    urls = args if args else sitemap_urls()

    creds = service_account.Credentials.from_service_account_file(cred, scopes=SCOPES)
    session = AuthorizedSession(creds)

    ok = 0
    for u in urls:
        r = session.post(ENDPOINT, json={"url": u, "type": "URL_UPDATED"})
        tag = "OK" if r.status_code == 200 else f"HTTP {r.status_code}"
        print(f"  [{tag}] {u}")
        if r.status_code == 200:
            ok += 1
        elif r.status_code == 429:
            print("  ※ 일일 할당량 초과(429) — 내일 다시 시도하세요.")
            break
    print(f"\n완료: {ok}/{len(urls)} 성공.")


if __name__ == "__main__":
    main(sys.argv[1:])
