"""
University scraping configurations.

Each entry maps a university domain/identifier to its scraping configuration.
The unified extractor uses these configurations to handle different university websites.
"""

from typing import Dict, List, Optional, Callable
from urllib.parse import urlparse, parse_qs, unquote, urljoin


def resolve_funnelback_redirect(href: str, base_url: str) -> Optional[str]:
    """Resolve Funnelback redirect URLs."""
    if not href:
        return None
    parsed = urlparse(href)
    if "redirect" in parsed.path or "funnelback" in parsed.netloc:
        qs = parse_qs(parsed.query)
        if "url" in qs and qs["url"]:
            real_url = unquote(qs["url"][0])
            if real_url.startswith("//"):
                real_url = "https:" + real_url
            elif real_url.startswith("/"):
                real_url = urljoin(base_url, real_url)
            return real_url
    return urljoin(base_url, href) if href else None


def resolve_derby_redirect(href: str, base_url: str) -> Optional[str]:
    """Resolve Derby redirect URLs."""
    if not href:
        return None
    parsed = urlparse(href)
    if "funnelback" in parsed.netloc and parsed.path.endswith("/redirect"):
        qs = parse_qs(parsed.query)
        if "url" in qs and qs["url"]:
            return unquote(qs["url"][0])
    return urljoin(base_url, href)


def resolve_hw_redirect(href: str, base_url: str) -> Optional[str]:
    """Resolve Heriot-Watt redirect URLs."""
    if not href:
        return None
    if "url=" in href:
        parsed = urlparse(href)
        query = parse_qs(parsed.query)
        encoded = query.get("url", [None])[0]
        if encoded:
            return unquote(encoded)
    return urljoin(base_url, href) if href else None


def resolve_canterbury_redirect(href: str, base_url: str) -> Optional[str]:
    """Resolve Canterbury redirect URLs."""
    if not href:
        return None
    parsed = urlparse(href)
    query = parse_qs(parsed.query)
    raw_url = query.get("url", [None])[0]
    if raw_url:
        try:
            return unquote(raw_url)
        except:
            return None
    return urljoin(base_url, href) if href else None


# University configurations dictionary
UNIVERSITY_CONFIGS: Dict[str, Dict] = {
    # Abertay University
    "abertay.ac.uk": {
        "folder_name": "abertay",
        "course_selector": "h3 > a[href*='redirect']",
        "pagination_type": "next_button",
        "pagination_selector": "a.next:not(.disabled)",
        "filter_keywords": ["/postgraduate-taught/", "/postgraduate-research/", "undergraduate"],
        "match_mode": "segment",
        "url_resolution": resolve_funnelback_redirect,
        "wait_selector": "h3 > a[href*='redirect']",
    },
    
    # Derby University
    "derby.ac.uk": {
        "folder_name": "derby",
        "course_selector": "div.course-teaser-heading a",
        "pagination_type": "next_button",
        "pagination_selector": "div.pagination-controls a[title='Next']",
        "filter_keywords": ["undergraduate", "postgraduate"],
        "match_mode": "contains",
        "url_resolution": resolve_derby_redirect,
    },
    
    # University College Birmingham (UCB)
    "ucb.ac.uk": {
        "folder_name": "ucb",
        "course_selector": "a[href*='/study/courses/']",
        "pagination_type": "single_page",
        "pagination_selector": None,
        "filter_keywords": [],
        "match_mode": "contains",
    },
    
    # Heriot-Watt University
    "hw.ac.uk": {
        "folder_name": "hw",
        "course_selector": "td.hw_course-search__subject a[href*='/s/redirect']",
        "pagination_type": "next_button",
        "pagination_selector": "a.hw_course-search__pagination-link--next, a[aria-label='Next']",
        "filter_keywords": [],
        "match_mode": "contains",
        "url_resolution": resolve_hw_redirect,
        "wait_selector": "td.hw_course-search__subject",
    },
    
    # Canterbury University (New Zealand)
    "canterbury.ac.nz": {
        "folder_name": "canterbury",
        "course_selector": ".cmp-funnelback-search__results-item-title a.cmp-button[href*='redirect']",
        "pagination_type": "url_params",
        "pagination_selector": None,
        "pagination_param": "start_rank",
        "pagination_increment": 20,
        "filter_keywords": [],
        "match_mode": "contains",
        "url_resolution": resolve_canterbury_redirect,
        "wait_selector": ".cmp-funnelback-search__results-item-title",
    },
    
    # Otago University
    "otago.ac.nz": {
        "folder_name": "otago",
        "course_selector": "div.listing-item__header.test a[data-live-url]",
        "pagination_type": "next_button",
        "pagination_selector": "div.pagination__item--next a[rel~='next']",
        "filter_keywords": [],
        "match_mode": "contains",
        "wait_selector": "div.listing-item__header.test",
    },
    
    # MCPHS University
    "mcphs.edu": {
        "folder_name": "mcphs",
        "course_selector": ".generic-card__heading > a",
        "pagination_type": "next_button",
        "pagination_selector": "button.pagination__next-button:not([disabled])",
        "filter_keywords": [],
        "match_mode": "contains",
        "wait_selector": ".generic-card__heading > a",
    },
    
    # York College of Pennsylvania
    "ycp.edu": {
        "folder_name": "york",
        "course_selector": "div[x-data*='open'] h2",
        "pagination_type": "url_params",
        "pagination_selector": "li.pager__item--next a[rel='next']",
        "pagination_param": "page",
        "filter_keywords": [],
        "match_mode": "contains",
        "wait_selector": "div[x-data*='open'] h2",
        "special_logic": "generate_slug_from_title",  # Generates URLs from titles
    },
    
    # University of Buckingham
    "buckingham.ac.uk": {
        "folder_name": "buckingham",
        "course_selector": ".courses .courselist-internal > a[href]",
        "pagination_type": "accordion",
        "pagination_selector": "button.levelheader.accordion_title",
        "filter_keywords": ["undergraduate", "postgraduate", "foundation"],
        "match_mode": "contains",
        "wait_selector": "button.levelheader.accordion_title",
    },
    
    # Staffordshire University
    "staffs.ac.uk": {
        "folder_name": "staffs",
        "course_selector": "h2.card__title > a.link--stretched",
        "pagination_type": "next_button",
        "pagination_selector": "a[data-test-id='searchstax-pagination-next']:not(.disabled)",
        "filter_keywords": [],
        "match_mode": "contains",
        "wait_selector": ".card__content",
    },
    
    # University of Bedfordshire
    "beds.ac.uk": {
        "folder_name": "bedford",
        "course_selector": ".course-search-result a[href^='/courses/']",
        "pagination_type": "next_button",
        "pagination_selector": "button.page-link.course-search-page-link[aria-label='Next']:not([disabled])",
        "filter_keywords": [],
        "match_mode": "segment",
        "wait_selector": ".course-search-result",
    },
    
    # Coventry University
    "coventry.ac.uk": {
        "folder_name": "coventry",
        "course_selector": "p.h5.mtm > a",
        "pagination_type": "next_button",
        "pagination_selector": "nav[aria-label='Pagination Navigation'] li.button > a:text('Next')",
        "filter_keywords": ["foundation", "undergraduate", "postgraduate"],
        "match_mode": "segment",
    },
    
    # Sheffield Hallam University
    "shu.ac.uk": {
        "folder_name": "shu",
        "course_selector": "a.m-snippet__link",
        "pagination_type": "page_numbers",
        "pagination_selector": ".m-pagination",
        "pagination_extract_pattern": r"of\D*(\d+)",
        "pagination_param": "page",
        "filter_keywords": [],
        "match_mode": "contains",
        "wait_selector": "a.m-snippet__link",
    },
    
    # University of Leicester
    "le.ac.uk": {
        "folder_name": "leac",
        "course_selector": "li.search-result-list__item h4.search-result-list__title a",
        "pagination_type": "next_button",
        "pagination_selector": "a.pagination__link--next",
        "filter_keywords": [],
        "match_mode": "segment",
        "wait_selector": "ul.search-result-list",
    },
    
    # University of Salford
    "salford.ac.uk": {
        "folder_name": "salford",
        "course_selector": "a.uos-search-card__link",
        "pagination_type": "next_button",
        "pagination_selector": "li.uos-pager__item--next a.uos-pager__link[rel='next']",
        "filter_keywords": ["undergraduate", "postgraduate"],
        "match_mode": "segment",
    },
    
    # Wrexham University
    "wrexham.ac.uk": {
        "folder_name": "wrexham",
        "course_selector": ".search-result-card h2 a[href]",
        "pagination_type": "single_page",
        "pagination_selector": None,
        "filter_keywords": ["postgraduate", "undergraduate"],
        "match_mode": "segment",
        "wait_selector": ".search-result-card",
    },
    
    # University for the Creative Arts (UCA)
    "uca.ac.uk": {
        "folder_name": "uca",
        "course_selector": "div.col-12 > a[href^='/study/courses/']",
        "pagination_type": "page_numbers",
        "pagination_selector": "div.col.pagination-control[data-t4-ajax-link='normal']",
        "pagination_param": "page",
        "filter_keywords": [],
        "match_mode": "contains",
        "wait_selector": "div.col-12 > a[href^='/study/courses/']",
    },
}


def get_config_for_url(url: str) -> Optional[Dict]:
    """
    Get university configuration for a given URL.
    
    Args:
        url: University course page URL
        
    Returns:
        Configuration dictionary or None if not found
    """
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        # Try exact domain match first
        if domain in UNIVERSITY_CONFIGS:
            return UNIVERSITY_CONFIGS[domain]
        
        # Try partial domain match (e.g., "www.abertay.ac.uk" -> "abertay.ac.uk")
        for config_domain, config in UNIVERSITY_CONFIGS.items():
            if config_domain in domain or domain.endswith(config_domain):
                return config
        
        return None
    except Exception:
        return None


def get_all_configured_domains() -> List[str]:
    """Get list of all configured university domains."""
    return list(UNIVERSITY_CONFIGS.keys())


def get_university_display_name(url: str) -> str:
    """
    Get display name for a university from its URL.
    
    Args:
        url: University course page URL
        
    Returns:
        Display name of the university
    """
    config = get_config_for_url(url)
    if not config:
        # Try to extract from URL
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        # Remove www. and common TLDs, capitalize
        name = domain.replace("www.", "").split(".")[0]
        return name.replace("-", " ").title()
    
    # Map folder names to display names
    folder_to_name = {
        "abertay": "Abertay University",
        "derby": "University of Derby",
        "ucb": "University College Birmingham",
        "hw": "Heriot-Watt University",
        "canterbury": "University of Canterbury",
        "otago": "University of Otago",
        "mcphs": "MCPHS University",
        "york": "York College of Pennsylvania",
        "buckingham": "University of Buckingham",
        "staffs": "Staffordshire University",
        "bedford": "University of Bedfordshire",
        "coventry": "Coventry University",
        "shu": "Sheffield Hallam University",
        "leac": "University of Leicester",
        "salford": "University of Salford",
        "wrexham": "Wrexham University",
        "uca": "University for the Creative Arts",
    }
    
    folder_name = config.get("folder_name", "")
    return folder_to_name.get(folder_name, folder_name.replace("_", " ").title())

