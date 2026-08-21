---
name: humanize
description: Use when the user explicitly asks to "humanize" text, remove "AI slop"/"AI-isms", make writing sound more human or less robotic/formulaic, or asks Claude to write in this style from the start of a task (e.g. "write this like a human would," "use the humanize skill"). Applies to emails, docs, posts, messages, or any prose meant for other people, whether the text already exists (Claude's own prior output or user-pasted text) or is about to be drafted. Do not trigger automatically on ordinary writing requests without an explicit ask — only when the user names this specific goal.
---

# Humanize

## When this applies

Only when explicitly asked for. Three equally valid triggers:

1. Claude just generated text and is asked to revise it with this skill.
2. Claude is told up front to write this way, before any draft exists.
3. The user pastes existing (often AI-generated) text and asks for a rewrite.

The procedure below is the same regardless of which of these triggered it.
Don't apply this skill's checklist to ordinary writing requests that didn't
ask for it — plenty of legitimate writing uses words like "crucial" on
purpose.

## What this targets

This is about writing quality and voice — making prose read the way a person
actually writes, not the generic, over-hedged, formulaic register that AI
text defaults to. The checklist in `reference.md` happens to overlap heavily
with what ML AI-detectors (GPTZero, Originality.ai, ZeroGPT, etc.) key off:
predictable vocabulary, uniform sentence-length rhythm, formulaic structure.
Fixing those tells well tends to read as more human to both people and
detectors — that's an expected side effect of doing this properly, not a
separate thing to chase.

## Procedure

1. **If text already exists** (revise-own-output or paste-and-rewrite mode),
   run the scan script for a mechanical signal report:
   ```
   python3 scripts/scan.py path/to/text.txt
   # or: python3 scripts/scan.py < text.txt
   ```
   If drafting fresh with no existing text, skip straight to step 3 and apply
   the checklist as you write; you can scan the result afterward as a check.

2. **Read the scan output as signal, not verdict.** It's a mechanical
   word/pattern match — it will flag legitimate uses of common words in
   on-topic context. Use it to know where to look closely, not as a
   find-and-delete list.

3. **Apply `reference.md`'s checklist categories with judgment.** Load that
   file and work through the text against each category: overused vocabulary,
   copula-avoidance, vague connection language, negative parallelism ("it's
   not X, it's Y"), rule-of-three overuse, undue-significance filler,
   present-participle tacking, promotional tone, formatting tells (em dashes
   especially — avoid by default, not just "in moderation"), rigid
   "challenges and future" structure, fake rhetorical questions, connector
   chains, hyperbole, filler paragraphs, uniform/symmetrical structure,
   repeated paragraph-opener formula, and circular/epigrammatic closers.

4. **Hard constraint: preserve meaning exactly.** This is a voice rewrite,
   not a content edit — don't drop, soften, or add claims, numbers, names, or
   intent while changing how something is said.

5. **Reintroduce natural variance on purpose.** Vary sentence length, allow
   an occasional fragment or asymmetric paragraph. Don't swap one uniform
   "AI" template for a different uniform "humanized" template — genuine human
   writing is uneven, not evenly de-AI'd.

6. **Present the rewrite** with a short "what changed" bullet list naming the
   pattern categories addressed — a brief summary, not a full diff.

## Revising vs. drafting fresh

- **Revising existing text:** work paragraph by paragraph and keep the
  author's actual structure and content — you're changing voice, not
  reorganizing.
- **Drafting fresh:** apply the checklist as constraints while writing, not
  as a filter applied after the fact.

## Supporting files

- `reference.md` — the full checklist: vocabulary list, sentence-pattern
  tells, formatting tells, and before/after examples for each. Load it in
  step 3.
- `scripts/scan.py` — stdlib-only Python 3 script that scans text for
  blocklist hits, em dashes (flags any nonzero count, not just high density),
  "not X, but Y" constructions, rule-of-three patterns, sentence-length
  variance, formatting tells, every paragraph's opening sentence (useful for
  spotting a repeated opener shape at a glance), and literal word overlap
  between the first and last sentence (a weak signal only — it misses
  thematic echoes, catches just repeated vocabulary). Run it in step 1.
