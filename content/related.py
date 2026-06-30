# 내부링크 강화 — 데이터 기반 "인근 역·지역 안내" 블록 + 롱테일 추천 링크.
# 역↔인접역, 역↔대표 행정동, 동↔역세권을 일관되게 상호링크해
# hub-and-spoke 구조와 문맥 링크(contextual internal link)를 보강하고,
# 추가로 지역×테마 롱테일 주제 링크를 결정적으로(slug 해시) 노출한다.
import hashlib

STATION_NAME = {
    "gangnam-station": "강남역", "sinnonhyeon-station": "신논현역", "nonhyeon-station": "논현역",
    "sinsa-station": "신사역", "apgujeong-station": "압구정역", "apgujeong-rodeo-station": "압구정로데오역",
    "cheongdam-station": "청담역", "gangnam-gu-office-station": "강남구청역", "hakdong-station": "학동역",
    "eonju-station": "언주역", "seonjeongneung-station": "선정릉역", "seolleung-station": "선릉역",
    "yeoksam-station": "역삼역", "samseong-station": "삼성역", "samseong-jungang-station": "삼성중앙역",
    "bongeunsa-station": "봉은사역", "hanti-station": "한티역", "daechi-station": "대치역",
    "hangnyeoul-station": "학여울역", "dogok-station": "도곡역", "maebong-station": "매봉역",
    "guryong-station": "구룡역", "gaepodong-station": "개포동역", "daemosan-station": "대모산입구역",
    "daecheong-station": "대청역", "irwon-station": "일원역", "suseo-station": "수서역",
}

DONG_NAME = {
    "sinsa-dong": "신사동", "apgujeong-dong": "압구정동", "cheongdam-dong": "청담동",
    "nonhyeon-dong": "논현동", "samseong-dong": "삼성동", "yeoksam-dong": "역삼동",
    "daechi-dong": "대치동", "dogok-dong": "도곡동", "gaepo-dong": "개포동",
    "irwon-dong": "일원동", "suseo-dong": "수서동", "segok-dong": "세곡동",
}

AREA_NAME = {
    "gangnam-station-area": "강남역 생활권", "teheran-ro-area": "테헤란로 업무지구",
    "coex-samseong-area": "삼성역·코엑스 생활권", "cheongdam-apgujeong-area": "청담·압구정 생활권",
    "nonhyeon-hakdong-area": "논현·학동 생활권", "daechi-academy-area": "대치동 학원가",
    "dogok-gaepo-area": "도곡·개포 생활권", "suseo-area": "수서역 생활권",
    "segok-jagok-area": "세곡·자곡 생활권",
}

# 역 -> (대표 행정동, 생활권, [인접 역 3])
STATION_REL = {
    "gangnam-station": ("yeoksam-dong", "gangnam-station-area", ["sinnonhyeon-station", "yeoksam-station", "seolleung-station"]),
    "sinnonhyeon-station": ("nonhyeon-dong", "gangnam-station-area", ["gangnam-station", "nonhyeon-station", "eonju-station"]),
    "nonhyeon-station": ("nonhyeon-dong", "nonhyeon-hakdong-area", ["sinnonhyeon-station", "hakdong-station", "eonju-station"]),
    "sinsa-station": ("sinsa-dong", "cheongdam-apgujeong-area", ["apgujeong-station", "nonhyeon-station", "sinnonhyeon-station"]),
    "apgujeong-station": ("apgujeong-dong", "cheongdam-apgujeong-area", ["sinsa-station", "apgujeong-rodeo-station", "cheongdam-station"]),
    "apgujeong-rodeo-station": ("apgujeong-dong", "cheongdam-apgujeong-area", ["apgujeong-station", "cheongdam-station", "gangnam-gu-office-station"]),
    "cheongdam-station": ("cheongdam-dong", "cheongdam-apgujeong-area", ["apgujeong-rodeo-station", "gangnam-gu-office-station", "bongeunsa-station"]),
    "gangnam-gu-office-station": ("cheongdam-dong", "cheongdam-apgujeong-area", ["cheongdam-station", "hakdong-station", "seonjeongneung-station"]),
    "hakdong-station": ("nonhyeon-dong", "nonhyeon-hakdong-area", ["nonhyeon-station", "gangnam-gu-office-station", "eonju-station"]),
    "eonju-station": ("nonhyeon-dong", "nonhyeon-hakdong-area", ["sinnonhyeon-station", "seonjeongneung-station", "yeoksam-station"]),
    "seonjeongneung-station": ("samseong-dong", "teheran-ro-area", ["seolleung-station", "gangnam-gu-office-station", "samseong-jungang-station"]),
    "seolleung-station": ("yeoksam-dong", "teheran-ro-area", ["yeoksam-station", "samseong-station", "seonjeongneung-station"]),
    "yeoksam-station": ("yeoksam-dong", "teheran-ro-area", ["gangnam-station", "seolleung-station", "eonju-station"]),
    "samseong-station": ("samseong-dong", "coex-samseong-area", ["seolleung-station", "samseong-jungang-station", "bongeunsa-station"]),
    "samseong-jungang-station": ("samseong-dong", "coex-samseong-area", ["samseong-station", "bongeunsa-station", "seonjeongneung-station"]),
    "bongeunsa-station": ("samseong-dong", "coex-samseong-area", ["samseong-station", "samseong-jungang-station", "cheongdam-station"]),
    "hanti-station": ("daechi-dong", "daechi-academy-area", ["seolleung-station", "dogok-station", "daechi-station"]),
    "daechi-station": ("daechi-dong", "daechi-academy-area", ["hanti-station", "hangnyeoul-station", "daecheong-station"]),
    "hangnyeoul-station": ("daechi-dong", "daechi-academy-area", ["daechi-station", "daecheong-station", "gaepodong-station"]),
    "dogok-station": ("dogok-dong", "dogok-gaepo-area", ["hanti-station", "maebong-station", "guryong-station"]),
    "maebong-station": ("dogok-dong", "dogok-gaepo-area", ["dogok-station", "guryong-station", "hanti-station"]),
    "guryong-station": ("gaepo-dong", "dogok-gaepo-area", ["maebong-station", "gaepodong-station", "dogok-station"]),
    "gaepodong-station": ("gaepo-dong", "dogok-gaepo-area", ["guryong-station", "daemosan-station", "hangnyeoul-station"]),
    "daemosan-station": ("gaepo-dong", "dogok-gaepo-area", ["gaepodong-station", "irwon-station", "daecheong-station"]),
    "daecheong-station": ("irwon-dong", "suseo-area", ["irwon-station", "hangnyeoul-station", "daechi-station"]),
    "irwon-station": ("irwon-dong", "suseo-area", ["daecheong-station", "suseo-station", "daemosan-station"]),
    "suseo-station": ("suseo-dong", "suseo-area", ["irwon-station", "daemosan-station", "daecheong-station"]),
}

# 대표 행정동 -> (생활권, [대표 역세권])
DONG_AREA = {
    "sinsa-dong": "cheongdam-apgujeong-area", "apgujeong-dong": "cheongdam-apgujeong-area",
    "cheongdam-dong": "cheongdam-apgujeong-area", "nonhyeon-dong": "nonhyeon-hakdong-area",
    "samseong-dong": "coex-samseong-area", "yeoksam-dong": "teheran-ro-area",
    "daechi-dong": "daechi-academy-area", "dogok-dong": "dogok-gaepo-area",
    "gaepo-dong": "dogok-gaepo-area", "irwon-dong": "suseo-area",
    "suseo-dong": "suseo-area", "segok-dong": "segok-jagok-area",
}
DONG_STATIONS = {
    "sinsa-dong": ["sinsa-station"],
    "apgujeong-dong": ["apgujeong-station", "apgujeong-rodeo-station"],
    "cheongdam-dong": ["cheongdam-station", "gangnam-gu-office-station"],
    "nonhyeon-dong": ["nonhyeon-station", "sinnonhyeon-station", "hakdong-station", "eonju-station"],
    "samseong-dong": ["samseong-station", "samseong-jungang-station", "bongeunsa-station", "seonjeongneung-station"],
    "yeoksam-dong": ["gangnam-station", "yeoksam-station", "seolleung-station"],
    "daechi-dong": ["daechi-station", "hanti-station", "hangnyeoul-station"],
    "dogok-dong": ["dogok-station", "maebong-station", "hanti-station"],
    "gaepo-dong": ["gaepodong-station", "guryong-station", "daemosan-station"],
    "irwon-dong": ["irwon-station", "daecheong-station", "daemosan-station"],
    "suseo-dong": ["suseo-station"],
    "segok-dong": ["suseo-station"],
}


def _st_href(slug):
    return f"/gangnam/{slug}-chuljangmassage/"


def _dong_href(slug):
    return f"/gangnam/{slug}-chuljangmassage/"


def _area_href(slug):
    return f"/gangnam/{slug}-chuljangmassage/"


def station_related_html(slug):
    """역 페이지 하단 '인근 역·지역 안내' 블록."""
    rel = STATION_REL.get(slug)
    if not rel:
        return ""
    dong, area, near = rel
    name = STATION_NAME[slug]
    items = [
        f'<li><a href="{_dong_href(dong)}">{DONG_NAME[dong]} 출장마사지</a></li>',
        f'<li><a href="{_area_href(area)}">{AREA_NAME[area]}</a></li>',
    ]
    for n in near:
        items.append(f'<li><a href="{_st_href(n)}">{STATION_NAME[n]} 출장마사지</a></li>')
    lis = "\n".join(items)
    return f"""
<section class="related">
<h2>{name} 인근 역·지역 안내</h2>
<p>{name}과 가까운 대표 행정동·생활권과 인접 역세권을 함께 정리했습니다. 본인 위치에 더 가까운 페이지에서 방문 가능 지역과 예약 기준을 확인하실 수 있습니다.</p>
<ul class="card-grid">
{lis}
</ul>
</section>
""" + longtail_block(name, slug)


def dong_related_html(slug):
    """대표 행정동 페이지 하단 '대표 역세권·생활권 안내' 블록."""
    if slug not in DONG_STATIONS:
        return ""
    name = DONG_NAME[slug]
    area = DONG_AREA[slug]
    sts = DONG_STATIONS[slug]
    items = [f'<li><a href="{_area_href(area)}">{AREA_NAME[area]}</a></li>']
    seen = set()
    for s in sts:
        if s in seen:
            continue
        seen.add(s)
        items.append(f'<li><a href="{_st_href(s)}">{STATION_NAME[s]} 출장마사지</a></li>')
    lis = "\n".join(items)
    return f"""
<section class="related">
<h2>{name} 대표 역세권·생활권 안내</h2>
<p>{name}과 연결되는 대표 역세권과 생활권 페이지입니다. 가까운 역이나 생활권 기준으로도 방문 가능 지역과 예약 안내를 확인하실 수 있습니다.</p>
<ul class="card-grid">
{lis}
</ul>
</section>
""" + longtail_block(name, slug)


# ---------------------------------------------------------------------------
# 롱테일 추천 링크 — 지역×테마, 매거진, 안내 페이지로 문맥 링크를 넓힌다.
# ---------------------------------------------------------------------------

THEME_NAME = {
    "swedish": "스웨디시", "lomilomi": "로미로미", "thai": "타이마사지",
    "chinese": "중국마사지", "aroma": "아로마테라피", "homecare": "홈케어",
    "hotel-style": "호텔식마사지", "foot": "발마사지", "sports": "스포츠·경락",
    "skincare": "스킨케어", "waxing": "왁싱", "couple": "커플 관리",
    "24hours": "24시간", "overnight": "수면 가능",
}
THEME_DESC = {
    "swedish": "오일을 사용한 부드러운 전신 이완 관리",
    "aroma": "향과 호흡으로 긴장을 푸는 관리",
    "thai": "스트레칭 중심의 시원한 이완",
    "sports": "운동 후 근육 회복·경락 관리",
    "foot": "발·종아리 집중 피로 회복",
    "homecare": "방문 환경 맞춤 케어",
    "hotel-style": "호텔·숙소 방문에 맞춘 관리",
    "24hours": "심야·새벽까지 가능한 방문 관리",
    "overnight": "관리 후 수면까지 이어지는 코스",
    "couple": "두 분이 함께 받는 동시 진행",
}
_THEME_ROTATION = ["swedish", "aroma", "thai", "sports", "foot",
                   "homecare", "hotel-style", "24hours", "overnight", "couple"]

# 롱테일 매거진 링크 풀(읽을거리)
_MAG_POOL = [
    ("/magazine/swedish-vs-thai/", "스웨디시와 타이마사지, 뭘 고를까", "테마 선택 가이드"),
    ("/magazine/first-time-guide/", "처음 이용 가이드", "예약부터 마무리까지"),
    ("/magazine/sleep-and-massage/", "수면과 마사지", "잠이 안 올 때 읽기"),
    ("/magazine/post-workout-timing/", "운동 후 회복 타이밍", "언제 받는 게 좋을까"),
    ("/magazine/neck-shoulder-care/", "어깨·목 결림 관리", "거북목·결림 완화"),
]


def _seed(s):
    return int(hashlib.md5(s.encode("utf-8")).hexdigest(), 16)


def _theme_picks(slug, k=3):
    seed = _seed(slug)
    out = []
    for i in range(k):
        out.append(_THEME_ROTATION[(seed + i * 3) % len(_THEME_ROTATION)])
    # 중복 제거(순서 유지)
    seen, uniq = set(), []
    for t in out:
        if t not in seen:
            seen.add(t)
            uniq.append(t)
    return uniq


def _mag_pick(slug):
    return _MAG_POOL[_seed(slug) % len(_MAG_POOL)]


def longtail_block(name, slug):
    """지역/역/생활권 페이지용 롱테일 추천 링크(지역×테마 + 읽을거리 + 예약)."""
    items = []
    for t in _theme_picks(slug):
        items.append(
            f'<li><a href="/themes/{t}/">{name} {THEME_NAME[t]} 출장마사지'
            f'<span>{THEME_DESC.get(t, "방문 관리 테마 안내")}</span></a></li>'
        )
    mag_href, mag_t, mag_s = _mag_pick(slug)
    items.append(f'<li><a href="{mag_href}">{mag_t}<span>{mag_s}</span></a></li>')
    items.append(
        f'<li><a href="/reservation/">{name} 출장마사지 예약 방법'
        f'<span>예약 가능 시간·방문 장소·결제 안내</span></a></li>'
    )
    lis = "\n".join(items)
    return f"""
<section class="longtail">
<h2>{name}에서 자주 찾는 주제</h2>
<p>{name} 인근에서 많이 찾는 관리 테마와 예약 정보를 주제별로 모았습니다. 받고 싶은 관리를 먼저 고른 뒤 위치와 시간을 알려주시면 가능 여부를 바로 확인해 드립니다.</p>
<ul class="lt-grid">
{lis}
</ul>
</section>
"""


def area_related_html(slug):
    """생활권 페이지 하단 — 소속 대표 동·역세권 안내 + 롱테일."""
    if slug not in AREA_NAME:
        return ""
    name = AREA_NAME[slug]
    dongs = [d for d, a in DONG_AREA.items() if a == slug]
    stations = [s for s, (d, a, n) in STATION_REL.items() if a == slug]
    items = []
    for d in dongs:
        items.append(f'<li><a href="{_dong_href(d)}">{DONG_NAME[d]} 출장마사지</a></li>')
    for s in stations[:5]:
        items.append(f'<li><a href="{_st_href(s)}">{STATION_NAME[s]} 출장마사지</a></li>')
    lis = "\n".join(items)
    block = f"""
<section class="related">
<h2>{name} 대표 동·역세권 안내</h2>
<p>{name}에 속한 대표 행정동과 인근 역세권 페이지입니다. 가까운 동이나 역 기준으로도 방문 가능 지역과 예약 안내를 확인하실 수 있습니다.</p>
<ul class="card-grid">
{lis}
</ul>
</section>
"""
    return block + longtail_block(name, "area-" + slug)


def theme_related_html(slug, name):
    """테마 페이지 하단 — 다른 테마 + 지역×테마 롱테일."""
    others = [t for t in _THEME_ROTATION if t != slug]
    seed = _seed("theme-" + slug)
    picks = [others[(seed + i) % len(others)] for i in range(4)]
    seen, uniq = set(), []
    for t in picks:
        if t not in seen:
            seen.add(t)
            uniq.append(t)
    theme_items = "\n".join(
        f'<li><a href="/themes/{t}/">{THEME_NAME[t]}</a></li>' for t in uniq
    )
    # 지역×테마 롱테일(대표 지역 3곳)
    regions = [
        ("/gangnam/gangnam-station-chuljangmassage/", "강남역"),
        ("/gangnam/yeoksam-dong-chuljangmassage/", "역삼동"),
        ("/gangnam/apgujeong-dong-chuljangmassage/", "압구정동"),
        ("/gangnam/cheongdam-dong-chuljangmassage/", "청담동"),
        ("/gangnam/samseong-station-chuljangmassage/", "삼성역"),
        ("/gangnam/sinsa-dong-chuljangmassage/", "신사동"),
    ]
    rpick = [regions[(seed + i) % len(regions)] for i in range(3)]
    rseen, runiq = set(), []
    for href, rname in rpick:
        if href not in rseen:
            rseen.add(href)
            runiq.append((href, rname))
    lt_items = "\n".join(
        f'<li><a href="{href}">{rname} {name} 출장마사지'
        f'<span>{rname} 인근 방문 가능 지역 안내</span></a></li>'
        for href, rname in runiq
    )
    mag_href, mag_t, mag_s = _mag_pick("theme-" + slug)
    lt_items += f'\n<li><a href="{mag_href}">{mag_t}<span>{mag_s}</span></a></li>'
    return f"""
<section class="related">
<h2>다른 테마와 함께 보기</h2>
<p>{name} 외에도 상황에 따라 어울리는 관리가 다릅니다. 아래 테마 안내를 함께 비교해 보세요.</p>
<ul class="card-grid">
{theme_items}
</ul>
</section>
<section class="longtail">
<h2>지역별 {name} 안내</h2>
<p>{name}는 지역과 무관하게 방문 가능합니다. 대표 지역 안내에서 본인 위치 기준 예약 정보를 확인하실 수 있습니다.</p>
<ul class="lt-grid">
{lt_items}
</ul>
</section>
"""
