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
    store: str
    url: str

    render: str = "unknown"
    framework: Optional[str] = None

    html_path: Optional[str] = None
    screenshot_path: Optional[str] = None

    headers: Dict[str, str] = field(default_factory=dict)
    meta: Dict[str, str] = field(default_factory=dict)

    json_ld: List[Any] = field(default_factory=list)

    scripts: List[str] = field(default_factory=list)

    network: List[Dict[str, Any]] = field(default_factory=list)

    selectors: ProductSelectors = field(default_factory=ProductSelectors)

    notes: List[str] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)