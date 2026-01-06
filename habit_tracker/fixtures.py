from __future__ import annotations

from datetime import datetime, timedelta
from typing import List, Tuple

from .models import Periodicity
from .storage import add_checkoff, create_habit, get_habit_by_name


DEFAULT_HABITS: List[Tuple[str, Periodicity]] = [
    ("Workout", Periodicity.daily),
    ("Read 10 minutes", Periodicity.daily),
    ("Drink Water", Periodicity.daily),
    ("Call parents", Periodicity.weekly),
    ("Clean apartment", Periodicity.weekly),
]


def load_fixtures(weeks: int = 4) -> None:
    """Create sample habits and check-offs (>=5 habits, >=4 weeks)."""
    # Create habits if they do not exist yet
    for name, periodicity in DEFAULT_HABITS:
        if get_habit_by_name(name) is None:
            create_habit(name, periodicity)

    now = datetime.utcnow()

    for name, periodicity in DEFAULT_HABITS:
        habit = get_habit_by_name(name)
        if habit is None:
            continue

        if periodicity == Periodicity.daily:
            # Daily habits: most days, with some gaps
            for day_offset in range(weeks * 7):
                if day_offset % 6 == 0:
                    continue
                add_checkoff(
                    habit,
                    when=now - timedelta(days=(weeks * 7 - day_offset)),
                )
        else:
            # Weekly habits: once per week, skip one week
            for week in range(weeks):
                if week == 2:
                    continue
                add_checkoff(
                    habit,
                    when=now - timedelta(days=(weeks - week) * 7),
                )
