# Kilo Adapter

The Kilo adapter is the first runtime target for Manurella v0.

It will compile portable domain-pack definitions into `.kilo/agents/*.md` files with YAML frontmatter.

## Target Shape

Each exported Kilo agent should include:

- `description`
- `mode`
- `permission`
- optional `model`
- optional `temperature`
- prompt body

## Rules

- Do not export broad edit/bash permissions by default.
- Do not export giant always-on reference libraries.
- Use Kilo permissions to keep creative, research, and tutoring agents away from code edits unless explicitly needed.
- Treat exported files as build artifacts unless manually promoted.

