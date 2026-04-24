#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


STATE_SECTIONS = {
    "Source Ledger": "<!-- append-source-ledger-rows-here -->",
    "Subresearch Index": "<!-- append-subresearch-index-rows-here -->",
    "Iteration Review Log": "<!-- append-iteration-review-log-rows-here -->",
    "Prompt Backlog": "<!-- append-prompt-backlog-rows-here -->",
    "Normalization Queue": "<!-- append-normalization-queue-rows-here -->",
}

ALLOWED_STATE_APPEND_STATUS = {"", "pending", "appended", "conflict_retry", "blocked"}
ALLOWED_PROMPT_STATUS = {"", "new", "claimed", "completed", "merged", "dropped"}
ALLOWED_CONTINUE_OR_SHIFT = {
    "",
    "continue_discovery",
    "shift_to_normalization",
    "shift_to_final_synthesis",
    "stop_for_exhaustion",
}
ALLOWED_PRIORITY = {"", "high", "medium", "low"}
ALLOWED_DRIFT_NOTE = {"", "tight_to_core", "slight_bounded_drift", "drift_not_allowed"}
ALLOWED_NORMALIZATION_STATUS = {
    "",
    "pending",
    "normalized",
    "duplicate",
    "contradiction_retained",
    "empty_with_reason",
}
ALLOWED_FINAL_REPORT_STATUS = {
    "",
    "pending",
    "promoted",
    "promoted_as_contradiction",
    "duplicate_noted",
    "empty_with_reason",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate an evidence-first research run.")
    parser.add_argument("--state", required=True, help="Path to evidence-research-state.md")
    return parser.parse_args()


def parse_table_cells(row: str) -> list[str]:
    stripped = row.strip()
    return [cell.strip() for cell in stripped.split("|")[1:-1]]


def find_section_bounds(lines: list[str], heading: str) -> tuple[int, int]:
    start = None
    for index, line in enumerate(lines):
        if line.strip() == heading:
            start = index
            break
    if start is None:
        raise ValueError(f"missing section heading: {heading}")
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    return start, end


def parse_state_top_fields(lines: list[str]) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in lines:
        if line.startswith("## "):
            break
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    return fields


def parse_state_table(lines: list[str], heading: str, marker: str) -> tuple[list[str], list[dict[str, str]]]:
    start, end = find_section_bounds(lines, f"## {heading}")
    section_lines = lines[start:end]
    if marker not in [line.strip() for line in section_lines]:
        raise ValueError(f"missing marker {marker} in section {heading}")
    table_lines = [line for line in section_lines if line.strip().startswith("|")]
    if len(table_lines) < 2:
        raise ValueError(f"section {heading} does not contain a markdown table")
    headers = parse_table_cells(table_lines[0])
    rows: list[dict[str, str]] = []
    for line in table_lines[2:]:
        cells = parse_table_cells(line)
        if len(cells) != len(headers):
            raise ValueError(f"row width mismatch in section {heading}: {line}")
        rows.append(dict(zip(headers, cells)))
    return headers, rows


def normalize_key(name: str) -> str:
    return name.strip().lower().replace(" ", "_")


def parse_section_bullets(section_lines: list[str]) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in section_lines:
        stripped = line.strip()
        if not stripped.startswith("- ") or ":" not in stripped:
            continue
        key, value = stripped[2:].split(":", 1)
        fields[key.strip()] = value.strip()
    return fields


def parse_subresearch_file(path: Path) -> dict[str, object]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or not lines[0].startswith("# Subresearch File "):
        raise ValueError(f"{path}: missing subresearch title line")

    file_id = lines[0].removeprefix("# Subresearch File ").strip()
    top_fields: dict[str, str] = {}
    for line in lines[1:]:
        if line.startswith("## "):
            break
        if ":" in line:
            key, value = line.split(":", 1)
            top_fields[key.strip()] = value.strip()

    def extract_section(heading: str) -> list[str]:
        start, end = find_section_bounds(lines, f"## {heading}")
        return lines[start + 1 : end]

    sources_section = extract_section("Sources Reviewed")
    sources_table_lines = [line for line in sources_section if line.strip().startswith("|")]
    next_prompts_section = extract_section("Next Research Prompts")
    prompt_table_lines = [line for line in next_prompts_section if line.strip().startswith("|")]
    prompt_rows = prompt_table_lines[2:] if len(prompt_table_lines) >= 2 else []
    iteration_control = parse_section_bullets(extract_section("Iteration Control"))
    state_update = parse_section_bullets(extract_section("State File Update"))

    return {
        "path": path,
        "file_id": file_id,
        "top_fields": top_fields,
        "sources_table_lines": sources_table_lines,
        "prompt_rows": prompt_rows,
        "iteration_control": iteration_control,
        "state_update": state_update,
    }


def split_compound_value(value: str) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in re.split(r"[,\s]+", value) if item.strip()]


def main() -> None:
    args = parse_args()
    state_path = Path(args.state)
    if not state_path.is_file():
        print(f"error: state file not found: {state_path}", file=sys.stderr)
        raise SystemExit(1)

    errors: list[str] = []

    lines = state_path.read_text(encoding="utf-8").splitlines()
    top_fields = parse_state_top_fields(lines)

    required_top_fields = {
        "run_id",
        "research_objective",
        "current_stage",
        "stage_status",
        "current_wave",
        "subresearch_dir",
        "final_report_path",
        "next_action",
        "updated_at",
    }
    for key in sorted(required_top_fields):
        if key not in top_fields:
            errors.append(f"state file missing top-level field: {key}")

    parsed_sections: dict[str, list[dict[str, str]]] = {}
    for heading, marker in STATE_SECTIONS.items():
        try:
            _, rows = parse_state_table(lines, heading, marker)
            parsed_sections[heading] = rows
        except ValueError as exc:
            errors.append(str(exc))

    for heading, rows in parsed_sections.items():
        seen: set[str] = set()
        for row in rows:
            first_value = next(iter(row.values()), "")
            if not first_value:
                errors.append(f"{heading}: row has empty first cell")
                continue
            if first_value in seen:
                errors.append(f"{heading}: duplicate first cell {first_value}")
            seen.add(first_value)

    for row in parsed_sections.get("Subresearch Index", []):
        if row.get("state_append_status", "") not in ALLOWED_STATE_APPEND_STATUS:
            errors.append(
                f"Subresearch Index {row.get('file_id','?')}: invalid state_append_status {row.get('state_append_status')}"
            )
        if row.get("normalization_status", "") not in ALLOWED_NORMALIZATION_STATUS:
            errors.append(
                f"Subresearch Index {row.get('file_id','?')}: invalid normalization_status {row.get('normalization_status')}"
            )
        if row.get("final_report_status", "") not in ALLOWED_FINAL_REPORT_STATUS:
            errors.append(
                f"Subresearch Index {row.get('file_id','?')}: invalid final_report_status {row.get('final_report_status')}"
            )

    for row in parsed_sections.get("Prompt Backlog", []):
        if row.get("status", "") not in ALLOWED_PROMPT_STATUS:
            errors.append(f"Prompt Backlog {row.get('prompt_id','?')}: invalid status {row.get('status')}")
        if row.get("priority", "") not in ALLOWED_PRIORITY:
            errors.append(f"Prompt Backlog {row.get('prompt_id','?')}: invalid priority {row.get('priority')}")

    review_ids = {row.get("review_file_id", "") for row in parsed_sections.get("Iteration Review Log", [])}
    prompt_ids = {row.get("prompt_id", "") for row in parsed_sections.get("Prompt Backlog", [])}

    for row in parsed_sections.get("Iteration Review Log", []):
        if row.get("continue_or_shift", "") not in ALLOWED_CONTINUE_OR_SHIFT:
            errors.append(
                f"Iteration Review Log {row.get('review_file_id','?')}: invalid continue_or_shift {row.get('continue_or_shift')}"
            )
        if row.get("theme_drift_note", "") not in ALLOWED_DRIFT_NOTE:
            errors.append(
                f"Iteration Review Log {row.get('review_file_id','?')}: invalid theme_drift_note {row.get('theme_drift_note')}"
            )
        for prompt_id in split_compound_value(row.get("prompt_ids", "")):
            if prompt_id not in prompt_ids:
                errors.append(
                    f"Iteration Review Log {row.get('review_file_id','?')}: missing prompt_id in backlog: {prompt_id}"
                )

    for row in parsed_sections.get("Prompt Backlog", []):
        parent = row.get("parent_review_file_id", "")
        if parent and parent not in review_ids:
            errors.append(f"Prompt Backlog {row.get('prompt_id','?')}: unknown parent review {parent}")

    latest_review_file_id = top_fields.get("latest_review_file_id", "")
    if latest_review_file_id and latest_review_file_id not in review_ids:
        errors.append(f"latest_review_file_id not found in Iteration Review Log: {latest_review_file_id}")

    subresearch_dir = state_path.parent / top_fields.get("subresearch_dir", "evidence-subresearch/")
    index_by_file_id = {
        row.get("file_id", ""): row for row in parsed_sections.get("Subresearch Index", []) if row.get("file_id", "")
    }

    if subresearch_dir.is_dir():
        for sub_path in sorted(subresearch_dir.glob("*.md")):
            try:
                sub_file = parse_subresearch_file(sub_path)
            except ValueError as exc:
                errors.append(str(exc))
                continue

            file_id = str(sub_file["file_id"])
            if file_id not in index_by_file_id:
                errors.append(f"{sub_path}: file_id not found in Subresearch Index: {file_id}")
                continue

            index_row = index_by_file_id[file_id]
            relative_path = str(sub_path.relative_to(state_path.parent))
            if index_row.get("path", "") and index_row.get("path") != relative_path:
                errors.append(
                    f"{sub_path}: path mismatch with Subresearch Index ({index_row.get('path')} != {relative_path})"
                )

            file_class = str(sub_file["top_fields"].get("file_class", ""))
            if file_class and file_class != index_row.get("file_class", ""):
                errors.append(
                    f"{sub_path}: file_class mismatch with Subresearch Index ({file_class} != {index_row.get('file_class')})"
                )

            if len(sub_file["sources_table_lines"]) < 2:
                errors.append(f"{sub_path}: Sources Reviewed table missing or incomplete")

            state_update = sub_file["state_update"]
            touched_sections = {
                section.strip()
                for section in state_update.get("state_sections_touched", "").split(",")
                if section.strip()
            }
            if not touched_sections:
                errors.append(f"{sub_path}: missing state_sections_touched")

            file_text = sub_path.read_text(encoding="utf-8")
            material_findings = re.findall(r"^- claim_or_observation:\s*(.+)$", file_text, re.MULTILINE)
            datapoints = re.findall(r"^- key_excerpt_or_datapoint:\s*(.+)$", file_text, re.MULTILINE)
            if material_findings:
                non_empty_datapoints = [item.strip() for item in datapoints if item.strip()]
                if len(non_empty_datapoints) < len(material_findings):
                    errors.append(f"{sub_path}: one or more findings are missing key_excerpt_or_datapoint")

            if file_class == "review":
                prompt_count = len(sub_file["prompt_rows"])
                continue_or_shift = sub_file["iteration_control"].get("continue_or_shift", "")
                if prompt_count < 3 and continue_or_shift not in {
                    "shift_to_normalization",
                    "stop_for_exhaustion",
                }:
                    errors.append(
                        f"{sub_path}: review file has {prompt_count} prompts without stage shift or exhaustion"
                    )
                if prompt_count > 5:
                    errors.append(f"{sub_path}: review file has more than 5 prompts")

            if file_class == "normalization":
                forbidden_sections = {"Iteration Review Log", "Prompt Backlog"}
                wrong_sections = sorted(forbidden_sections.intersection(touched_sections))
                if wrong_sections:
                    errors.append(
                        f"{sub_path}: normalization file touched forbidden state sections: {', '.join(wrong_sections)}"
                    )

    else:
        errors.append(f"subresearch directory not found: {subresearch_dir}")

    if errors:
        print("validation failed", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        raise SystemExit(1)

    print(
        "validation passed: "
        f"{len(parsed_sections.get('Source Ledger', []))} source rows, "
        f"{len(parsed_sections.get('Subresearch Index', []))} subresearch rows, "
        f"{len(parsed_sections.get('Iteration Review Log', []))} review rows, "
        f"{len(parsed_sections.get('Prompt Backlog', []))} prompt rows"
    )


if __name__ == "__main__":
    main()
