---
name: example-skill
description: PLACEHOLDER - replace this. The description is what Claude reads to decide whether to load the skill, so write it as a trigger condition - say what the skill does and when it applies, using words that would appear in a request that needs it.
---

# Example Skill

Replace this file with a real skill. The structure to follow:

## What this section is for

Everything below the frontmatter is loaded into context only when the skill
triggers, so it can be as long as it needs to be. Write it as instructions to
Claude, not as documentation for a human.

## Guidelines that work well here

- Concrete procedures, in the order they should be done
- Conventions and defaults you always want applied
- Worked examples, especially of the output format you expect
- Things to avoid, stated plainly

## Supporting files

A skill folder can hold more than SKILL.md. Reference sibling files by relative
path and Claude will read them when needed:

    skills/example-skill/
    ├── SKILL.md
    ├── reference.md
    └── scripts/
        └── helper.py

Keep SKILL.md itself lean and push detail into supporting files, so the loaded
context stays small until the detail is actually required.
