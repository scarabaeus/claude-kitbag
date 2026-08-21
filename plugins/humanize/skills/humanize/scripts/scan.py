#!/usr/bin/env python3
"""Mechanical quick-scan for common AI-writing tells. Advisory only:
read the report as signal to investigate, not a verdict to act on."""

import re
import statistics
import sys

BLOCKLIST = [
    "delve", "leverage", "navigate", "elevate", "intricate", "meticulously",
    "synergy", "empower", "landscape", "ecosystem", "underscore", "seamless",
    "robust", "game-changer", "crucial", "pivotal", "testament", "tapestry",
    "showcasing", "boasts", "vibrant", "garner", "fostering",
    "additionally", "bolstered", "enduring", "interplay", "groundbreaking",
    "renowned", "diverse array", "profound", "exemplifies", "commitment to",
    "nestled", "dive into", "here's the kicker", "making waves",
    "in the heart of", "serves as", "stands as", "in connection with",
    "associated with",
]

PARTICIPLES = [
    "highlighting", "underscoring", "fostering", "ensuring", "reflecting",
    "contributing to", "encompassing", "enhancing",
]

NEGATIVE_PARALLELISM_PATTERNS = [
    re.compile(r"\bit'?s\s+not\s+[^.?!]+,?\s+it'?s\b", re.IGNORECASE),
    re.compile(r"\bnot\s+just\s+[^,.\n]+,\s*(?:but\s+)?(?:also\s+)?", re.IGNORECASE),
    re.compile(r"\bnot\s+[^,.\n]+,\s+but\s+", re.IGNORECASE),
]

EMOJI_PATTERN = re.compile(
    "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF]"
)
SMART_QUOTE_CHARS = "‘’“”"

STOPWORDS = set("""
a an the and or but if of in on at to for with without from by as is are
was were be been being this that these those it its it's not just so than
then there here what which who whom whose when where why how
""".split())


def read_input():
    if len(sys.argv) > 1 and sys.argv[1] != "-":
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            return f.read()
    return sys.stdin.read()


def find_blocklist_hits(lines):
    hits = {}
    for lineno, line in enumerate(lines, start=1):
        lower = line.lower()
        for term in BLOCKLIST:
            count = lower.count(term)
            if count:
                entry = hits.setdefault(term, {"count": 0, "lines": []})
                entry["count"] += count
                entry["lines"].append(lineno)
    return hits


def find_negative_parallelism(text, lines):
    matches = []
    for pattern in NEGATIVE_PARALLELISM_PATTERNS:
        for m in pattern.finditer(text):
            lineno = text.count("\n", 0, m.start()) + 1
            snippet = m.group(0).strip()
            matches.append((lineno, snippet))
    return matches


def find_rule_of_three(sentences):
    hits = 0
    for sentence in sentences:
        parts = re.split(r",\s*(?:and\s+)?|\s+and\s+", sentence.strip())
        parts = [p for p in parts if len(p.split()) >= 2]
        if len(parts) == 3:
            hits += 1
    return hits


def split_sentences(text):
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    raw = re.split(r"(?<=[.!?])\s+", text)
    return [s for s in raw if s.strip()]


def find_participle_tacking(text):
    matches = []
    for term in PARTICIPLES:
        pattern = re.compile(r",\s*" + re.escape(term) + r"\b", re.IGNORECASE)
        for m in pattern.finditer(text):
            lineno = text.count("\n", 0, m.start()) + 1
            matches.append((lineno, term))
    return matches


def find_paragraph_openers(text):
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]
    openers = []
    for para in paragraphs:
        para_sentences = split_sentences(para)
        if para_sentences:
            openers.append(para_sentences[0])
    return openers


def significant_words(sentence):
    words = re.findall(r"[a-zA-Z']+", sentence.lower())
    return {w for w in words if w not in STOPWORDS and len(w) > 3}


def main():
    text = read_input()
    lines = text.splitlines() or [text]
    words = text.split()
    word_count = len(words)
    sentences = split_sentences(text)
    sentence_lengths = [len(s.split()) for s in sentences]

    print("=== humanize scan report ===")
    print(f"Words: {word_count}   Sentences: {len(sentences)}")
    print()

    blocklist_hits = find_blocklist_hits(lines)
    total_hits = sum(v["count"] for v in blocklist_hits.values())
    print(f"Blocklist hits ({total_hits}):")
    if blocklist_hits:
        for term, info in sorted(blocklist_hits.items(), key=lambda kv: -kv[1]["count"]):
            line_list = ", ".join(f"line {n}" for n in info["lines"][:5])
            print(f"  {term:<20} x{info['count']}   ({line_list})")
    else:
        print("  none")
    print()

    em_dash_count = text.count("—") + text.count("--")
    density = (em_dash_count / word_count * 100) if word_count else 0
    if density > 1.0:
        flag = "  -- high"
    elif em_dash_count > 0:
        flag = "  -- present (casual human writing usually has zero; treat any as a tell)"
    else:
        flag = ""
    print(f"Em dashes: {em_dash_count}  (density: {density:.2f} per 100 words){flag}")
    print()

    neg_parallel = find_negative_parallelism(text, lines)
    print(f'"Not X, but Y" constructions: {len(neg_parallel)}')
    for lineno, snippet in neg_parallel[:10]:
        print(f"  - line {lineno}: \"{snippet}\"")
    print()

    rule_of_three = find_rule_of_three(sentences)
    print(f"Rule-of-three lists detected: {rule_of_three}")
    print()

    if len(sentence_lengths) >= 2:
        mean = statistics.mean(sentence_lengths)
        stdev = statistics.stdev(sentence_lengths)
        uniform_flag = ""
        if mean and stdev / mean < 0.25:
            uniform_flag = "  -- low variance: sentences are unusually uniform in length"
        print(
            f"Sentence length: mean {mean:.1f} words, stdev {stdev:.1f} "
            f"(min {min(sentence_lengths)}, max {max(sentence_lengths)}){uniform_flag}"
        )
    else:
        print("Sentence length: not enough sentences to compute variance")
    print()

    participle_hits = find_participle_tacking(text)
    print(f"Present-participle tacking: {len(participle_hits)} instances")
    for lineno, term in participle_hits[:10]:
        print(f"  - line {lineno}: \", {term}...\"")
    print()

    openers = find_paragraph_openers(text)
    print(f"Paragraph openers ({len(openers)}):")
    for i, opener in enumerate(openers, start=1):
        trimmed = opener if len(opener) <= 80 else opener[:77] + "..."
        print(f"  {i}. {trimmed}")
    if len(openers) >= 3:
        print("  -- eyeball these for a repeated shape (e.g. every paragraph opening")
        print("     with a short flat declarative claim); that's a tell on its own")
    print()

    if len(sentences) >= 2:
        first_words = significant_words(sentences[0])
        last_words = significant_words(sentences[-1])
        shared = sorted(first_words & last_words)
        flag = "  -- possible circular closer" if len(shared) >= 2 else ""
        print(f"First/last sentence shared significant words: {len(shared)}{flag}")
        if shared:
            print(f"  shared: {', '.join(shared)}")
        print()

    emoji_count = len(EMOJI_PATTERN.findall(text))
    smart_quote_count = sum(text.count(c) for c in SMART_QUOTE_CHARS)
    bold_count = len(re.findall(r"\*\*[^*]+\*\*", text))
    hr_count = len(re.findall(r"^\s*(?:---+|\*\*\*+|___+)\s*$", text, re.MULTILINE))
    header_count = len(re.findall(r"^#{1,6}\s", text, re.MULTILINE))
    title_case_headers = 0
    for m in re.finditer(r"^#{1,6}\s+(.+)$", text, re.MULTILINE):
        heading = m.group(1).strip()
        words_in_heading = [w for w in heading.split() if w.isalpha()]
        if len(words_in_heading) >= 3 and all(w[0:1].isupper() for w in words_in_heading):
            title_case_headers += 1
    print(
        f"Formatting: {emoji_count} emoji, {smart_quote_count} smart-quote chars, "
        f"{bold_count} bold spans, {hr_count} horizontal rule(s), "
        f"{header_count} header(s) ({title_case_headers} title-case)"
    )

    print("=== end report ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
