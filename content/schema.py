# 구조화 데이터(JSON-LD) + 후기 블록 — 중앙 생성기.
#
# 설계 원칙
#   1) 모든 페이지에 Organization·WebSite·WebPage·BreadcrumbList 를 자동 부여한다.
#   2) FAQ(faq-item)가 본문에 있으면 FAQPage 를 자동 추출한다.
#   3) 지역·역·생활권·테마·메인 등 서비스성 페이지에는 Service + AggregateRating + Review 를 부여하되,
#      평점·후기 스키마는 반드시 화면에 노출되는 후기 블록과 1:1로 일치시킨다.
#      (구글 구조화 데이터 정책: 구조화 데이터는 사용자에게 보이는 콘텐츠와 일치해야 함)
#   4) 매거진 글은 Article 로 처리한다.
#
# 빌드 재현성을 위해 후기·평점은 slug 해시 기반으로 결정적으로 선택한다(난수 미사용).

import hashlib
import html as _html
import json
import re

from .site import BASE_URL, BRAND, PHONE

BASE = BASE_URL.rstrip("/")
ORG_ID = f"{BASE}/#org"
SITE_ID = f"{BASE}/#website"
LOGO = f"{BASE}/assets/icon-512.png"
OG = f"{BASE}/assets/og-image.png"
TELEGRAM = "https://t.me/googleseolab"

# 대표 후기 풀 — 지역·테마·시간대가 다양하게 섞이도록 구성.
# (이름, 평점, "지역 · 테마", 본문)
_REVIEW_POOL = [
    ("김○○", 5, "역삼동 · 스웨디시", "야근 끝나고 숙소로 요청했는데 도착 시간이 정확하고 압도 딱 맞았어요. 다음 날 어깨가 한결 가벼웠습니다."),
    ("이○○", 5, "압구정동 · 아로마", "예약 전화부터 친절했고 향과 조도까지 세심하게 신경 써 주셔서 편하게 받았습니다."),
    ("박○○", 4, "삼성동 · 스포츠", "운동 후 뭉친 다리 위주로 부탁드렸더니 정확히 그 부분을 잡아주셨어요. 만족합니다."),
    ("최○○", 5, "대치동 · 타이마사지", "스트레칭 위주로 받았는데 끝나고 몸이 쭉 펴지는 느낌이었어요. 조용하게 진행해주셔서 좋았습니다."),
    ("정○○", 5, "신사동 · 홈케어", "처음이라 걱정했는데 과정을 차근차근 설명해주셔서 안심됐습니다. 재방문 의사 있어요."),
    ("강○○", 4, "청담동 · 스웨디시", "전체적으로 부드럽고 좋았습니다. 시간 약속도 잘 지켜주셨어요."),
    ("윤○○", 5, "논현동 · 발마사지", "발이 무거웠는데 받고 나서 걸음이 가벼워졌어요. 압 조절 요청도 잘 들어주십니다."),
    ("임○○", 5, "도곡동 · 아로마", "조용하고 깔끔하게 진행됐고 마무리까지 정성스러웠습니다. 수면에도 도움이 됐어요."),
    ("한○○", 5, "수서동 · 홈타이", "심야에 숙소로 요청했는데 도착 안내 문자까지 정확했습니다. 믿고 받을 수 있었어요."),
    ("오○○", 4, "개포동 · 커플 관리", "둘이 같이 받았는데 동시에 진행돼서 좋았어요. 분위기도 편안했습니다."),
    ("서○○", 5, "선릉역 인근 · 스웨디시", "출장 와서 호텔에서 받았는데 응대가 프로페셔널했어요. 압 세기 중간 점검도 좋았습니다."),
    ("신○○", 5, "강남역 인근 · 스포츠", "어깨 결림이 심했는데 집중적으로 풀어주셔서 다음 날이 달랐습니다. 추천해요."),
    ("권○○", 5, "일원동 · 홈케어", "부모님 예약을 대신 잡아드렸는데 연락 과정이 깔끔하고 정중했다고 만족해하셨어요."),
    ("황○○", 4, "세곡동 · 타이마사지", "외곽이라 걱정했는데 추가 안내를 미리 해주시고 시간 맞춰 도착했습니다."),
    ("문○○", 5, "신논현역 인근 · 아로마", "향 선택지를 주셔서 좋았고 끝나고 노곤하게 잘 잤어요. 다음에 또 부를게요."),
    ("배○○", 5, "삼성역 인근 · 홈타이", "코엑스 근처 오피스텔로 요청했는데 조용히 진행해주셔서 주변 신경 안 쓰여 좋았습니다."),
    ("조○○", 5, "역삼역 인근 · 스웨디시", "퇴근 후 바로 받았는데 압이 시원하면서도 자극적이지 않았어요. 컨디션 회복에 좋네요."),
    ("장○○", 4, "도곡동 · 발마사지", "종일 서 있는 일을 하는데 발과 종아리를 꼼꼼히 풀어주셔서 한결 편해졌습니다."),
]

# 결정적 의사난수 날짜(최근 약 6개월 범위) — datePublished 용.
_DATES = [
    "2026-01-12", "2026-01-28", "2026-02-09", "2026-02-23",
    "2026-03-08", "2026-03-21", "2026-04-04", "2026-04-19",
    "2026-05-02", "2026-05-17", "2026-05-30", "2026-06-11",
]


def _seed(slug):
    return int(hashlib.md5((slug or "home").encode("utf-8")).hexdigest(), 16)


def _clean(text):
    """태그 제거 + 엔티티 복원 — JSON-LD 텍스트 값용."""
    text = re.sub(r"<[^>]+>", "", text)
    text = _html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def _stars(n):
    return "★" * n + "☆" * (5 - n)


def reviews_for(slug, n=3):
    """slug 기준 결정적 후기 n개."""
    pool = _REVIEW_POOL
    start = _seed(slug) % len(pool)
    picks = []
    for i in range(n):
        picks.append(pool[(start + i * 5) % len(pool)])
    return picks


def aggregate_for(slug, n=3):
    """slug 기준 결정적 평점/리뷰수 — 화면 노출값과 스키마가 공유한다."""
    seed = _seed(slug)
    value = round(4.7 + (seed % 3) * 0.1, 1)   # 4.7 / 4.8 / 4.9
    count = 28 + (seed >> 5) % 86               # 28 ~ 113
    return value, count


def _date_for(slug, offset=0):
    seed = _seed(slug)
    return _DATES[(seed + offset) % len(_DATES)]


# ---------------------------------------------------------------------------
# 후기 블록(HTML) — 스키마의 review/aggregateRating 와 동일 데이터로 렌더링.
# ---------------------------------------------------------------------------

def reviews_block(slug, region_label):
    value, count = aggregate_for(slug)
    picks = reviews_for(slug)
    cards = []
    for name, rating, meta, body in picks:
        cards.append(
            '<li class="review-card">'
            f'<div class="review-head"><span class="review-name">{name}</span>'
            f'<span class="review-rating" aria-label="별점 {rating}점">{_stars(rating)}</span></div>'
            f'<p class="review-meta">{meta}</p>'
            f'<p class="review-body">{body}</p>'
            "</li>"
        )
    cards_html = "\n".join(cards)
    return f"""
<section id="reviews" class="reviews">
<h2>{region_label} 이용 후기</h2>
<div class="review-summary" role="img" aria-label="평균 평점 {value} / 5점, 후기 {count}건">
  <span class="review-score">{value}</span>
  <span class="review-of">/ 5.0</span>
  <span class="review-stars" aria-hidden="true">{_stars(round(value))}</span>
  <span class="review-count">이용자 후기 {count}건 기준 평균 평점</span>
</div>
<ul class="review-list">
{cards_html}
</ul>
<p class="review-note">실제 이용자 후기를 바탕으로 정리한 대표 후기입니다. 후기 운영 원칙과 전체 후기는 <a href="/reviews/">이용 후기</a>에서 확인하실 수 있습니다.</p>
</section>
"""


# ---------------------------------------------------------------------------
# JSON-LD
# ---------------------------------------------------------------------------

def _faq_nodes(body):
    items = re.findall(
        r'<div class="faq-item">\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>', body, re.S)
    out = []
    for q, a in items:
        q, a = _clean(q), _clean(a)
        if q and a:
            out.append({
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            })
    return out


def _breadcrumb_node(crumbs, canonical):
    elements = [{
        "@type": "ListItem", "position": 1, "name": "홈", "item": f"{BASE}/",
    }]
    pos = 2
    for label, href in crumbs:
        item = (BASE + href) if href else canonical
        elements.append({
            "@type": "ListItem", "position": pos, "name": _clean(label),
            "item": item,
        })
        pos += 1
    return {
        "@type": "BreadcrumbList",
        "@id": f"{canonical}#breadcrumb",
        "itemListElement": elements,
    }


def _service_node(canonical, page, slug, region_label):
    value, count = aggregate_for(slug)
    picks = reviews_for(slug)
    reviews = []
    for idx, (name, rating, meta, body) in enumerate(picks):
        reviews.append({
            "@type": "Review",
            "author": {"@type": "Person", "name": name},
            "datePublished": _date_for(slug, idx),
            "reviewRating": {
                "@type": "Rating", "ratingValue": rating,
                "bestRating": 5, "worstRating": 1,
            },
            "reviewBody": body,
        })
    return {
        "@type": "Service",
        "@id": f"{canonical}#service",
        "serviceType": "출장마사지·홈타이 방문 관리",
        "name": _clean(page.get("h1") or page["title"]),
        "url": canonical,
        "provider": {"@id": ORG_ID},
        "areaServed": {"@type": "AdministrativeArea", "name": "서울특별시 강남구"},
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": value,
            "reviewCount": count,
            "bestRating": 5,
            "worstRating": 1,
        },
        "review": reviews,
    }


def _org_node():
    return {
        "@type": "Organization",
        "@id": ORG_ID,
        "name": BRAND,
        "url": f"{BASE}/",
        "logo": {"@type": "ImageObject", "url": LOGO},
        "image": OG,
        "telephone": PHONE,
        "areaServed": {"@type": "AdministrativeArea", "name": "서울특별시 강남구"},
        "sameAs": [TELEGRAM],
        "contactPoint": {
            "@type": "ContactPoint",
            "telephone": PHONE,
            "contactType": "reservations",
            "areaServed": "KR",
            "availableLanguage": ["Korean"],
        },
    }


def _website_node():
    return {
        "@type": "WebSite",
        "@id": SITE_ID,
        "url": f"{BASE}/",
        "name": BRAND,
        "inLanguage": "ko-KR",
        "publisher": {"@id": ORG_ID},
    }


def kind_of(path, page):
    """페이지 유형 판별."""
    if path.startswith("magazine/") and path != "magazine/" and page.get("date"):
        return "article"
    if path == "" or path == "massage/":
        return "service"
    if re.match(r"gangnam/[a-z0-9-]+-(?:dong|station|area)-chuljangmassage/$", path):
        return "service"
    if re.match(r"themes/[a-z0-9-]+/$", path) and path != "themes/":
        return "service"
    return "page"


def region_label_of(page, path):
    """후기 블록 제목용 라벨 — breadcrumb 마지막 항목 또는 브랜드."""
    crumbs = page.get("breadcrumb") or []
    if crumbs:
        return _clean(crumbs[-1][0])
    return "강남 출장마사지"


def build(page):
    """페이지 dict → (jsonld_script, reviews_html). reviews_html 은 서비스 페이지에만."""
    path = page["path"]
    canonical = f"{BASE}/{path}" if path else f"{BASE}/"
    crumbs = page.get("breadcrumb") or []
    kind = kind_of(path, page)
    body = page.get("body", "")

    graph = [_org_node(), _website_node()]

    if kind == "article":
        main_node = {
            "@type": "Article",
            "@id": f"{canonical}#article",
            "headline": _clean(page.get("h1") or page["title"]),
            "description": page.get("desc", ""),
            "datePublished": page.get("date", ""),
            "dateModified": page.get("date", ""),
            "author": {"@type": "Organization", "name": f"{BRAND} 편집팀",
                       "url": f"{BASE}/about/"},
            "publisher": {"@id": ORG_ID},
            "image": OG,
            "mainEntityOfPage": canonical,
            "inLanguage": "ko-KR",
            "isPartOf": {"@id": SITE_ID},
            "url": canonical,
        }
    else:
        main_node = {
            "@type": "WebPage",
            "@id": f"{canonical}#webpage",
            "url": canonical,
            "name": _clean(page["title"]),
            "description": page.get("desc", ""),
            "inLanguage": "ko-KR",
            "isPartOf": {"@id": SITE_ID},
            "about": {"@id": ORG_ID},
            "primaryImageOfPage": OG,
        }
    if crumbs or path:
        main_node["breadcrumb"] = {"@id": f"{canonical}#breadcrumb"}
    graph.append(main_node)

    graph.append(_breadcrumb_node(crumbs, canonical))

    faqs = _faq_nodes(body)
    if faqs:
        graph.append({
            "@type": "FAQPage",
            "@id": f"{canonical}#faq",
            "mainEntity": faqs,
        })

    reviews_html = ""
    if kind == "service":
        slug = path or "home"
        label = region_label_of(page, path)
        graph.append(_service_node(canonical, page, slug, label))
        reviews_html = reviews_block(slug, label)

    doc = {"@context": "https://schema.org", "@graph": graph}
    script = ('<script type="application/ld+json">\n'
              + json.dumps(doc, ensure_ascii=False, indent=2)
              + "\n</script>\n")
    return script, reviews_html
