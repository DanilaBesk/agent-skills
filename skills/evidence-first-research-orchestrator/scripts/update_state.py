#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from pathlib import Path


SECTION_SPECS = {
    "source_ledger": {
        "heading": "## Source Ledger",
        "marker": "<!-- append-source-ledger-rows-here -->",
    },
    "subresearch_index": {
        "heading": "## Subresearch Index",
        "marker": "<!-- append-subresearch-index-rows-here -->",
    },
    "iteration_review_log": {
        "heading": "## Iteration Review Log",
        "marker": "<!-- append-iteration-review-log-rows-here -->",
    },
    "prompt_backlog": {
        "heading": "## Prompt Backlog",
        "marker": "<!-- append-prompt-backlog-rows-here -->",
    },
    "normalization_queue": {
        "heading": "## Normalization Queue",
        "marker": "<!-- append-normalization-queue-rows-here -->",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Append table rows into a specific evidence-research state section."
    )
    parser.add_argument("--state", required=True, help="Path to evidence-research-state.md")
    parser.add_argument(
        "--section",
        required=True,
        choices=sorted(SECTION_SPECS.keys()),
        help="Target state section",
    )
    parser.add_argument(
        "--row",
        action="append",
        default=[],
        help="Single markdown table row to append",
    )
    parser.add_argument(
        "--row-file",
        action="append",
        default=[],
        help="Text file containing one markdown table row per line",
    )
    parser.add_argument(
        "--on-duplicate",
        choices=["error", "skip"],
        default="error",
        help="How to handle an existing first-cell key in the target section",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and print what would change without writing the file",
    )
    return parser.parse_args()


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def parse_table_cells(row: str) -> list[str]:
    stripped = row.strip()
    if not (stripped.startswith("|") and stripped.endswith("|")):
        fail(f"row must start and end with '|': {row}")
    return [cell.strip() for cell in stripped.split("|")[1:-1]]


def load_rows(args: argparse.Namespace) -> list[str]:
    rows: list[str] = []
    rows.extend(row.strip() for row in args.row if row.strip())
    for row_file in args.row_file:
        path = Path(row_file)
        if not path.is_file():
            fail(f"row file not found: {path}")
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                rows.append(line)
    if not rows:
        fail("at least one --row or --row-file entry is required")
    return rows


def find_section_bounds(lines: list[str], heading: str) -> tuple[int, int]:
    start = None
    for index, line in enumerate(lines):
        if line.strip() == heading:
            start = index
            break
    if start is None:
        fail(f"missing state section heading: {heading}")

    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    return start, end


def existing_first_cells(section_lines: list[str]) -> set[str]:
    table_lines = [line for line in section_lines if line.strip().startswith("|")]
    data_lines = table_lines[2:] if len(table_lines) >= 2 else []
    first_cells: set[str] = set()
    for line in data_lines:
        cells = parse_table_cells(line)
        if cells and cells[0]:
            first_cells.add(cells[0])
    return first_cells


def main() -> None:
    args = parse_args()
    state_path = Path(args.state)
    if not state_path.is_file():
        fail(f"state file not found: {state_path}")

    rows = load_rows(args)
    lines = state_path.read_text(encoding="utf-8").splitlines()

    spec = SECTION_SPECS[args.section]
    start, end = find_section_bounds(lines, spec["heading"])
    section_lines = lines[start:end]

    marker_line_indexes = [
        start + offset for offset, line in enumerate(section_lines) if line.strip() == spec["marker"]
    ]
    if len(marker_line_indexes) != 1:
        fail(f"expected exactly one marker {spec['marker']} in section {spec['heading']}")
    marker_index = marker_line_indexes[0]

    existing_keys = existing_first_cells(section_lines)
    new_lines: list[str] = []
    skipped = 0

    seen_new_keys: set[str] = set()
    for row in rows:
        cells = parse_table_cells(row)
        first_cell = cells[0] if cells else ""
        if not first_cell:
            fail(f"row must have a non-empty first cell: {row}")
        if first_cell in seen_new_keys:
            fail(f"duplicate first-cell key inside input rows: {first_cell}")
        seen_new_keys.add(first_cell)
        if first_cell in existing_keys:
            if args.on_duplicate == "skip":
                skipped += 1
                continue
            fail(f"duplicate first-cell key in target section: {first_cell}")
        new_lines.append(row)

    if args.dry_run:
        print(
            f"dry-run: would append {len(new_lines)} row(s) to {args.section}, "
            f"skip {skipped} duplicate row(s)"
        )
        for row in new_lines:
            print(row)
        return

    updated_lines = lines[:marker_index] + new_lines + lines[marker_index:]
    state_path.write_text("\n".join(updated_lines) + "\n", encoding="utf-8")
    print(
        f"appended {len(new_lines)} row(s) to {args.section} in {state_path}"
        + (f"; skipped {skipped} duplicate row(s)" if skipped else "")
    )


if __name__ == "__main__":
    main()
