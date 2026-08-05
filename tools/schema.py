from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional


@dataclass
class ProductSelectors:
    title: Optional[str] = None
    price: Optional[str] = None
    old_price: Optional[str] = None
    image: Optional[str] = None
    link: Optional[str] = None
    rating: Optional[str] = None
    reviews: Optional[str] = None


@dataclass
class ListingSelectors:
    container: Optional[str] = None
    item: Optional[str] = None
    next_page: Optional[str] = None


@dataclass
class ApiEndpoint:
    url: str
    method: str = "GET"
    content_type: Optional[str] = None


@dataclass
class AnalysisReport:

    site: str

    homepage: str

    render: str = "unknown"

    framework: Optional[str] = None

    anti_bot: List[str] = field(default_factory=list)

    json_ld: bool = False

    listing: ListingSelectors = field(default_factory=ListingSelectors)

    product: ProductSelectors = field(default_factory=ProductSelectors)

    api: List[ApiEndpoint] = field(default_factory=list)

    xhr: List[str] = field(default_factory=list)

    cookies: List[str] = field(default_factory=list)

    scripts: List[str] = field(default_factory=list)

    headers: Dict[str, str] = field(default_factory=dict)

    difficulty: int = 1

    recommended_strategy: str = "requests"

    notes: List[str] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)
