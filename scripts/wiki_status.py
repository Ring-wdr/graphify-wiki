from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES_DIR = ROOT / "notes"
GRAPH_OUTPUTS = [
    ROOT / "graphify-out" / "graph.html",
    ROOT / "graphify-out" / "GRAPH_REPORT.md",
    ROOT / "graphify-out" / "graph.json",
]


def git_status_paths() -> list[str]:
    result = subprocess.run(
        ["git", "status", "--short"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    return [line[3:] for line in lines if len(line) > 3]


def latest_mtime(paths: list[Path]) -> float:
    mtimes = [path.stat().st_mtime for path in paths if path.exists()]
    return max(mtimes) if mtimes else 0.0


def note_files() -> list[Path]:
    return [path for path in NOTES_DIR.rglob("*.md") if path.is_file()]


def main() -> None:
    changed_paths = git_status_paths()
    note_related = [path for path in changed_paths if path.startswith("notes/")]
    graph_related = [path for path in changed_paths if path.startswith("graphify-out/")]
    workflow_related = [
        path for path in changed_paths if path in {".gitignore", "README.md"} or path.startswith("scripts/")
    ]

    notes_mtime = latest_mtime(note_files())
    graph_mtime = latest_mtime(GRAPH_OUTPUTS)
    graph_missing = [path.relative_to(ROOT).as_posix() for path in GRAPH_OUTPUTS if not path.exists()]
    graph_stale = bool(notes_mtime and graph_mtime and notes_mtime > graph_mtime)

    print("Wiki status")
    print(f"- note changes: {len(note_related)}")
    print(f"- graph changes: {len(graph_related)}")
    print(f"- workflow changes: {len(workflow_related)}")
    print(f"- graph stale vs notes: {'yes' if graph_stale else 'no'}")

    if graph_missing:
        print(f"- graph outputs missing: {', '.join(graph_missing)}")

    if note_related:
        print("- suggested next commit: notes/hubs/meta first")
    elif graph_related:
        print("- suggested next commit: graph output refresh")
    elif graph_stale:
        print("- suggested next step: rebuild graph outputs")
    else:
        print("- suggested next step: working tree is aligned")

    if note_related:
        print("")
        print("Changed notes:")
        for path in note_related[:10]:
            print(f"  - {path}")
        if len(note_related) > 10:
            print(f"  - ... and {len(note_related) - 10} more")

    if graph_related:
        print("")
        print("Changed graph outputs:")
        for path in graph_related:
            print(f"  - {path}")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        print(exc.stderr or exc.stdout or str(exc), file=sys.stderr)
        raise SystemExit(exc.returncode)
