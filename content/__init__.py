# 전체 페이지 목록 집계
from . import main, areas, stations, stations2, districts, themes, info, magazine, about

PAGES = (
    [main.PAGE]
    + areas.PAGES
    + stations.PAGES
    + stations2.PAGES
    + districts.PAGES
    + themes.PAGES
    + info.PAGES
    + magazine.PAGES
    + [about.PAGE]
)
