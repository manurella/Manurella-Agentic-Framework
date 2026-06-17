# Tools

Local tools that enforce Manurella framework structure.

## Framework Validator

Run from the repository root:

```powershell
python tools/validate_framework.py --repo .
```

The validator checks:

- cognitive graph YAML
- duplicate graph node and edge IDs
- graph edge references
- evidence paths
- agent frontmatter shape
- agent permission values
- accepted-agent promotion minimums
- eval hygiene warnings

Errors fail validation. Warnings identify known quality risks that should be fixed before promotion or final reporting.
