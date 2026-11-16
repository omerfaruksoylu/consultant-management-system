"""Restriction check for task assignment (FR-05).

This module decides whether a task can be assigned to a consultant on a given day.
It has no database or web code, so it can be tested on its own.
"""
from dataclasses import dataclass, field
from datetime import date, timedelta


@dataclass
class Consultant:
    id: int
    working_weekdays: set[int]            # 0 = Monday ... 6 = Sunday
    weekly_limit: int                     # max assigned days in one week
    monthly_budget_days: int              # max assigned days in one month
    leave_days: set[date] = field(default_factory=set)


@dataclass
class Assignment:
    consultant_id: int
    day: date


@dataclass
class CheckResult:
    allowed: bool
    reason: str


def week_start(day: date) -> date:
    """Return the Monday of the week that contains `day`."""
    return day - timedelta(days=day.weekday())


def check_assignment(consultant: Consultant, existing: list[Assignment], day: date) -> CheckResult:
    """Check the four restriction types in order and return the first one that fails."""
    # 1) Working weekday
    if day.weekday() not in consultant.working_weekdays:
        return CheckResult(False, f"Consultant does not work on {day:%A}s")

    # 2) Leave day
    if day in consultant.leave_days:
        return CheckResult(False, f"Consultant is on leave on {day.isoformat()}")

    own = [a for a in existing if a.consultant_id == consultant.id]

    # 3) Weekly limit
    same_week = [a for a in own if week_start(a.day) == week_start(day)]
    if len(same_week) >= consultant.weekly_limit:
        return CheckResult(
            False, f"Weekly limit reached ({len(same_week)}/{consultant.weekly_limit} days)"
        )

    # 4) Monthly budget
    same_month = [a for a in own if (a.day.year, a.day.month) == (day.year, day.month)]
    if len(same_month) >= consultant.monthly_budget_days:
        return CheckResult(
            False,
            f"Monthly budget reached ({len(same_month)}/{consultant.monthly_budget_days} days)",
        )

    return CheckResult(True, "OK")
