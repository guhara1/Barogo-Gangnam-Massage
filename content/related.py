# 내부링크 강화 — 데이터 기반 "인근 역·지역 안내" 블록.
# 역↔인접역, 역↔대표 행정동, 동↔역세권을 일관되게 상호링크해
# hub-and-spoke 구조와 문맥 링크(contextual internal link)를 보강한다.

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
"""


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
"""
