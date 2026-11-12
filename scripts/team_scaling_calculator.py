#!/usr/bin/env python3
"""Estimate engineering-team capacity and a hiring requirement.

The model is deliberately transparent. It estimates delivery capacity from
current throughput, availability, attrition, and a hiring ramp. It is not a
headcount recommendation without product, budget, and coordination context.
"""
from __future__ import annotations

import argparse
import json
import math
import sys


def positive(name: str, value: float, allow_zero: bool = False) -> float:
    minimum = 0 if allow_zero else 0.000001
    if not math.isfinite(value) or value < minimum:
        raise ValueError(f"{name} must be {'non-negative' if allow_zero else 'positive'}")
    return value


def calculate(
    engineers: float,
    points_per_engineer: float,
    work_items: float,
    target_months: float,
    available_fraction: float,
    attrition_rate: float,
    ramp_months: float,
) -> dict[str, float]:
    positive("engineers", engineers)
    positive("points_per_engineer", points_per_engineer)
    positive("work_items", work_items, allow_zero=True)
    positive("target_months", target_months)
    positive("available_fraction", available_fraction)
    positive("ramp_months", ramp_months, allow_zero=True)
    if not 0 < available_fraction <= 1:
        raise ValueError("available_fraction must be in (0, 1]")
    if not 0 <= attrition_rate < 1:
        raise ValueError("attrition_rate must be in [0, 1)")

    monthly_per_engineer = points_per_engineer * available_fraction
    effective_current = engineers * (1 - attrition_rate)
    monthly_capacity = effective_current * monthly_per_engineer
    required_monthly_capacity = work_items / target_months if work_items else 0.0
    required_engineers = (
        required_monthly_capacity / monthly_per_engineer
        if required_monthly_capacity else 0.0
    )
    additional = max(0.0, required_engineers - effective_current)

    # New hires are not assumed fully productive until their ramp period ends.
    ramp_factor = 1.0 if ramp_months == 0 else max(0.0, 1.0 - ramp_months / max(target_months, ramp_months))
    ramp_adjusted_additional = additional / max(ramp_factor, 0.25)

    return {
        "current_engineers": engineers,
        "effective_engineers_after_attrition": round(effective_current, 2),
        "monthly_capacity_units": round(monthly_capacity, 2),
        "required_monthly_capacity_units": round(required_monthly_capacity, 2),
        "estimated_required_engineers": round(required_engineers, 2),
        "additional_fte_before_ramp": round(additional, 2),
        "estimated_additional_hires_with_ramp": round(ramp_adjusted_additional, 2),
        "capacity_gap_per_month": round(max(0.0, required_monthly_capacity - monthly_capacity), 2),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engineers", type=float, required=True, help="Current engineering FTE")
    parser.add_argument("--points-per-engineer", type=float, required=True, help="Observed monthly throughput per FTE")
    parser.add_argument("--work-items", type=float, required=True, help="Total comparable work units in scope")
    parser.add_argument("--target-months", type=float, required=True)
    parser.add_argument("--available-fraction", type=float, default=0.75, help="Share of time available for planned delivery")
    parser.add_argument("--attrition-rate", type=float, default=0.0, help="Expected attrition fraction, 0 to less than 1")
    parser.add_argument("--ramp-months", type=float, default=2.0, help="Months for a new hire to reach expected productivity")
    args = parser.parse_args()

    try:
        result = calculate(
            args.engineers, args.points_per_engineer, args.work_items,
            args.target_months, args.available_fraction, args.attrition_rate,
            args.ramp_months,
        )
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
