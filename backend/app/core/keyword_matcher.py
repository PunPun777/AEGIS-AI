"""
keyword_matcher.py
------------------
Reusable geopolitical keyword matching engine for AEGIS-AI.

This module is the single place where all text-scanning logic lives.
Every service that needs to detect geopolitical signals should call
these helpers rather than implementing its own iteration.

Capabilities
------------
- Case-insensitive matching
- Multi-word phrase matching  ("military exercise", "exchange of fire")
- Compound and hyphenated phrase matching ("state-sponsored", "air defence")
- Longest-phrase priority  — if "missile barrage" matches, "missile" alone
  is NOT counted as an additional independent match for that span.
- Covered-span deduplication — overlapping shorter matches are suppressed.
- Category scoring — returns a normalised score [0.0, 1.0] per category.
- Confidence contribution — maps match density to a confidence delta.

Public API
----------
    match_phrases(text, vocabulary)         -> list[str]
    has_match(text, vocabulary)             -> bool
    match_explanation_groups(text, groups)  -> list[str]
    score_categories(text, category_map)    -> dict[str, float]
    build_match_result(text, groups, ...)   -> MatchResult

All functions are stateless and thread-safe.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from functools import lru_cache


# ─────────────────────────────────────────────────────────────────────────────
# Data structures
# ─────────────────────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class _Span:
    """A half-open [start, end) character interval in the normalised text."""
    start: int
    end: int

    def overlaps(self, other: "_Span") -> bool:
        return self.start < other.end and other.start < self.end


@dataclass
class MatchResult:
    """
    Structured output from a full keyword match pass.

    Attributes
    ----------
    matched_phrases : list[str]
        All distinct phrases found in the text, longest-first, deduplicated.
    categories : list[str]
        Names of the categories that contributed at least one match.
    sentences : list[str]
        Human-readable analyst sentences (from explanation groups).
    score : float
        Aggregate signal strength in [0.0, 1.0].  Derived from the number of
        distinct category hits relative to total categories inspected.
    category_scores : dict[str, float]
        Per-category signal strength in [0.0, 1.0].
    """
    matched_phrases: list[str] = field(default_factory=list)
    categories: list[str] = field(default_factory=list)
    sentences: list[str] = field(default_factory=list)
    score: float = 0.0
    category_scores: dict[str, float] = field(default_factory=dict)

    def __bool__(self) -> bool:
        return bool(self.matched_phrases)


# ─────────────────────────────────────────────────────────────────────────────
# Internal helpers
# ─────────────────────────────────────────────────────────────────────────────

def _normalise(text: str) -> str:
    """Lowercase and collapse whitespace for consistent matching."""
    return re.sub(r"\s+", " ", text.lower().strip())


@lru_cache(maxsize=256)
def _sorted_vocab(vocabulary: frozenset[str]) -> tuple[str, ...]:
    """
    Return vocabulary items sorted by descending length.

    Longest phrases are tried first so that "missile barrage" is matched
    before its sub-phrase "missile", suppressing the shorter hit.

    Result is cached per vocabulary frozenset for performance.
    """
    return tuple(sorted(vocabulary, key=len, reverse=True))


def _find_all_spans(norm_text: str, phrase: str) -> list[_Span]:
    """Return all non-overlapping occurrences of phrase in norm_text."""
    spans: list[_Span] = []
    start = 0
    while True:
        pos = norm_text.find(phrase, start)
        if pos == -1:
            break
        spans.append(_Span(pos, pos + len(phrase)))
        start = pos + 1   # allow overlapping occurrences to be found
    return spans


def _is_covered(span: _Span, covered: list[_Span]) -> bool:
    """Return True if span is fully contained within any covered span."""
    return any(c.start <= span.start and span.end <= c.end for c in covered)


# ─────────────────────────────────────────────────────────────────────────────
# Core matching
# ─────────────────────────────────────────────────────────────────────────────

def match_phrases(text: str, vocabulary: frozenset[str]) -> list[str]:
    """
    Find all vocabulary phrases present in text, applying longest-phrase
    priority and covered-span deduplication.

    Parameters
    ----------
    text : str
        Raw (mixed-case) input text.
    vocabulary : frozenset[str]
        Flat set of lowercase candidate phrases (single or multi-word).

    Returns
    -------
    list[str]
        Matched phrases in order of descending length, no duplicates.
        Shorter sub-phrases that are fully covered by a longer match are
        excluded.

    Examples
    --------
    >>> vocab = frozenset({"missile", "missile barrage", "barrage"})
    >>> match_phrases("A missile barrage hit the city", vocab)
    ['missile barrage']
    """
    norm = _normalise(text)
    sorted_terms = _sorted_vocab(vocabulary)

    covered: list[_Span] = []
    matched: list[str] = []
    seen: set[str] = set()

    for phrase in sorted_terms:
        if phrase in seen:
            continue
        for span in _find_all_spans(norm, phrase):
            if _is_covered(span, covered):
                continue
            # Accept this match — cover its span and record the phrase
            covered.append(span)
            if phrase not in seen:
                matched.append(phrase)
                seen.add(phrase)

    return matched


def has_match(text: str, vocabulary: frozenset[str]) -> bool:
    """
    Return True if any vocabulary phrase is present in text.

    Optimised early-exit version — stops on the first match found,
    prioritising longer phrases.

    Parameters
    ----------
    text : str
        Raw (mixed-case) input text.
    vocabulary : frozenset[str]
        Flat set of lowercase candidate phrases.

    Returns
    -------
    bool
    """
    norm = _normalise(text)
    for phrase in _sorted_vocab(vocabulary):
        if phrase in norm:
            return True
    return False


# ─────────────────────────────────────────────────────────────────────────────
# Explanation-group matching
# ─────────────────────────────────────────────────────────────────────────────

def match_explanation_groups(
    text: str,
    groups: list[tuple[frozenset[str], str]],
) -> list[str]:
    """
    Iterate over explanation groups and return analyst sentences for every
    group that contains at least one match in text.

    Each group is a ``(vocabulary, sentence)`` pair.  Matching within each
    group uses longest-phrase priority so compound expressions ("exchange of
    fire") take precedence over single tokens.

    Parameters
    ----------
    text : str
        Raw input text.
    groups : list[tuple[frozenset[str], str]]
        Ordered list of (vocabulary frozenset, analyst sentence) pairs.

    Returns
    -------
    list[str]
        Ordered list of distinct analyst sentences for matched groups.
    """
    norm = _normalise(text)
    sentences: list[str] = []
    seen_sentences: set[str] = set()

    for vocabulary, sentence in groups:
        if sentence in seen_sentences:
            continue
        # Use longest-phrase priority within each group's vocabulary
        for phrase in _sorted_vocab(vocabulary):
            if phrase in norm:
                sentences.append(sentence)
                seen_sentences.add(sentence)
                break   # one match per group is sufficient

    return sentences


# ─────────────────────────────────────────────────────────────────────────────
# Category scoring
# ─────────────────────────────────────────────────────────────────────────────

def score_categories(
    text: str,
    category_map: dict[str, frozenset[str]],
    weights: dict[str, float] | None = None,
) -> dict[str, float]:
    """
    Score text against named vocabulary categories.

    For each category, a score in [0.0, 1.0] is produced by counting how many
    distinct phrases from the category vocabulary match the text, then
    normalising against a soft cap (``_SCORE_CAP`` matches = 1.0 score).

    Parameters
    ----------
    text : str
        Raw input text.
    category_map : dict[str, frozenset[str]]
        Mapping of category label → vocabulary frozenset.
    weights : dict[str, float] | None
        Optional per-category multipliers applied after normalisation.
        Values outside [0, 1] are clamped.

    Returns
    -------
    dict[str, float]
        Mapping of category label → score in [0.0, 1.0].
    """
    _SCORE_CAP = 5   # number of distinct phrase matches that produce score 1.0

    scores: dict[str, float] = {}
    for category, vocabulary in category_map.items():
        hits = match_phrases(text, vocabulary)
        raw = len(hits) / _SCORE_CAP
        base = min(raw, 1.0)
        w = 1.0 if weights is None else max(0.0, min(1.0, weights.get(category, 1.0)))
        scores[category] = round(base * w, 4)
    return scores


def aggregate_score(category_scores: dict[str, float]) -> float:
    """
    Derive a single aggregate signal score from per-category scores.

    Uses the maximum category score as the aggregate, biased upward when
    multiple categories contribute simultaneously.

    Parameters
    ----------
    category_scores : dict[str, float]
        Output of ``score_categories``.

    Returns
    -------
    float
        Score in [0.0, 1.0].
    """
    if not category_scores:
        return 0.0
    values = list(category_scores.values())
    peak = max(values)
    active = sum(1 for v in values if v > 0)
    # Each additional active category adds a small boost (max +0.2 combined)
    boost = min(0.2, (active - 1) * 0.04) if active > 1 else 0.0
    return round(min(1.0, peak + boost), 4)


# ─────────────────────────────────────────────────────────────────────────────
# Comprehensive result builder
# ─────────────────────────────────────────────────────────────────────────────

def build_match_result(
    text: str,
    groups: list[tuple[frozenset[str], str]],
    category_map: dict[str, frozenset[str]] | None = None,
    category_weights: dict[str, float] | None = None,
) -> MatchResult:
    """
    Run the full matching pipeline and return a structured ``MatchResult``.

    Parameters
    ----------
    text : str
        Raw input text.
    groups : list[tuple[frozenset[str], str]]
        Explanation groups for this prediction class.
    category_map : dict[str, frozenset[str]] | None
        Optional named category vocabularies for scoring.  When provided,
        ``MatchResult.category_scores`` and ``.score`` are populated.
    category_weights : dict[str, float] | None
        Optional per-category weights forwarded to ``score_categories``.

    Returns
    -------
    MatchResult
    """
    # 1. Analyst sentences from explanation groups
    sentences = match_explanation_groups(text, groups)

    # 2. All raw matched phrases (flat, across the union of all group vocabs)
    union_vocab: frozenset[str] = frozenset().union(
        *(vocab for vocab, _ in groups)
    )
    all_phrases = match_phrases(text, union_vocab)

    # 3. Category scoring (optional)
    cat_scores: dict[str, float] = {}
    agg_score = 0.0
    active_categories: list[str] = []

    if category_map:
        cat_scores = score_categories(text, category_map, category_weights)
        agg_score = aggregate_score(cat_scores)
        active_categories = [c for c, s in cat_scores.items() if s > 0]

    return MatchResult(
        matched_phrases=all_phrases,
        categories=active_categories,
        sentences=sentences,
        score=agg_score,
        category_scores=cat_scores,
    )
