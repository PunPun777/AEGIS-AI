"""
domain_knowledge.py
-------------------
Geopolitical Domain Intelligence Layer

This module is the single source of truth for all geopolitical vocabulary
used across AEGIS-AI's intelligence services.  No service should define
its own keyword lists; every keyword-based decision should import from here.

Organisation
------------
Each constant is a frozenset[str] of lowercase terms (no duplicates).
Related frozensets are combined into SEMANTIC_GROUPS (a dict keyed by a
string label) for services that iterate over categories.

Naming convention
-----------------
<DOMAIN>_KEYWORDS   — frozenset of lowercase terms for that domain
"""

# ─────────────────────────────────────────────────────────────────────────────
# KINETIC / PHYSICAL CONFLICT
# ─────────────────────────────────────────────────────────────────────────────

AIRSTRIKE_KEYWORDS: frozenset[str] = frozenset({
    "airstrike", "air strike", "air strikes", "airstrikes",
    "air raid", "air raids", "air campaign", "air offensive",
    "bombing", "bombing raid", "bombing campaign", "bombardment",
    "aerial attack", "aerial bombardment", "aerial offensive",
    "close air support", "cas sortie", "sorties",
    "fighter jet", "fighter jets", "warplane", "warplanes",
    "combat aircraft", "bomber", "bombers", "stealth bomber",
    "b-52", "f-16", "f-35", "su-35", "su-57", "mig-29",
    "drone strike", "drone attack", "uav strike", "uav attack",
    "precision strike", "precision bombing",
})

MISSILE_KEYWORDS: frozenset[str] = frozenset({
    "missile", "missiles", "ballistic missile", "ballistic missiles",
    "cruise missile", "cruise missiles", "anti-ship missile",
    "surface-to-air missile", "sam", "anti-missile", "interceptor",
    "rocket", "rockets", "rocket fire", "rocket barrage", "rocket attack",
    "rocket salvo", "projectile", "projectiles",
    "hypersonic missile", "hypersonic weapon",
    "long-range missile", "medium-range missile", "short-range missile",
    "icbm", "irbm", "srbm", "scud", "patriot", "iron dome",
    "s-400", "s-300", "thaad", "artillery rocket",
    "mortar round", "mortar", "mortars", "mortar fire",
    "rpg", "rocket-propelled grenade",
})

WEAPON_KEYWORDS: frozenset[str] = frozenset({
    "weapon", "weapons", "weaponry", "arms", "arsenal",
    "firearm", "firearms", "ammunition", "ammo", "ordnance",
    "explosive", "explosives", "ied", "improvised explosive",
    "bomb", "bombs", "car bomb", "suicide bomb", "suicide bomber",
    "vest bomb", "shaped charge", "fragmentation",
    "grenade", "grenades", "hand grenade",
    "machine gun", "assault rifle", "sniper", "sniper rifle",
    "anti-tank", "atgm", "anti-aircraft", "anti-drone",
    "cluster munition", "cluster bomb", "white phosphorus",
    "thermobaric", "fuel-air explosive",
    "landmine", "landmines", "mine", "mines",
    "biological weapon", "chemical weapon", "wmd",
    "gun", "guns", "rifle", "rifles", "pistol",
})

MILITARY_KEYWORDS: frozenset[str] = frozenset({
    "military", "military forces", "armed forces", "armed group",
    "troops", "soldiers", "servicemen", "personnel", "combatants",
    "battalion", "brigade", "division", "regiment", "platoon",
    "squadron", "unit", "units", "garrison", "detachment",
    "deployment", "deployed", "mobilization", "mobilised", "mobilized",
    "military exercise", "war game", "wargame", "live-fire exercise",
    "joint exercise", "joint drill", "military drill",
    "military operation", "combat operation", "ground operation",
    "special forces", "special operations", "sof", "rangers",
    "marines", "navy seals", "paratrooper", "paratroopers",
    "air force", "navy", "army", "infantry", "cavalry",
    "armour", "armor", "armoured vehicle", "tank", "tanks",
    "military base", "military compound", "military outpost",
    "command center", "command centre", "headquarters",
    "reinforcements", "troop surge", "troop withdrawal",
    "ceasefire line", "front line", "frontline", "battle line",
    "national guard", "reserve forces", "paramilitary",
})

NAVAL_KEYWORDS: frozenset[str] = frozenset({
    "navy", "naval", "warship", "warships", "destroyer", "destroyers",
    "frigate", "frigates", "aircraft carrier", "carrier", "carriers",
    "submarine", "submarines", "corvette", "corvettes",
    "patrol boat", "patrol vessel", "coast guard",
    "naval base", "naval exercise", "naval blockade",
    "maritime", "maritime dispute", "sea lane", "sea lanes",
    "territorial waters", "exclusive economic zone", "eez",
    "south china sea", "red sea", "persian gulf", "arabian sea",
    "strait of hormuz", "strait of malacca", "black sea",
    "naval fleet", "fleet", "flotilla", "amphibious",
    "amphibious assault", "naval bombardment", "gunboat",
    "torpedo", "depth charge", "mine-laying", "mine sweeping",
    "freedom of navigation", "fonop",
})

SHELLING_KEYWORDS: frozenset[str] = frozenset({
    "shelling", "shell", "shells", "shell fire", "shellfire",
    "artillery", "artillery fire", "artillery barrage",
    "artillery shelling", "artillery strike", "howitzer",
    "cannon", "cannons", "gunfire", "gun battle", "gunfight",
    "crossfire", "sustained fire", "volley", "barrage",
    "heavy fire", "sniper fire", "tracer",
})

# ─────────────────────────────────────────────────────────────────────────────
# CONFLICT / WAR (broad)
# ─────────────────────────────────────────────────────────────────────────────

CONFLICT_KEYWORDS: frozenset[str] = frozenset({
    "conflict", "conflicts", "armed conflict",
    "war", "wars", "warfare", "warzone", "war zone",
    "combat", "combatant", "fighting", "clashes", "clash",
    "hostilities", "hostility", "belligerent", "belligerence",
    "battle", "battles", "battlefield", "skirmish", "skirmishes",
    "attack", "attacks", "attacked", "attacker", "attackers",
    "assault", "assaults", "offensive", "counter-offensive",
    "operation", "ground offensive", "military campaign",
    "siege", "sieges", "besieged", "encirclement",
    "occupation", "occupied territory", "occupying",
    "invasion", "invade", "invading", "invader",
    "incursion", "incursions", "cross-border",
    "annexation", "annexed", "annexing",
    "raid", "raids", "raided",
    "ambush", "ambushes", "ambushed",
    "infiltration", "infiltrate",
    "breakout", "counter-attack", "flank",
    "armed clash", "armed clashes", "armed confrontation",
    "warlord", "militia", "militias",
    "proxy war", "proxy conflict", "civil war",
    "inter-communal violence", "ethnic conflict",
    "sectarian violence", "sectarian conflict",
    "tribal conflict", "factional fighting",
})

INSURGENCY_KEYWORDS: frozenset[str] = frozenset({
    "insurgency", "insurgencies", "insurgent", "insurgents",
    "guerrilla", "guerrillas", "guerrilla warfare",
    "rebel", "rebels", "rebellion", "rebelling",
    "armed group", "armed faction", "faction", "factions",
    "separatist", "separatists", "separatism",
    "underground movement", "underground network",
    "cell", "sleeper cell", "extremist cell",
    "ambush attack", "hit and run", "asymmetric warfare",
    "counter-insurgency", "coin", "pacification",
    "insurgent group", "armed organization",
    "freedom fighter", "freedom fighters",
})

TERRORISM_KEYWORDS: frozenset[str] = frozenset({
    "terror", "terrorism", "terrorist", "terrorists",
    "extremist", "extremists", "extremism", "radical", "radicals",
    "jihadist", "jihadists", "jihad", "islamist", "islamists",
    "al-qaeda", "al qaeda", "isis", "isil", "daesh",
    "boko haram", "al-shabaab", "hezbollah", "hamas",
    "taliban", "haqqani", "lashkar",
    "suicide attack", "suicide bomber", "suicide bombing",
    "car bomb", "vehicle-ramming", "mass shooting",
    "mass casualty", "terror attack", "terror plot",
    "terror suspect", "terror financing", "terrorist cell",
    "homegrown extremist", "lone wolf",
    "radicalization", "radicalisation", "deradicalization",
    "counter-terrorism", "anti-terrorism",
    "kidnapping", "abduction", "hostage", "hostages",
    "beheading", "execution", "atrocity", "atrocities",
})

COUP_KEYWORDS: frozenset[str] = frozenset({
    "coup", "coup d'état", "coup d'etat",
    "military coup", "military takeover", "power grab",
    "putsch", "overthrow", "overthrown", "deposed",
    "junta", "military junta", "military government",
    "usurpation", "usurped",
    "government toppled", "government ousted",
    "president ousted", "leader deposed",
    "martial law", "state of emergency",
    "mutiny", "mutinied", "mutinous",
    "palace coup", "counter-coup",
})

CASUALTY_KEYWORDS: frozenset[str] = frozenset({
    "casualties", "casualty", "fatalities", "fatality",
    "killed", "dead", "deaths", "death toll",
    "wounded", "injured", "injuries", "hurt",
    "missing", "missing in action", "mia",
    "prisoner of war", "pow", "captured",
    "civilian death", "civilian casualties",
    "collateral damage", "civilian harm",
    "massacre", "slaughter", "killing", "killings",
    "mass grave", "body count",
})

# ─────────────────────────────────────────────────────────────────────────────
# NUCLEAR / WMD
# ─────────────────────────────────────────────────────────────────────────────

NUCLEAR_KEYWORDS: frozenset[str] = frozenset({
    "nuclear", "nuclear weapon", "nuclear weapons", "nuclear warhead",
    "nuclear bomb", "atomic bomb", "thermonuclear",
    "nuclear test", "nuclear testing", "nuclear detonation",
    "enrichment", "uranium enrichment", "plutonium",
    "centrifuge", "centrifuges", "heavy water reactor",
    "nuclear program", "nuclear programme", "nuclear deal",
    "jcpoa", "non-proliferation", "npt",
    "iaea", "nuclear inspectors", "nuclear safeguards",
    "nuclear deterrent", "nuclear deterrence",
    "first strike", "second strike", "mutually assured destruction", "mad",
    "dirty bomb", "radiological weapon",
    "tactical nuclear", "strategic nuclear",
    "nuclear missile", "icbm", "trident",
    "reactor", "nuclear reactor", "meltdown",
    "radiation leak", "radioactive", "fallout",
})

CYBER_KEYWORDS: frozenset[str] = frozenset({
    "cyberattack", "cyber attack", "cyber attacks",
    "cybersecurity", "cyber security", "cyber incident",
    "hacking", "hacked", "hackers", "hacker",
    "ransomware", "malware", "spyware", "trojan",
    "data breach", "data theft", "data leak",
    "infrastructure attack", "critical infrastructure",
    "power grid attack", "grid hack",
    "state-sponsored hacking", "nation-state hacking",
    "cyber espionage", "cyber spy", "cyber warfare",
    "ddos", "denial of service", "phishing",
    "zero-day", "vulnerability exploit",
    "apt", "advanced persistent threat",
    "cyber operation", "offensive cyber",
    "signals intelligence", "sigint", "electronic warfare",
})

# ─────────────────────────────────────────────────────────────────────────────
# PROTEST / CIVIL UNREST
# ─────────────────────────────────────────────────────────────────────────────

PROTEST_KEYWORDS: frozenset[str] = frozenset({
    "protest", "protests", "protester", "protesters", "protesting",
    "demonstration", "demonstrations", "demonstrator", "demonstrators",
    "demonstrating",
    "march", "marches", "marchers", "marching",
    "rally", "rallies", "rallying",
    "uprising", "uprisings", "revolt", "revolts",
    "riot", "riots", "rioting", "rioters",
    "civil unrest", "public disorder", "street protest",
    "mass protest", "mass demonstration", "nationwide protest",
    "anti-government protest", "pro-democracy protest",
    "student protest", "worker strike", "general strike",
    "sit-in", "sit in", "sit-down",
    "blockade", "blockades", "roadblock", "road block",
    "occupation" , "occupy", "occupying",
    "civil disobedience", "non-violent resistance",
    "crowd control", "riot police", "tear gas",
    "pepper spray", "water cannon", "rubber bullet",
    "crackdown", "dispersed", "dispersal",
    "activist", "activists", "campaigner", "campaigners",
    "organiser", "organizer", "movement", "grassroots",
    "petition", "petition drive",
    "grievance", "grievances", "demands",
    "chant", "chants", "placard", "banner",
    "walkout", "work stoppage", "labor action", "labour action",
    "picket", "picketing", "boycott",
    "hunger strike", "hunger striker",
    "mobilization", "mobilisation",
    "momentum", "solidarity march",
})

# ─────────────────────────────────────────────────────────────────────────────
# DIPLOMACY / PEACE
# ─────────────────────────────────────────────────────────────────────────────

DIPLOMACY_KEYWORDS: frozenset[str] = frozenset({
    "diplomacy", "diplomatic", "diplomat", "diplomats",
    "ambassador", "ambassadors", "embassy", "embassies",
    "consulate", "consulates", "envoy", "special envoy",
    "foreign minister", "foreign ministry", "state department",
    "bilateral", "multilateral", "trilateral",
    "summit", "summits", "high-level talks",
    "meeting", "meetings", "conference", "conferences",
    "dialogue", "talks", "negotiations", "negotiation",
    "foreign policy", "international relations",
    "diplomatic mission", "diplomatic ties",
    "diplomatic relations", "normalisation", "normalization",
    "expel", "expelled", "expulsion", "persona non grata",
    "sanctions relief", "diplomatic channel",
    "back-channel", "backchannel",
})

CEASEFIRE_KEYWORDS: frozenset[str] = frozenset({
    "ceasefire", "cease-fire", "cease fire",
    "truce", "truces", "armistice",
    "peace deal", "peace agreement", "peace accord",
    "peace process", "peace talks", "peace negotiations",
    "peace plan", "peace proposal",
    "humanitarian pause", "humanitarian corridor",
    "temporary halt", "halt to fighting",
    "de-escalation", "de escalation",
    "confidence-building", "confidence building measure",
    "buffer zone", "demilitarized zone", "dmz",
    "peace mission", "peacekeeping", "peacekeepers",
    "un peacekeepers", "peacekeeping force",
})

PEACE_KEYWORDS: frozenset[str] = frozenset({
    "peace", "peaceful", "peacebuilding", "peace building",
    "reconciliation", "reconcile",
    "post-conflict", "post conflict",
    "disarmament", "disarm", "demobilization", "demobilisation",
    "reintegration", "ddr",
    "transitional justice", "war crimes tribunal",
    "truth commission", "reparation", "reparations",
    "reconstruction", "rebuilding", "recovery",
    "stability", "stabilization", "stabilisation",
    "normalization", "normalisation",
    "cooperation", "collaborate", "partnership",
    "agreement", "agreements", "accord", "accords",
    "treaty", "treaties", "pact",
    "joint statement", "communiqué",
})

# ─────────────────────────────────────────────────────────────────────────────
# SANCTIONS / ECONOMY
# ─────────────────────────────────────────────────────────────────────────────

SANCTION_KEYWORDS: frozenset[str] = frozenset({
    "sanctions", "sanction", "sanctioned",
    "trade embargo", "embargo", "embargoes",
    "asset freeze", "asset seizure", "frozen assets",
    "travel ban", "visa ban",
    "export controls", "import ban", "import restrictions",
    "blacklist", "blacklisted", "blocked",
    "targeted sanctions", "sectoral sanctions",
    "economic pressure", "economic coercion",
    "financial sanctions", "financial restrictions",
    "swift ban", "correspondent banking",
    "oil embargo", "arms embargo",
    "unilateral sanctions", "multilateral sanctions",
    "un sanctions", "eu sanctions", "us sanctions",
    "raft of sanctions", "wave of sanctions",
    "sanction regime", "sanctions package",
    "countermeasures", "retaliatory tariffs",
})

ECONOMY_KEYWORDS: frozenset[str] = frozenset({
    "economy", "economic", "economics",
    "trade", "trade war", "trade dispute", "trade deal",
    "tariff", "tariffs", "import duty", "customs",
    "gdp", "growth rate", "recession", "inflation",
    "currency", "exchange rate", "devaluation",
    "investment", "foreign investment", "fdi",
    "debt", "debt crisis", "sovereign debt",
    "aid", "foreign aid", "development aid",
    "imf", "world bank", "wto",
    "supply chain", "global supply chain",
    "commodities", "oil prices", "gas prices",
    "energy security", "energy crisis",
    "food security", "food crisis", "famine",
    "poverty", "inequality", "unemployment",
    "financial crisis", "banking crisis", "bank run",
    "market crash", "stock market",
    "covid economic impact", "pandemic economy",
})

# ─────────────────────────────────────────────────────────────────────────────
# HUMANITARIAN / REFUGEES
# ─────────────────────────────────────────────────────────────────────────────

REFUGEE_KEYWORDS: frozenset[str] = frozenset({
    "refugee", "refugees", "refugee crisis",
    "displaced", "displacement", "internally displaced",
    "idp", "idps", "asylum seeker", "asylum seekers",
    "migrant", "migrants", "migration", "mass migration",
    "forced displacement", "forced migration",
    "exodus", "mass exodus", "flee", "fleeing", "fled",
    "camp", "refugee camp", "displacement camp",
    "unhcr", "un refugee agency",
    "safe passage", "humanitarian corridor",
    "resettlement", "voluntary return",
    "stateless", "statelessness",
    "border crossing", "irregular migration",
    "trafficking", "human trafficking", "smuggling",
})

DISASTER_KEYWORDS: frozenset[str] = frozenset({
    "disaster", "disasters", "catastrophe", "catastrophic",
    "earthquake", "earthquakes", "aftershock",
    "tsunami", "flood", "floods", "flooding",
    "hurricane", "typhoon", "cyclone", "tornado",
    "wildfire", "wildfire outbreak", "fire",
    "drought", "famine", "food shortage",
    "epidemic", "pandemic", "outbreak",
    "disease", "virus", "pathogen",
    "infrastructure collapse", "dam break", "dam failure",
    "humanitarian crisis", "humanitarian emergency",
    "aid worker", "aid workers", "relief effort",
    "emergency response", "rescue operation", "search and rescue",
    "evacuation", "evacuated", "evacuees",
    "death toll", "missing persons",
    "climate disaster", "climate emergency",
    "heat wave", "extreme weather",
})

# ─────────────────────────────────────────────────────────────────────────────
# ELECTIONS / GOVERNANCE
# ─────────────────────────────────────────────────────────────────────────────

ELECTION_KEYWORDS: frozenset[str] = frozenset({
    "election", "elections", "electoral", "electorate",
    "vote", "votes", "voting", "voter", "voters",
    "ballot", "ballots", "ballot box", "polling station",
    "parliamentary election", "presidential election",
    "general election", "by-election", "runoff",
    "referendum", "referendums", "plebiscite",
    "election result", "election outcome",
    "election fraud", "vote rigging", "election interference",
    "disinformation campaign", "election manipulation",
    "opposition", "incumbent", "candidate", "candidates",
    "poll", "polls", "opinion poll",
    "parliament", "parliamentary", "legislature",
    "congress", "senate", "assembly",
    "political party", "coalition", "majority", "minority",
    "democracy", "democratic", "autocracy", "authoritarian",
    "political transition", "power transfer",
    "inauguration", "swearing in",
    "term limit", "constitutional change",
    "political crisis", "political deadlock", "political turmoil",
})

# ─────────────────────────────────────────────────────────────────────────────
# BORDERS / TERRITORY
# ─────────────────────────────────────────────────────────────────────────────

BORDER_KEYWORDS: frozenset[str] = frozenset({
    "border", "borders", "border dispute", "border tension",
    "border crossing", "border closure", "border skirmish",
    "frontier", "frontiers", "boundary", "boundaries",
    "demarcation line", "line of control", "loc",
    "no man's land", "buffer zone",
    "territorial dispute", "territorial claim", "contested territory",
    "sovereign territory", "territorial integrity",
    "checkpoint", "checkpoints", "border checkpoint",
    "no-fly zone", "exclusion zone",
    "territorial waters", "maritime boundary",
    "airspace", "airspace violation",
    "enclave", "exclave",
    "disputed region", "occupied territory",
    "self-determination", "secession", "secessionist",
    "independence", "independence movement",
})

# ─────────────────────────────────────────────────────────────────────────────
# COMBINED / CROSS-CUTTING COMPOSITE SETS
# ─────────────────────────────────────────────────────────────────────────────

# All terms that, when found in a "conflict" headline, should elevate
# severity to CRITICAL.
CRITICAL_SEVERITY_TRIGGERS: frozenset[str] = frozenset().union(
    MISSILE_KEYWORDS,
    AIRSTRIKE_KEYWORDS,
    TERRORISM_KEYWORDS,
    NUCLEAR_KEYWORDS,
    WEAPON_KEYWORDS,
    {
        "war", "warfare", "warzone",
        "invasion", "invade",
        "explosion", "blast", "detonation",
        "massacre", "genocide",
        "biological weapon", "chemical weapon", "wmd",
    },
)

# Combined conflict vocabulary (used for fast category detection)
ALL_CONFLICT_KEYWORDS: frozenset[str] = frozenset().union(
    CONFLICT_KEYWORDS,
    INSURGENCY_KEYWORDS,
    TERRORISM_KEYWORDS,
    COUP_KEYWORDS,
    MILITARY_KEYWORDS,
    NAVAL_KEYWORDS,
    AIRSTRIKE_KEYWORDS,
    MISSILE_KEYWORDS,
    WEAPON_KEYWORDS,
    SHELLING_KEYWORDS,
    CASUALTY_KEYWORDS,
    NUCLEAR_KEYWORDS,
    CYBER_KEYWORDS,
)

# Combined protest / civil-unrest vocabulary
ALL_PROTEST_KEYWORDS: frozenset[str] = frozenset().union(
    PROTEST_KEYWORDS,
)

# Combined "normal" / non-threat vocabulary
ALL_NORMAL_KEYWORDS: frozenset[str] = frozenset().union(
    DIPLOMACY_KEYWORDS,
    CEASEFIRE_KEYWORDS,
    PEACE_KEYWORDS,
    ECONOMY_KEYWORDS,
    ELECTION_KEYWORDS,
    DISASTER_KEYWORDS,
    REFUGEE_KEYWORDS,
)

# ─────────────────────────────────────────────────────────────────────────────
# EXPLANATION GROUPS
# Each group maps to a human-readable intelligence sentence.
# Services should iterate over these to generate analyst explanations.
# ─────────────────────────────────────────────────────────────────────────────

CONFLICT_EXPLANATION_GROUPS: list[tuple[frozenset[str], str]] = [
    (MISSILE_KEYWORDS,       "Missile or projectile terminology detected"),
    (AIRSTRIKE_KEYWORDS,     "Aerial strike language identified"),
    (SHELLING_KEYWORDS,      "Heavy weapons and shelling terminology detected"),
    (TERRORISM_KEYWORDS,     "Terrorism-related language detected"),
    (NUCLEAR_KEYWORDS,       "Nuclear or WMD language detected"),
    (CYBER_KEYWORDS,         "Cyberattack or cyber warfare language identified"),
    (MILITARY_KEYWORDS,      "Military deployment or force language detected"),
    (NAVAL_KEYWORDS,         "Naval confrontation terminology identified"),
    (WEAPON_KEYWORDS,        "Weapons or armament terminology detected"),
    (INSURGENCY_KEYWORDS,    "Insurgency or guerrilla activity language identified"),
    (COUP_KEYWORDS,          "Coup or governmental overthrow language detected"),
    (CASUALTY_KEYWORDS,      "Casualty or human loss language present"),
    (CONFLICT_KEYWORDS,      "Active conflict or warfare language identified"),
    (BORDER_KEYWORDS,        "Border conflict or territorial dispute context found"),
    (SANCTION_KEYWORDS,      "Sanctions or economic pressure language detected"),
]

PROTEST_EXPLANATION_GROUPS: list[tuple[frozenset[str], str]] = [
    (PROTEST_KEYWORDS,       "Protest activity language identified"),
    (
        frozenset({"demonstration", "demonstrators", "demonstrating",
                   "public demonstration", "street demonstration"}),
        "Public demonstration context found",
    ),
    (
        frozenset({"march", "marches", "marchers", "marching",
                   "solidarity march"}),
        "Organized march or solidarity action detected",
    ),
    (
        frozenset({"riot", "riots", "rioting", "rioters",
                   "civil unrest", "public disorder"}),
        "Civil unrest or riot indicators present",
    ),
    (
        frozenset({"crackdown", "dispersal", "tear gas", "pepper spray",
                   "water cannon", "rubber bullet", "riot police"}),
        "Security force crackdown language detected",
    ),
    (
        frozenset({"strike", "walkout", "work stoppage", "general strike",
                   "labor action", "labour action", "picket", "boycott"}),
        "Industrial or civil action language detected",
    ),
    (
        frozenset({"sit-in", "blockade", "blockades", "civil disobedience",
                   "hunger strike", "non-violent resistance"}),
        "Non-violent resistance methodology identified",
    ),
    (
        frozenset({"activist", "activists", "campaigner", "campaigners",
                   "organiser", "organizer", "grassroots"}),
        "Activist or organized movement language detected",
    ),
    (
        frozenset({"demands", "petition", "grievance", "grievances"}),
        "Grievance and demand language identified",
    ),
    (
        frozenset({"uprising", "uprisings", "revolt", "revolts",
                   "anti-government", "pro-democracy"}),
        "Uprising or political opposition language detected",
    ),
]

NORMAL_EXPLANATION_GROUPS: list[tuple[frozenset[str], str]] = [
    (
        frozenset({"agreement", "agreements", "treaty", "treaties", "accord",
                   "accords", "deal", "pact", "joint statement"}),
        "Diplomatic agreement language found",
    ),
    (
        frozenset({"summit", "summits", "talks", "negotiations", "dialogue",
                   "meeting", "meetings", "conference", "high-level talks"}),
        "Diplomatic engagement context detected",
    ),
    (CEASEFIRE_KEYWORDS, "Ceasefire or peace process language identified"),
    (PEACE_KEYWORDS,     "Peace or reconciliation language found"),
    (ECONOMY_KEYWORDS,   "Economic context identified"),
    (
        frozenset({"growth", "development", "expansion", "investment",
                   "gdp", "trade deal"}),
        "Positive economic development language present",
    ),
    (
        frozenset({"festival", "celebration", "cultural", "heritage",
                   "commemorat"}),
        "Cultural event or celebration language detected",
    ),
    (
        frozenset({"education", "school", "university", "scholarship",
                   "research"}),
        "Education or research sector context found",
    ),
    (DISASTER_KEYWORDS,  "Humanitarian or disaster response language found"),
    (REFUGEE_KEYWORDS,   "Refugee or displacement context identified"),
    (ELECTION_KEYWORDS,  "Political process or electoral language identified"),
    (DIPLOMACY_KEYWORDS, "Diplomatic process language detected"),
    (SANCTION_KEYWORDS,  "Sanction or economic pressure context present"),
]

# ─────────────────────────────────────────────────────────────────────────────
# REGION VOCABULARY
# Each region maps to an extended list of lowercase markers.
# ─────────────────────────────────────────────────────────────────────────────

REGION_KEYWORDS: dict[str, list[str]] = {
    "Middle East": [
        # Countries
        "israel", "israeli", "israelis",
        "palestine", "palestinian", "palestinians",
        "gaza", "west bank", "ramallah",
        "iran", "iranian", "tehran", "isfahan", "mashhad",
        "iraq", "iraqi", "baghdad", "mosul", "basra", "erbil",
        "syria", "syrian", "damascus", "aleppo", "idlib", "raqqa",
        "lebanon", "lebanese", "beirut",
        "saudi arabia", "saudi", "riyadh", "jeddah",
        "yemen", "yemeni", "sanaa", "houthi", "houthis",
        "jordan", "jordanian", "amman",
        "egypt", "egyptian", "cairo", "sinai",
        "turkey", "turkish", "ankara", "istanbul", "erdogan",
        "qatar", "doha",
        "kuwait", "kuwait city",
        "bahrain", "manama",
        "oman", "muscat",
        "uae", "dubai", "abu dhabi", "emirates",
        "libya", "libyan", "tripoli", "benghazi",
        "tunisia", "tunisian",
        "morocco", "moroccan", "rabat",
        "algeria", "algerian", "algiers",
        "sudan", "sudanese", "khartoum",
        # Geopolitical actors/concepts
        "hezbollah", "hamas", "islamic jihad",
        "irgc", "quds force", "revolutionary guard",
        "arab league", "opec", "gulf cooperation council", "gcc",
        "strait of hormuz", "persian gulf", "arabian peninsula",
        "sinai peninsula", "golan heights", "jerusalem",
    ],
    "South Asia": [
        # Countries
        "india", "indian", "indians", "delhi", "new delhi",
        "mumbai", "kolkata", "bangalore", "hyderabad", "chennai",
        "pakistan", "pakistani", "islamabad", "karachi", "lahore",
        "rawalpindi", "peshawar", "quetta",
        "afghanistan", "afghan", "afghans", "kabul", "kandahar",
        "helmand", "kunduz",
        "bangladesh", "bangladeshi", "dhaka", "chittagong",
        "sri lanka", "sri lankan", "colombo",
        "nepal", "nepali", "kathmandu",
        "bhutan", "thimphu",
        "maldives", "malé",
        "myanmar", "burmese", "yangon", "naypyidaw", "rohingya",
        # Geopolitical actors/concepts
        "kashmir", "line of control", "loc kashmir",
        "indo-pakistan", "india-china", "india-pakistan",
        "saarc", "belt and road", "china-pakistan",
        "isi", "cia pakistan",
        "quadrilateral security", "quad",
    ],
    "East Asia": [
        # Countries
        "china", "chinese", "beijing", "shanghai", "shenzhen",
        "guangzhou", "xi jinping", "ccp", "prc",
        "taiwan", "taiwanese", "taipei",
        "japan", "japanese", "tokyo", "osaka",
        "south korea", "korean", "seoul", "busan",
        "north korea", "dprk", "pyongyang", "kim jong-un",
        "mongolia", "ulaanbaatar",
        "hong kong",
        "macau",
        # Geopolitical actors/concepts
        "south china sea", "taiwan strait", "east china sea",
        "disputed islands", "diaoyu", "senkaku", "spratly",
        "paracel islands",
        "asean", "apec",
        "korean peninsula", "demilitarized zone", "dmz korea",
        "ballistic missile test", "icbm launch",
    ],
    "Europe": [
        # Countries
        "ukraine", "ukrainian", "kyiv", "kharkiv", "kherson",
        "mariupol", "dnipro", "zaporizhzhia", "odesa",
        "russia", "russian", "russians", "moscow", "kremlin",
        "putin", "st. petersburg", "volgograd", "rostov",
        "france", "french", "paris", "marseille", "macron",
        "germany", "german", "berlin", "munich", "hamburg",
        "uk", "britain", "british", "england", "london",
        "scotland", "wales", "sunak", "boris johnson",
        "poland", "polish", "warsaw", "krakow",
        "italy", "italian", "rome", "milan",
        "spain", "spanish", "madrid", "barcelona",
        "greece", "greek", "athens",
        "serbia", "serbian", "belgrade",
        "kosovo", "pristina",
        "bulgaria", "bucharest", "romania",
        "hungary", "budapest", "orban",
        "czech republic", "prague",
        "slovakia", "bratislava",
        "finland", "helsinki",
        "sweden", "stockholm",
        "norway", "oslo",
        "denmark", "copenhagen",
        "netherlands", "amsterdam", "the hague",
        "belgium", "brussels",
        "switzerland", "zurich", "bern",
        "austria", "vienna",
        "moldova", "chisinau", "transnistria",
        "belarus", "belarusian", "minsk", "lukashenko",
        "baltic states", "estonia", "latvia", "lithuania",
        "balkans", "western balkans",
        # Geopolitical actors/concepts
        "nato", "european union", "council of europe",
        "osce", "imf europe",
        "schwarzmeer", "black sea", "baltic sea",
        "donbas", "donbass", "donetsk", "luhansk",
        "crimea", "crimean", "kerch bridge",
        "wagner", "wagner group", "prigozhin",
        "nordstream", "nord stream",
    ],
    "Africa": [
        # Countries / regions
        "nigeria", "nigerian", "abuja", "lagos",
        "ethiopia", "ethiopian", "addis ababa", "tigray", "amhara",
        "somalia", "somali", "mogadishu",
        "kenya", "nairobi",
        "south africa", "johannesburg", "cape town", "pretoria",
        "democratic republic of congo", "drc", "kinshasa",
        "congo", "congolese",
        "mali", "malian", "bamako",
        "burkina faso", "ouagadougou",
        "niger", "niamey",
        "sahel",
        "central african republic", "car", "bangui",
        "chad", "n'djamena",
        "mozambique", "maputo",
        "zimbabwe", "harare",
        "angola", "luanda",
        "cameroon", "yaounde",
        "ghana", "accra",
        "senegal", "dakar",
        "ivory coast", "abidjan",
        "libya", "libyan",
        "sudan", "south sudan", "juba",
        # Geopolitical actors/concepts
        "african union", "ecowas", "igad",
        "al-shabaab", "boko haram", "isis-k sahel",
        "sahel crisis", "sahelian",
    ],
    "Latin America": [
        # Countries
        "mexico", "mexican", "mexico city",
        "colombia", "colombian", "bogota", "medellin",
        "venezuela", "venezuelan", "caracas", "maduro",
        "brazil", "brazilian", "brasilia", "são paulo", "rio",
        "argentina", "argentina", "buenos aires",
        "chile", "chilean", "santiago",
        "peru", "peruvian", "lima",
        "bolivia", "la paz",
        "ecuador", "quito",
        "cuba", "havana", "cubano",
        "nicaragua", "managua", "ortega",
        "haiti", "port-au-prince",
        "honduras", "tegucigalpa",
        "el salvador", "san salvador", "bukele",
        "guatemala", "guatemala city",
        "panama", "panama city",
        "paraguay", "asuncion",
        "uruguay", "montevideo",
        # Geopolitical concepts
        "cartels", "narco", "drug trafficking",
        "gang violence", "gang warfare",
        "farc", "eln", "sendero",
        "oas", "mercosur", "celac",
    ],
    "Central Asia": [
        "kazakhstan", "kazakhstani", "nur-sultan", "astana", "almaty",
        "uzbekistan", "uzbek", "tashkent",
        "kyrgyzstan", "kyrgyz", "bishkek",
        "tajikistan", "tajik", "dushanbe",
        "turkmenistan", "turkmen", "ashgabat",
        "azerbaijan", "azerbaijani", "baku",
        "armenia", "armenian", "yerevan", "nagorno-karabakh",
        "georgia", "georgian", "tbilisi", "abkhazia",
        "csto", "sco", "shanghai cooperation",
        "caspian sea",
    ],
    "USA": [
        # Political / governmental
        "united states", "usa", "u.s.", "us government", "us military",
        "america", "american", "americans",
        "washington", "washington dc", "white house",
        "pentagon", "state department", "cia", "fbi",
        "congress", "senate", "house of representatives",
        "president biden", "president trump", "biden", "trump",
        "democrat", "republican",
        # Cities / states
        "new york", "california", "texas", "florida", "chicago",
        "los angeles", "san francisco", "houston", "dallas",
        "miami", "boston", "seattle", "atlanta", "phoenix",
        "wall street", "silicon valley",
        # Concepts / agencies
        "department of defense", "dod",
        "homeland security", "nsa",
        "federal reserve", "fed",
        "us sanctions", "us troops", "us forces",
        "us navy", "us army", "us air force", "us marines",
    ],
}
