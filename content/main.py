# 메인 페이지 — 허브 역할. 모든 키워드를 밀어 넣지 않고 상세 페이지로 연결한다.
# 스키마: WebPage + BreadcrumbList + Organization + FAQPage.
# 오프라인 사업장 주소가 없는 방문형 사이트이므로 LocalBusiness Schema는 사용하지 않는다.
from .site import BASE_URL, BRAND, PHONE, PHONE_DISPLAY
from .pricing import PRICING

_JSONLD = f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "강남 출장마사지·홈타이 지역별 예약 안내",
  "url": "{BASE_URL}/",
  "description": "강남구 전지역 방문 출장마사지·홈타이 예약 안내",
  "inLanguage": "ko-KR",
  "publisher": {{
    "@type": "Organization",
    "name": "{BRAND}",
    "telephone": "{PHONE}",
    "url": "{BASE_URL}/",
    "logo": "{BASE_URL}/assets/icon-512.png",
    "image": "{BASE_URL}/assets/og-image.png",
    "areaServed": {{
      "@type": "AdministrativeArea",
      "name": "서울특별시 강남구"
    }}
  }}
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{
      "@type": "ListItem",
      "position": 1,
      "name": "홈",
      "item": "{BASE_URL}/"
    }}
  ]
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {{
      "@type": "Question",
      "name": "강남구 전지역 방문이 가능한가요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "예약 시간, 정확한 위치, 배정 상황에 따라 가능 여부가 달라집니다. 지역별 안내에서 신사·압구정·청담·논현·삼성·역삼·대치·도곡·개포·일원·수서·세곡동 기준으로 확인할 수 있습니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "강남역이나 선릉역 근처도 가능한가요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "강남역·역삼역·선릉역·삼성역 등 주요 역세권은 역 상세 페이지에서 주변 생활권과 함께 안내합니다. 정확한 가능 여부는 예약 시 위치를 기준으로 확인합니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "논현1동과 논현2동은 왜 따로 없나요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "논현1·2동은 논현동, 삼성1·2동은 삼성동, 개포1~4동은 개포동처럼 번호 행정동은 대표 동 페이지에서 통합 안내하여 중복 페이지 위험을 줄입니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "환승역은 호선별로 페이지가 다른가요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "아니요. 강남역, 선릉역, 수서역 같은 환승역도 역명 기준 1개 페이지만 운영합니다. 노선별·출구별 페이지는 만들지 않습니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "강남 홈타이는 어떻게 예약하나요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "자택, 숙소, 사무실 인근 방문 가능 여부를 먼저 확인한 뒤 위치와 희망 시간을 알려주시면 됩니다. 예약 전화로 가장 빠르게 확인할 수 있습니다."
      }}
    }}
  ]
}}
</script>
"""

_HERO = f"""<section class="hero">
  <div class="hero-inner">
    <p class="hero-badge">Premium Visiting Spa · 강남구 전지역</p>
    <h1>강남 출장마사지 · 강남구 홈타이<br>지역별 예약 안내</h1>
    <p class="hero-lead">샵까지 갈 필요 없이, 계신 곳에서 받는 프리미엄 방문 관리.<br>자택·오피스텔·숙소 어디든 전화 한 통이면 예약이 끝납니다.</p>
    <div class="hero-actions">
      <a class="hero-btn primary" href="tel:{PHONE}">📞 {PHONE_DISPLAY}</a>
      <a class="hero-btn" href="/courses/">코스 안내 보기</a>
    </div>
    <ul class="hero-stats">
      <li><strong>12개</strong><span>대표 행정동</span></li>
      <li><strong>27개</strong><span>역세권 안내</span></li>
      <li><strong>9개</strong><span>생활권 안내</span></li>
      <li><strong>24시간</strong><span>예약 상담</span></li>
    </ul>
  </div>
</section>
"""

_BODY = f"""
<section id="service">
<h2>강남구에서 출장마사지를 찾는 이유</h2>
<p>강남 출장마사지를 찾는 분들은 대부분 현재 위치에서 가까운 방문 가능 지역을 먼저 확인합니다. 강남구는 서울 안에서도 업무지구, 상권, 주거지, 학원가, 병원가, 대형 복합시설이 한데 모인 지역이라, 같은 강남이라도 어느 동·어느 역 인근이냐에 따라 검색 의도와 이용 패턴이 크게 다릅니다. 이 페이지는 강남구 전체 구조를 설명하는 허브로, 대표 행정동·지하철역·생활권·테마별 안내로 연결됩니다. {BRAND}는 예약 확인부터 방문 관리까지 정해진 절차에 따라 진행하며, 처음 이용하시는 분도 어렵지 않게 예약할 수 있도록 각 단계를 명확하게 안내해 드립니다.</p>
</section>

<section id="coverage">
<h2>대표 행정동별 방문 가능 지역 안내</h2>
<p>강남구 지역 안내는 신사·압구정·청담·논현·삼성·역삼·대치·도곡·개포·일원·수서·세곡 열두 개 대표 행정동을 중심으로 구성되어 있습니다. 논현1·2동, 삼성1·2동, 역삼1·2동, 대치1·2·4동, 도곡1·2동, 개포1~4동, 일원본동·일원1동처럼 번호로 나뉜 행정동은 별도 페이지를 만들지 않고 각 대표 동 페이지에서 통합 안내합니다. 같은 생활권을 잘게 쪼개 비슷한 내용을 반복하기보다, 대표 동 단위로 묶어 생활권 특징과 방문 조건을 한 번에 설명하는 편이 이용자에게도 정확하기 때문입니다.</p>
<ul class="card-grid">
<li><a href="/gangnam/sinsa-dong-chuljangmassage/">신사동</a></li>
<li><a href="/gangnam/apgujeong-dong-chuljangmassage/">압구정동</a></li>
<li><a href="/gangnam/cheongdam-dong-chuljangmassage/">청담동</a></li>
<li><a href="/gangnam/nonhyeon-dong-chuljangmassage/">논현동</a></li>
<li><a href="/gangnam/samseong-dong-chuljangmassage/">삼성동</a></li>
<li><a href="/gangnam/yeoksam-dong-chuljangmassage/">역삼동</a></li>
<li><a href="/gangnam/daechi-dong-chuljangmassage/">대치동</a></li>
<li><a href="/gangnam/dogok-dong-chuljangmassage/">도곡동</a></li>
<li><a href="/gangnam/gaepo-dong-chuljangmassage/">개포동</a></li>
<li><a href="/gangnam/irwon-dong-chuljangmassage/">일원동</a></li>
<li><a href="/gangnam/suseo-dong-chuljangmassage/">수서동</a></li>
<li><a href="/gangnam/segok-dong-chuljangmassage/">세곡동</a></li>
</ul>
<p>강남구 전체 구조가 궁금하시면 <a href="/gangnam/">강남구 전체 안내</a>에서 한눈에 확인하실 수 있습니다.</p>
</section>

<section id="stations">
<h2>강남역·역삼역·선릉역·삼성역 역세권 안내</h2>
<p>지하철역별 안내는 강남구를 지나는 2호선·신분당선·7호선·9호선·수인분당선·3호선 주요 역세권을 기준으로 구성합니다. 강남역·역삼역·선릉역·삼성역처럼 실제 검색 수요가 큰 키워드를 중심으로, 각 역 페이지에서 인근 생활권과 주변 대표 동, 방문 전 준비사항을 설명합니다. 강남역(2호선·신분당선), 선릉역(2호선·수인분당선), 수서역(3호선·수인분당선·SRT·GTX)처럼 노선이 여러 개인 환승역도 역명 기준 1개 페이지만 운영하며, 노선별·출구별 페이지는 만들지 않습니다.</p>
<ul class="card-grid">
<li><a href="/gangnam/gangnam-station-chuljangmassage/">강남역</a></li>
<li><a href="/gangnam/sinnonhyeon-station-chuljangmassage/">신논현역</a></li>
<li><a href="/gangnam/yeoksam-station-chuljangmassage/">역삼역</a></li>
<li><a href="/gangnam/seolleung-station-chuljangmassage/">선릉역</a></li>
<li><a href="/gangnam/samseong-station-chuljangmassage/">삼성역</a></li>
<li><a href="/gangnam/apgujeong-station-chuljangmassage/">압구정역</a></li>
<li><a href="/gangnam/cheongdam-station-chuljangmassage/">청담역</a></li>
<li><a href="/gangnam/daechi-station-chuljangmassage/">대치역</a></li>
<li><a href="/gangnam/suseo-station-chuljangmassage/">수서역</a></li>
</ul>
<p>강남구 27개 역세권 전체는 <a href="/gangnam/stations/">지하철역별 안내</a>에서 확인하실 수 있습니다.</p>
</section>

<section id="districts">
<h2>청담·압구정·논현·대치 생활권 차이</h2>
<p>강남역과 역삼역 주변은 테헤란로 업무지구 수요가 강하고, 선릉역과 삼성역 주변은 오피스와 코엑스 생활권으로 이어집니다. 청담동과 압구정동은 고급 주거지·상권·병원·미용 수요가 함께 있고, 대치동과 도곡동은 학원가와 주거지 중심으로 구분됩니다. 같은 강남이라도 생활권마다 방문 시간대와 공간 준비가 다르므로, 생활권 단위로 정리한 안내를 함께 참고하시면 본인 위치에 맞는 정보를 더 빨리 찾을 수 있습니다.</p>
<ul class="card-grid">
<li><a href="/gangnam/gangnam-station-area-chuljangmassage/">강남역 생활권</a></li>
<li><a href="/gangnam/teheran-ro-area-chuljangmassage/">테헤란로 업무지구</a></li>
<li><a href="/gangnam/coex-samseong-area-chuljangmassage/">삼성역·코엑스 생활권</a></li>
<li><a href="/gangnam/cheongdam-apgujeong-area-chuljangmassage/">청담·압구정 생활권</a></li>
<li><a href="/gangnam/nonhyeon-hakdong-area-chuljangmassage/">논현·학동 생활권</a></li>
<li><a href="/gangnam/daechi-academy-area-chuljangmassage/">대치동 학원가</a></li>
<li><a href="/gangnam/dogok-gaepo-area-chuljangmassage/">도곡·개포 생활권</a></li>
<li><a href="/gangnam/suseo-area-chuljangmassage/">수서역 생활권</a></li>
<li><a href="/gangnam/segok-jagok-area-chuljangmassage/">세곡·자곡 생활권</a></li>
</ul>
</section>

<section id="themes">
<h2>테마별 관리 안내</h2>
<p>테마별 안내에서는 관리 유형별 특징, 추천 대상, 예약 전 확인사항을 설명합니다. 테마는 각각 독립 페이지로 운영하며, 지역 페이지와 역 페이지에서는 관련 테마로 연결만 해 드립니다. 특정 역과 테마를 조합한 페이지는 운영하지 않으니, 원하시는 관리 유형을 먼저 고른 뒤 예약 시 위치를 알려주시면 됩니다.</p>
<ul class="card-grid">
<li><a href="/themes/swedish/">스웨디시</a></li>
<li><a href="/themes/lomilomi/">로미로미</a></li>
<li><a href="/themes/thai/">타이마사지</a></li>
<li><a href="/themes/chinese/">중국마사지</a></li>
<li><a href="/themes/aroma/">아로마테라피</a></li>
<li><a href="/themes/homecare/">홈케어</a></li>
<li><a href="/themes/hotel-style/">호텔식마사지</a></li>
<li><a href="/themes/foot/">발마사지</a></li>
<li><a href="/themes/sports/">스포츠·경락</a></li>
<li><a href="/themes/skincare/">스킨케어</a></li>
<li><a href="/themes/waxing/">왁싱</a></li>
<li><a href="/themes/couple/">커플 관리</a></li>
<li><a href="/themes/24hours/">24시간</a></li>
<li><a href="/themes/overnight/">수면 가능</a></li>
</ul>
</section>

<section id="course">
<h2>코스 선택 안내</h2>
<p>코스는 이용 목적과 그날의 컨디션에 따라 선택하시는 것이 좋습니다. 누적된 피로를 풀고 싶은 분, 편안한 휴식이 필요한 분, 운동 후 근육 이완이 필요한 분, 숙소로 방문을 원하시는 분, 커플이 함께 받고 싶은 분 등 상황에 맞는 선택 기준을 <a href="/courses/">코스안내</a> 페이지에서 자세히 다룹니다. 고민되시면 예약 전화에서 상태를 말씀해 주세요. 함께 정해 드립니다.</p>
</section>

<section id="hometai">
<h2>강남 홈타이 예약 전 확인사항</h2>
<p>강남 홈타이는 자택, 숙소, 사무실 인근에서 예약 가능 여부를 먼저 확인한 뒤 이용하는 방문형 관리 서비스입니다. 원활한 방문을 위해 정확한 주소, 공동현관 출입 방법, 주차 가능 여부, 조용한 공간 확보 여부를 미리 확인해 주시면 좋습니다. 강남구는 강남역·역삼역 업무지구와 수서·세곡 생활권의 이동 기준이 다르고, 청담·압구정, 대치·도곡, 개포·일원도 도로 상황과 시간대에 따라 방문 가능 시간이 달라질 수 있으므로 예약 전 확인이 중요합니다. 준비사항 전체는 <a href="/guide/">이용가이드</a>에 정리되어 있습니다.</p>
</section>

<section id="safety">
<h2>강남 출장마사지 사이트 이용 가이드</h2>
<p>이 사이트는 과장된 표현 대신 신뢰를 주는 안내형 문장으로 구성되어 있습니다. 방문 가능 지역, 예약 가능 시간, 추가 이동비 여부, 결제 방식, 취소 기준, 개인정보 처리 기준, 고객 유의사항을 분명하게 안내하며, 불법·선정적 표현이나 허위 후기는 사용하지 않습니다. 메인페이지는 강남구 전체 안내를 담당하고, 대표 행정동·역세권·생활권 페이지가 각 세부 검색을 담당합니다. 이용 전 서비스 범위와 유의사항을 확인해 주시고, 무리하거나 불법적인 요청은 어떤 경우에도 진행하지 않는다는 기준을 분명히 안내드립니다.</p>
</section>

<section id="faq">
<h2>자주 묻는 질문</h2>
<div class="faq-item">
<h3>강남구 전지역 방문이 가능한가요?</h3>
<p>예약 시간, 정확한 위치, 배정 상황에 따라 가능 여부가 달라집니다. 지역별 안내에서 신사·압구정·청담·논현·삼성·역삼·대치·도곡·개포·일원·수서·세곡동 기준으로 확인할 수 있습니다.</p>
</div>
<div class="faq-item">
<h3>강남역이나 선릉역 근처도 가능한가요?</h3>
<p>강남역·역삼역·선릉역·삼성역 등 주요 역세권은 역 상세 페이지에서 주변 생활권과 함께 안내합니다. 정확한 가능 여부는 예약 시 위치를 기준으로 확인합니다.</p>
</div>
<div class="faq-item">
<h3>논현1동과 논현2동은 왜 따로 없나요?</h3>
<p>논현1·2동은 논현동, 삼성1·2동은 삼성동, 개포1~4동은 개포동처럼 번호 행정동은 대표 동 페이지에서 통합 안내하여 중복 페이지 위험을 줄입니다.</p>
</div>
<div class="faq-item">
<h3>환승역은 호선별로 페이지가 다른가요?</h3>
<p>아니요. 강남역, 선릉역, 수서역 같은 환승역도 역명 기준 1개 페이지만 운영합니다. 노선별·출구별 페이지는 만들지 않습니다.</p>
</div>
<div class="faq-item">
<h3>강남 홈타이는 어떻게 예약하나요?</h3>
<p>자택, 숙소, 사무실 인근 방문 가능 여부를 먼저 확인한 뒤 위치와 희망 시간을 알려주시면 됩니다. 예약 전화로 가장 빠르게 확인할 수 있습니다.</p>
</div>
</section>

{PRICING}
<section id="contact" class="cta">
<h2>예약문의</h2>
<p>강남구 방문 관리 예약과 상담은 전화로 가장 빠르게 진행됩니다. 위치와 희망 시간을 알려주시면 가능 여부를 바로 확인해 드립니다.</p>
<a class="cta-phone" href="tel:{PHONE}">{PHONE_DISPLAY}</a>
</section>
"""

PAGE = {
    "path": "",
    "title": "강남 출장마사지｜강남구 홈타이 지역별 예약 안내",
    "desc": "강남 출장마사지·홈타이 예약 전 행정동, 역세권, 이용 기준을 정리했습니다.",
    "h1": "강남 출장마사지 · 강남구 홈타이 지역별 예약 안내",
    "body": _BODY,
    "extra_head": _JSONLD,
    "breadcrumb": [],
    "hero": _HERO,
}
