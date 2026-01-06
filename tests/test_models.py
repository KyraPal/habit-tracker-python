from habit_tracker.models import Periodicity



def test_periodicity_enum():
    assert Periodicity("daily") == Periodicity.daily
    assert Periodicity("weekly") == Periodicity.weekly
