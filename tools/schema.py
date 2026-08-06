from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


@dataclass
class ProductSelectors:
    container: Optional[str] = None
    title: Optional[str] = None
    price: Optional[str] = None
    old_price: Optional[str] = None
    image: Optional[str] = None
    link: Optional[str] = None


@dataclass
class AnalysisReport:

    # Temel bilgiler
    store: str
    url: str

    # HTTP
    status_code: Optional[int] = None
    final_url: Optional[str] = None
    response_time: Optional[float] = None

    headers: Dict[str, str] = field(default_factory=dict)
    cookies: Dict[str, str] = field(default_factory=dict)

    # Sayfa içeriği
    html: Optional[str] = None
    rendered_html: Optional[str] = None

    title: Optional[str] = None

    meta: Dict[str, str] = field(default_factory=dict)
    opengraph: Dict[str, str] = field(default_factory=dict)

    canonical: Optional[str] = None

    json_ld: List[Any] = field(default_factory=list)
    product_jsonld: Dict[str, Any] = field(default_factory=dict)

    scripts: List[str] = field(default_factory=list)

    # Playwright
    render: str = "unknown"
    framework: Optional[str] = None

    network: List[Dict[str, Any]] = field(default_factory=list)

    # DOM Analizi
    selectors: ProductSelectors = field(default_factory=ProductSelectors)

    selector_candidates: List[Dict[str, Any]] = field(default_factory=list)

    product_candidate: Dict[str, Any] = field(default_factory=dict)

    # Çıktılar
    html_path: Optional[str] = None
    screenshot_path: Optional[str] = None

    # Tanı / Notlar
    notes: List[str] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)