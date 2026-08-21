# claude-kitbag

Personal Claude skills and plugins, distributed as a plugin marketplace.

## Install

In Claude Code:

```
/plugin marketplace add scarabaeus/claude-kitbag
/plugin install kitbag-core@claude-kitbag
```

In claude.ai or Claude Desktop chat: **Customize → Plugins → Personal plugins →
"+" → Add marketplace → Add from a repository**, then enter `scarabaeus/claude-kitbag`.

## Layout

```
claude-kitbag/
├── .claude-plugin/
│   └── marketplace.json          # the catalog - lists every plugin
└── plugins/
    └── kitbag-core/
        ├── .claude-plugin/
        │   └── plugin.json       # this plugin's manifest
        └── skills/
            └── example-skill/
                └── SKILL.md      # one folder per skill
```

`metadata.pluginRoot` is set to `./plugins` in the marketplace file, which is why
each plugin's `source` is just its folder name rather than `./plugins/<name>`.

## Planned Skills/Plugins
- `/humanize` - Forces claude to output typical AI slop text output into more "natural sounding" human written text. For use in written communication shared with others.
- `/eli5` - "Explain like I'm 5" has claude explain complex topics to me like I'm 5 years old. Usage: `/eli5 <insert complex topic>`

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
