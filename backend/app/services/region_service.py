"""
region_service.py
-----------------
Extracts the geographic region from a news article headline.

All regional vocabulary is imported from the centralised
app.core.domain_knowledge module; no keyword lists are defined here.

Logic
-----
Iterates over REGION_KEYWORDS in definition order.  The first region
whose keyword list contains a match (case-insensitive substring) is
returned.  Returns "Other" if no region matches.
"""

from app.core.domain_knowledge import REGION_KEYWORDS


def get_region(text: str) -> str:
    lower = text.lower()
    for region, keywords in REGION_KEYWORDS.items():
        if any(keyword in lower for keyword in keywords):
            return region
    return "Other"
