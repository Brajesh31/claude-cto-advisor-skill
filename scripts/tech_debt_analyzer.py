#!/usr/bin/env python3
"""Rank technical-debt items from a JSON file.

Input may be a list of objects or {"items": [...]}.
Expected optional fields: title, area, impact, frequency, risk, age_days,
effort_days, owner, description. Ratings impact/frequency/risk use 1..5.
The tool produces a transparent prioritization aid, not an objective measure.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def number(item: dict[str, Any], key: str, default: float, low: float, high: float) -> float:
    raw = item.get(key, default)
    try:
        value = float(raw)
    except (TypeError, ValueError):
        raise ValueError(f"{key!r} must be numeric for item {item.get('title', '<untitled>')!r}")
    if not low <= value <= high:
        raise ValueError(f"{key!r} must be between {low} and {high}")
    return value


def analyze(item: dict[str, Any]) -> dict[str, Any]:
    impact = number(item, "impact", 3, 1, 5)
    frequency = number(item, "frequency", 3, 1, 5)
    risk = number(item, "risk", 3, 1, 5)
    age_days = number(item, "age_days", 0, 0, 36500)
    effort_days = number(item, "effort_days", 1, 0.25, 3650)

    # Higher impact, occurrence, risk, and age increase priority.
    age_score = min(age_days / 180.0, 5.0)
    raw_score = 0.35 * impact + 0.25 * frequency + 0.25 * risk + 0.15 * age_score
    effort_factor = max(0.5, min(2.0, effort_days ** 0.25))
    score = min(100.0, (raw_score / 5.0) * 100.0 / effort_factor)

    if score >= 75:
        band = "Critical"
    elif score >= 55:
        band = "High"
    elif score >= 35:
        band = "Moderate"
    else:
        band = "Low"

    return {
        "title": str(item.get("title") or item.get("id") or "Untitled debt item"),
        "area": str(item.get("area") or "Unspecified"),
        "owner": str(item.get("owner") or "Unassigned"),
        "score": round(score, 1),
        "priority": band,
        "impact": impact,
        "frequency": frequency,
        "risk": risk,
        "age_days": int(age_days),
        "effort_days": effort_days,
        "description": str(item.get("description") or ""),
    }


def load_items(path: Path) -> list[dict[str, Any]]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ValueError(f"cannot read {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path}: {exc}") from exc

    items = payload.get("items") if isinstance(payload, dict) else payload
    if not isinstance(items, list) or not all(isinstance(x, dict) for x in items):
        raise ValueError("input must be a JSON array or an object containing an 'items' array")
    return items


def render_markdown(rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Technical Debt Priorities", "",
        "| Priority | Score | Item | Area | Owner | Effort (days) |",
        "|---|---:|---|---|---|---:|",
    ]
    for row in rows:
        title = row["title"].replace("|", "\\|")
        area = row["area"].replace("|", "\\|")
        owner = row["owner"].replace("|", "\\|")
        lines.append(
            f"| {row['priority']} | {row['score']:.1f} | {title} | {area} | "
            f"{owner} | {row['effort_days']:g} |"
        )
    lines += ["", "Scores are prioritization aids. Validate assumptions with the team before committing work."]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="JSON file with technical-debt items")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    args = parser.parse_args()
    try:
        rows = sorted((analyze(x) for x in load_items(args.input)), key=lambda x: x["score"], reverse=True)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    output = json.dumps(rows, indent=2) if args.format == "json" else render_markdown(rows)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
