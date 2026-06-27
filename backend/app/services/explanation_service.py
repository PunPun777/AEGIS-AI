KEYWORD_GROUPS: dict[str, list[tuple[set[str], str]]] = {
    "conflict": [
        ({"missile", "rocket", "ballistic", "projectile"}, "Missile or projectile terminology detected"),
        ({"airstrike", "strike", "bombardment", "bombing"}, "Aerial strike language identified"),
        ({"explosion", "blast", "detonation", "bomb"}, "Explosive event language detected"),
        ({"war", "warfare", "warzone", "combat"}, "Active warfare context found"),
        ({"invasion", "incursion", "occupation", "siege"}, "Territorial invasion language identified"),
        ({"terror", "terrorist", "terrorism", "extremist"}, "Terrorism-related language detected"),
        ({"military", "troops", "soldiers", "armed forces", "battalion"}, "Military presence terminology detected"),
        ({"attack", "assault", "offensive"}, "Attack-related language identified"),
        ({"border", "frontier", "crossing", "checkpoint"}, "Border conflict context found"),
        ({"shelling", "artillery", "mortar", "gunfire"}, "Heavy weapons terminology detected"),
        ({"casualties", "fatalities", "deaths", "wounded", "killed"}, "Casualty language present"),
    ],
    "protest": [
        ({"protest", "protests", "protester"}, "Protest activity language identified"),
        ({"demonstration", "demonstrators"}, "Public demonstration context found"),
        ({"march", "marchers", "marching"}, "Organized march activity detected"),
        ({"rally", "rallying", "mobilization"}, "Rally or mobilization language identified"),
        ({"strike", "walkout", "stoppage"}, "Industrial or civil action language detected"),
        ({"sit-in", "blockade", "occupation"}, "Non-violent resistance terminology found"),
        ({"activists", "activist", "campaigners"}, "Activist group language detected"),
        ({"unrest", "clashes", "tension", "friction"}, "Civil unrest indicators present"),
        ({"demands", "petition", "grievance"}, "Grievance and demand language identified"),
    ],
    "normal": [
        ({"agreement", "treaty", "accord", "deal"}, "Diplomatic agreement language found"),
        ({"meeting", "summit", "conference", "talks"}, "Diplomatic engagement context detected"),
        ({"economic", "economy", "trade", "commerce"}, "Economic context identified"),
        ({"growth", "development", "expansion"}, "Positive development language present"),
        ({"festival", "celebration", "cultural"}, "Cultural event language detected"),
        ({"education", "school", "university"}, "Education sector context found"),
        ({"cooperation", "collaboration", "partnership"}, "Cooperative language identified"),
        ({"health", "medical", "healthcare"}, "Health sector context detected"),
        ({"aid", "relief", "humanitarian"}, "Humanitarian context language found"),
        ({"election", "vote", "parliament", "congress"}, "Political process language identified"),
    ],
}

_FALLBACK_EXPLANATIONS: dict[str, str] = {
    "conflict": "Geopolitical conflict indicators present",
    "protest": "Civil unrest indicators present",
    "normal": "No significant threat indicators detected",
}


def generate_explanation(text: str, prediction: str) -> list[str]:
    lower = text.lower()
    groups = KEYWORD_GROUPS.get(prediction, [])
    explanations = [
        sentence
        for keywords, sentence in groups
        if any(kw in lower for kw in keywords)
    ]
    if not explanations:
        explanations = [_FALLBACK_EXPLANATIONS.get(prediction, "Classification based on model output")]
    return explanations
