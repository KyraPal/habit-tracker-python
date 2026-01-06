from datetime import datetime, timedelta

from habit_tracker.analytics import longest_streak_for_habit
from habit_tracker.models import Periodicity
from habit_tracker.storage import add_checkoff, create_habit, init_db


def test_longest_streak_daily_simple(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    init_db()
    h = create_habit("TestDaily", Periodicity.daily)

    base = datetime(2025, 1, 1)
    add_checkoff(h, base)
    add_checkoff(h, base + timedelta(days=1))
    add_checkoff(h, base + timedelta(days=2))

    assert longest_streak_for_habit(h) == 3


def test_longest_streak_daily_with_gap(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    init_db()
    h = create_habit("TestDailyGap", Periodicity.daily)

    base = datetime(2025, 1, 1)
    add_checkoff(h, base)
    add_checkoff(h, base + timedelta(days=2))

    assert longest_streak_for_habit(h) == 1
