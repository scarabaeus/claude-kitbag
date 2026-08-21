# claude-kitbag

Personal Claude skills and plugins, distributed as a plugin marketplace.

## Implemented Skills/Plugins
- `/humanize` - Rewrites AI-generated-sounding text into natural human prose. Usage: `/humanize <insert ai slop>`
_Note: [AI detection tools](https://grammarly.com/ai-content-detector) currently flags output at about 10% to 20% AI-generated._

## Planned Skills/Plugins
- `/eli5` - "Explain like I'm 5" has Claude explain complex topics to me like I'm 5 years old. Usage: `/eli5 <insert complex topic>`

## Install

In Claude Code:

```
/plugin marketplace add scarabaeus/claude-kitbag
/plugin install kitbag-core@claude-kitbag
```

In claude.ai or Claude Desktop chat: **Customize → Plugins → Personal plugins →
"+" → Add marketplace → Add from a repository**, then enter `scarabaeus/claude-kitbag`.

For local testing before pushing anywhere, add by filesystem path instead:

```
/plugin marketplace add /path/to/claude-kitbag
/plugin install humanize@claude-kitbag
```

No git commit or remote is required for a local path add.

**When iterating on plugin content locally:** after editing files and running
`/plugin marketplace update <name>`, an already-running session may not pick
up the change — watch for a "Plugins changed, run `/reload-plugins`" notice
and act on it (or just start a fresh session after updating). Skipping this
means you can be testing stale content without any error or warning, which
will silently invalidate before/after comparisons.

## Layout

```
claude-kitbag/
├── .claude-plugin/
│   └── marketplace.json          # the catalog - lists every plugin
└── plugins/
    ├── kitbag-core/
    │   ├── .claude-plugin/
    │   │   └── plugin.json       # this plugin's manifest
    │   └── skills/
    │       └── example-skill/
    │           └── SKILL.md      # one folder per skill
    └── humanize/
        ├── .claude-plugin/
        │   └── plugin.json
        └── skills/
            └── humanize/
                ├── SKILL.md
                ├── reference.md
                └── scripts/
                    └── scan.py
```

Each plugin's `source` is the full path from the marketplace root:
`./plugins/<name>`. (An earlier version of this file used `metadata.pluginRoot`
to shorten `source` to a bare folder name — the docs describe this as valid,
but the installed CLI ignored `pluginRoot` at install time and looked for the
source directly under the marketplace root, failing with "Source path does not
exist." Using the full `./plugins/<name>` path sidesteps that inconsistency
entirely, so it's what this repo uses.)

## Adding a skill

Create a new folder under an existing plugin's `skills/` directory containing a
`SKILL.md`. Nothing else needs updating - skills are discovered by scanning that
directory.

## Adding a plugin

1. Create `plugins/<new-plugin>/.claude-plugin/plugin.json`
2. Add an entry to the `plugins` array in `.claude-plugin/marketplace.json`
3. Plugin names must be kebab-case: lowercase letters, digits, and hyphens

## Publishing changes

```
git add -A && git commit -m "..." && git push
```

Then in any client, refresh: `/plugin marketplace update claude-kitbag`

Note: `version` is deliberately omitted from `plugin.json`. With no version
declared, Claude Code uses the resolved commit SHA, so every push is picked up
automatically. If a `version` is ever added, it must be bumped on every release
or clients will keep serving the cached copy.

## Validate before pushing

```
claude plugin validate .
```

Checks the marketplace schema, duplicate plugin names, and source paths. To check
skill frontmatter, point it at a skills directory:

```
claude plugin validate plugins/kitbag-core/skills
```
