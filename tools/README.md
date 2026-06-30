# 색인(인덱싱) 도구

빌드(`python3 build.py`)가 생성하는 색인 관련 산출물:

| 파일 | 용도 |
|---|---|
| `sitemap.xml` | 전 색인 페이지 + `<lastmod>` (구글·빙·네이버 공통) |
| `rss.xml` | 매거진 글 RSS 피드 (빠른 발견·구독) |
| `robots.txt` | 모든 봇 허용 + sitemap·rss 위치 안내 |
| `{key}.txt` | IndexNow 키 파일 (사이트 루트에 호스팅되어야 함) |

> 위 파일들은 모두 저장소에 커밋되어 배포 시 도메인 루트에서 서빙됩니다.
> 도메인이 바뀌면 `content/site.py`의 `BASE_URL`을 고치고 다시 빌드하세요.

---

## 1. 가장 빠른 즉시 색인 — IndexNow (빙·네이버)

빙·네이버·얀덱스 등은 **IndexNow**를 지원해, 알리는 즉시 색인 큐에 들어갑니다.
(구글은 IndexNow 미참여 → 아래 3번 참고)

```bash
# 전체 일괄 통보 (최초 배포 직후 1회)
python3 tools/indexnow.py

# 글/페이지 하나만 올렸을 때 — 그 URL만 즉시 통보
python3 tools/indexnow.py https://barogo-gangnam-massage.netlify.app/magazine/새글/

# 실제 전송 없이 대상만 확인
python3 tools/indexnow.py --dry-run
```

전제: 키 파일(`{key}.txt`)이 **배포된 도메인 루트에서 실제로 열려야** 합니다.
배포 후 `https://<도메인>/8f4b2e1a9c7d4e63b05f8a1c2d6e9f30.txt` 가 열리는지 먼저 확인하세요.

**글 올릴 때마다 자동 통보**하려면 배포 파이프라인 마지막에
`python3 tools/indexnow.py` 한 줄을 추가하면 됩니다.
(예: GitHub Actions 배포 잡 끝, 또는 로컬 배포 스크립트 끝)

---

## 2. 네이버 — 서치어드바이저

- IndexNow(`tools/indexnow.py`)가 네이버 엔드포인트로도 보냅니다.
- 추가로 **서치어드바이저**(searchadvisor.naver.com)에 사이트 등록 →
  `sitemap.xml`, `rss.xml` 제출 + 사이트 소유확인(메인 `<head>`의
  `naver-site-verification` 메타 이미 적용됨)을 하면 가장 안정적입니다.

---

## 3. 구글 — 색인 경로

구글은 IndexNow에 참여하지 않습니다. 확실한 순서:

1. **Search Console**에 도메인 등록 → `sitemap.xml` 제출 (가장 중요)
2. 새 글은 **URL 검사 → 색인 요청** 으로 개별 푸시
3. (보조) **Indexing API** 자동화 — `tools/google_indexing.py`
   - ⚠ 공식 지원 대상은 JobPosting·BroadcastEvent 뿐이라 일반 페이지엔 보조 수단입니다.
   - 준비: GCP에서 Indexing API 사용 설정 → 서비스 계정 JSON → 그 계정을
     Search Console 속성 소유자로 추가 → `pip install google-auth requests`
   ```bash
   GOOGLE_APPLICATION_CREDENTIALS=service_account.json \
       python3 tools/google_indexing.py
   ```

---

## 4. sitemap ping (참고 — 대부분 폐지)

```bash
python3 tools/ping_sitemap.py
```

- 구글 ping 엔드포인트는 2023년 폐지(404), 빙도 IndexNow로 대체됐습니다.
- 이 스크립트는 best-effort로 시도하고 응답을 그대로 보여줄 뿐입니다.
- **즉시 색인의 실효 수단은 IndexNow(1번) + Search Console(3번)** 입니다.

---

## 배포 후 체크리스트

1. `https://<도메인>/{key}.txt` 열리는지 확인 (IndexNow 전제)
2. `https://<도메인>/sitemap.xml`, `/rss.xml`, `/robots.txt` 확인
3. `python3 tools/indexnow.py` 1회 실행 (빙·네이버 일괄 통보)
4. 구글 Search Console·네이버 서치어드바이저에 sitemap·rss 제출
5. 이후 글 올릴 때마다 `python3 tools/indexnow.py <URL>`
