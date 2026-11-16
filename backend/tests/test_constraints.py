"""Tests for the restriction check (FR-05)."""
from datetime import date

from app.constraints import Assignment, Consultant, check_assignment

# October 2026: the 12th is a Monday
MON, TUE, WED, FRI = date(2026, 10, 12), date(2026, 10, 13), date(2026, 10, 14), date(2026, 10, 16)


def make_consultant(leave_days=None):
    """Works Mon-Wed, max 2 days per week, max 3 days per month."""
    return Consultant(id=1, working_weekdays={0, 1, 2}, weekly_limit=2,
                      monthly_budget_days=3, leave_days=leave_days or set())


def test_allowed():
    assert check_assignment(make_consultant(), [], MON).allowed


def test_non_working_day():
    assert not check_assignment(make_consultant(), [], FRI).allowed


def test_leave_day():
    assert not check_assignment(make_consultant(leave_days={WED}), [], WED).allowed


def test_weekly_limit():
    existing = [Assignment(1, MON), Assignment(1, TUE)]
    assert not check_assignment(make_consultant(), existing, WED).allowed


def test_monthly_budget():
    existing = [Assignment(1, date(2026, 10, 5)), Assignment(1, date(2026, 10, 6)), Assignment(1, MON)]
    assert not check_assignment(make_consultant(), existing, TUE).allowed