REGION_KEYWORDS: dict[str, list[str]] = {
    "Middle East": [
        "israel", "palestine", "gaza", "iran", "iraq", "syria", "lebanon",
        "saudi", "arabia", "yemen", "jordan", "egypt", "turkey", "qatar",
        "kuwait", "bahrain", "oman", "dubai", "tehran", "baghdad", "beirut",
    ],
    "South Asia": [
        "india", "pakistan", "afghanistan", "bangladesh", "sri lanka",
        "nepal", "bhutan", "maldives", "delhi", "mumbai", "karachi",
        "kabul", "dhaka", "colombo", "kashmir",
    ],
    "Europe": [
        "ukraine", "russia", "france", "germany", "uk", "britain", "england",
        "spain", "italy", "poland", "nato", "eu", "brussels", "berlin",
        "paris", "london", "rome", "madrid", "kyiv", "moscow",
    ],
    "USA": [
        "usa", "united states", "america", "washington", "biden", "trump",
        "congress", "senate", "pentagon", "white house", "new york",
        "california", "texas", "florida", "chicago",
    ],
}

def get_region(text: str) -> str:
    lower = text.lower()
    for region, keywords in REGION_KEYWORDS.items():
        if any(keyword in lower for keyword in keywords):
            return region
    return "Other"
