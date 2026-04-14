# graphify-wiki

Small graphify-based wiki for building a public, Git-managed development knowledge base.

## Links

- Repository: https://github.com/Ring-wdr/graphify-wiki
- Wiki Pages: https://ring-wdr.github.io/graphify-wiki/

## Repository Shape

- `notes/`: source-of-truth knowledge notes
- `notes/inbox/`: rough captures that still need to be refined
- `notes/dev/`: atomic development notes grouped by problem or task
- `notes/hubs/`: curation hubs for navigating the wiki
- `notes/meta/`: templates, writing rules, and repository operating notes
- `scripts/rebuild_wiki_graph.py`: rebuild the graph outputs from note links
- `graphify-out/graph.html`: interactive graph visualization
- `graphify-out/GRAPH_REPORT.md`: graph audit report
- `graphify-out/graph.json`: exported graph data
- `graphify-out/wiki/index.md`: generated local wiki index for graph navigation

## Knowledge Workflow

- Keep one concept, problem, or pattern per note.
- Prefer English `kebab-case` filenames and Korean note bodies.
- Treat `notes/` as the primary asset in Git history.
- Regenerate `graphify-out/` after meaningful note updates, but keep note changes and graph regeneration in separate commits.

Recommended commit prefixes:

- `notes:` add or revise knowledge notes
- `hubs:` reorganize hub navigation
- `taxonomy:` adjust folder structure or naming
- `meta:` update templates or repository rules
- `graph:` regenerate graph outputs

## Development

This repository is managed with `uv`.

```bash
uv sync
uv run python scripts/rebuild_wiki_graph.py
```

Optional: install the `graphify` Codex skill into your user profile.

```bash
uv run graphify install --platform codex
```

## Publishing

GitHub Pages is deployed by Actions on pushes to `main`.
