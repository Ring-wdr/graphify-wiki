from __future__ import annotations

import json
import re
import shutil
from collections import Counter
from pathlib import Path

from graphify.analyze import god_nodes, suggest_questions, surprising_connections
from graphify.build import build_from_json
from graphify.cluster import cluster, score_all
from graphify.detect import detect
from graphify.export import to_html, to_json
from graphify.report import generate
from graphify.report import _safe_community_name
from graphify.wiki import _community_article, _god_node_article, _index_md, _safe_filename

ROOT = Path(__file__).resolve().parents[1]
NOTES_DIR = ROOT / "notes"
OUT_DIR = ROOT / "graphify-out"
WIKI_DIR = OUT_DIR / "wiki"

TITLE_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]+)?\)")

CATEGORY_LABELS = {
    "notes/dev/version-control": "Version Control",
    "notes/dev/debugging": "Debugging & Operations",
    "notes/dev/backend-runtime": "Backend Runtime",
    "notes/dev/database": "Database",
    "notes/dev/architecture": "Architecture",
    "notes/dev/tooling": "Tooling & Delivery",
    "notes/hubs": "Hub Navigation",
    "notes/meta": "Wiki Operations",
    "notes/inbox": "Inbox Notes",
}


def note_files() -> list[Path]:
    return sorted(path for path in NOTES_DIR.rglob("*.md") if path.is_file())


def relative_repo_path(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def note_id(path: Path) -> str:
    rel = path.relative_to(ROOT).with_suffix("").as_posix()
    return re.sub(r"[^a-zA-Z0-9]+", "_", rel).strip("_").lower()


def read_title(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = TITLE_RE.search(text)
    if match:
        return match.group(1).strip()
    return path.stem.replace("-", " ").replace("_", " ").title()


def resolve_link(source: Path, href: str) -> Path | None:
    if "://" in href or href.startswith("mailto:"):
        return None
    candidate = (source.parent / href).resolve()
    if candidate.suffix == "":
        candidate = candidate.with_suffix(".md")
    try:
        candidate.relative_to(NOTES_DIR.resolve())
    except ValueError:
        return None
    if not candidate.exists() or candidate.suffix.lower() != ".md":
        return None
    return candidate


def extract_edges(files: list[Path], ids_by_path: dict[Path, str]) -> list[dict]:
    deduped: dict[tuple[str, str], dict] = {}
    for source in files:
        text = source.read_text(encoding="utf-8")
        source_id = ids_by_path[source]
        source_file = relative_repo_path(source)
        for href in LINK_RE.findall(text):
            target = resolve_link(source, href.strip())
            if target is None:
                continue
            target_id = ids_by_path[target]
            if source_id == target_id:
                continue
            key = tuple(sorted((source_id, target_id)))
            deduped.setdefault(
                key,
                {
                    "source": source_id,
                    "target": target_id,
                    "relation": "references",
                    "confidence": "EXTRACTED",
                    "confidence_score": 1.0,
                    "source_file": source_file,
                    "source_location": None,
                    "weight": 1.0,
                },
            )
    return list(deduped.values())


def build_extraction(files: list[Path]) -> dict:
    ids_by_path = {path: note_id(path) for path in files}
    nodes = []
    for path in files:
        nodes.append(
            {
                "id": ids_by_path[path],
                "label": read_title(path),
                "file_type": "document",
                "source_file": relative_repo_path(path),
                "source_location": None,
                "source_url": None,
                "captured_at": None,
                "author": None,
                "contributor": None,
            }
        )

    return {
        "nodes": nodes,
        "edges": extract_edges(files, ids_by_path),
        "hyperedges": [],
        "input_tokens": 0,
        "output_tokens": 0,
    }


def category_for(source_file: str) -> str:
    for prefix, label in sorted(CATEGORY_LABELS.items(), key=lambda item: len(item[0]), reverse=True):
        if source_file.startswith(prefix):
            return label
    return "Knowledge Notes"


def community_labels_for(graph, communities: dict[int, list[str]]) -> dict[int, str]:
    labels: dict[int, str] = {}
    degree = dict(graph.degree())

    for cid, nodes in communities.items():
        counts = Counter(category_for(graph.nodes[node].get("source_file", "")) for node in nodes)
        ranked = counts.most_common()
        if not ranked:
            labels[cid] = f"Community {cid}"
            continue
        if len(ranked) == 1 or ranked[0][1] > ranked[1][1]:
            labels[cid] = ranked[0][0]
            continue
        top_node = max(nodes, key=lambda node: degree.get(node, 0))
        labels[cid] = graph.nodes[top_node].get("label", ranked[0][0])

    return labels


def write_wiki(graph, communities: dict[int, list[str]], labels: dict[int, str], cohesion: dict[int, float], gods: list[dict]) -> None:
    WIKI_DIR.mkdir(parents=True, exist_ok=True)

    for cid, nodes in communities.items():
        label = labels.get(cid, f"Community {cid}")
        article = _community_article(graph, cid, nodes, label, labels, cohesion.get(cid))
        (WIKI_DIR / f"{_safe_filename(label)}.md").write_text(article, encoding="utf-8")
        (WIKI_DIR / f"_COMMUNITY_{_safe_community_name(label)}.md").write_text(article, encoding="utf-8")

    for node in gods:
        node_id = node.get("id")
        if node_id and node_id in graph:
            article = _god_node_article(graph, node_id, labels)
            (WIKI_DIR / f"{_safe_filename(node['label'])}.md").write_text(article, encoding="utf-8")

    index = _index_md(communities, labels, gods, graph.number_of_nodes(), graph.number_of_edges())
    (WIKI_DIR / "index.md").write_text(index, encoding="utf-8")


def main() -> None:
    files = note_files()
    if not files:
        raise SystemExit("No markdown notes found under notes/.")

    extraction = build_extraction(files)
    graph = build_from_json(extraction)
    communities = cluster(graph)
    cohesion = score_all(graph, communities)
    detection = detect(NOTES_DIR)
    labels = community_labels_for(graph, communities)
    gods = god_nodes(graph)
    surprises = surprising_connections(graph, communities)
    questions = suggest_questions(graph, communities, labels)
    token_cost = {"input": 0, "output": 0}

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    report = generate(
        graph,
        communities,
        cohesion,
        labels,
        gods,
        surprises,
        detection,
        token_cost,
        "notes",
        suggested_questions=questions,
    )

    (OUT_DIR / "GRAPH_REPORT.md").write_text(report, encoding="utf-8")
    to_json(graph, communities, str(OUT_DIR / "graph.json"))
    to_html(graph, communities, str(OUT_DIR / "graph.html"), community_labels=labels)

    if WIKI_DIR.exists():
        shutil.rmtree(WIKI_DIR)
    write_wiki(graph, communities, labels, cohesion, gods)

    summary = {
        "files": len(files),
        "nodes": graph.number_of_nodes(),
        "edges": graph.number_of_edges(),
        "communities": len(communities),
        "wiki_dir": str(WIKI_DIR.relative_to(ROOT)).replace("\\", "/"),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
