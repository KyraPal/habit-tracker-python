from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import List, Optional, Tuple

from .models import Habit, Periodicity
from .storage import list_checkoffs_for_habit, list_habits


def _period_key(ts: datetime, periodicity: Periodicity) -> Tuple[int, int, int]:
    """Convert timestamps into day/week keys."""
    if periodicity == Periodicity.daily:
        d = ts.date()
        return (d.year, d.month, d.day)

    iso_year, iso_week, _ = ts.isocalendar()
    return (iso_year, iso_week, 0)


def _unique_sorted_periods(
    timestamps: List[datetime], periodicity: Periodicity
) -> List[Tuple[int, int, int]]:
    """Return unique, sorted period keys."""
    keys = {_period_key(ts, periodicity) for ts in timestamps}
    return sorted(keys)


def _is_next_period(
    prev: Tuple[int, int, int],
    curr: Tuple[int, int, int],
    periodicity: Periodicity,
) -> bool:
    """Check whether two periods are consecutive."""
    if periodicity == Periodicity.daily:
        prev_date = date(prev[0], prev[1], prev[2])
        curr_date = date(curr[0], curr[1], curr[2])
        return (curr_date - prev_date).days == 1

    py, pw, _ = prev
    cy, cw, _ = curr
    if cy == py and cw == pw + 1:
        return True
    if cy == py + 1 and cw == 1:
        return True
    return False


def longest_streak_for_habit(habit: Habit) -> int:
    """Calculate the longest streak for a single habit."""
    timestamps = list_checkoffs_for_habit(habit.id)
    periods = _unique_sorted_periods(timestamps, habit.periodicity)

    if not periods:
        return 0

    longest = 1
    current = 1
    prev = periods[0]

    for curr in periods[1:]:
        if _is_next_period(prev, curr, habit.periodicity):
            current += 1
        else:
            current = 1
        longest = max(longest, current)
        prev = curr

    return longest


@dataclass(frozen=True)
class LongestStreakResult:
    habit_name: str
    streak: int
    periodicity: Periodicity


def longest_streak_across_all() -> Optional[LongestStreakResult]:
    """Return the longest streak across all habits."""
    habits = list_habits()
    if not habits:
        return None

    best: Optional[LongestStreakResult] = None
    for h in habits:
        s = longest_streak_for_habit(h)
        candidate = LongestStreakResult(
            habit_name=h.name,
            streak=s,
            periodicity=h.periodicity,
        )
        if best is None or candidate.streak > best.streak:
            best = candidate

    return best
