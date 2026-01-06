from __future__ import annotations

from datetime import datetime, timezone

import click

from .analytics import longest_streak_across_all, longest_streak_for_habit
from .fixtures import load_fixtures
from .models import Periodicity
from .storage import (
    add_checkoff,
    create_habit,
    delete_habit,
    get_habit_by_name,
    init_db,
    list_habits,
    list_habits_by,
)


def _parse_periodicity(value: str) -> Periodicity:
    try:
        return Periodicity(value)
    except Exception:
        raise click.BadParameter("periodicity must be 'daily' or 'weekly'")


@click.group()
def cli() -> None:
    """Habit tracker CLI."""
    pass


@cli.command()
def init() -> None:
    """Initialize the SQLite database."""
    init_db()
    click.echo("Database initialized (habits.db).")


@cli.command("load-fixtures")
@click.option("--weeks", default=4, show_default=True, type=int)
def load_fixtures_cmd(weeks: int) -> None:
    """Load sample habits and check-offs."""
    init_db()
    load_fixtures(weeks=weeks)
    click.echo(f"Fixtures loaded (weeks={weeks}).")


@cli.command()
@click.argument("name")
@click.option("--periodicity", required=True)
def create(name: str, periodicity: str) -> None:
    """Create a new habit."""
    init_db()
    habit = create_habit(name, Periodicity(periodicity))
    click.echo(f"Created habit: {habit.name} ({habit.periodicity.value})")


@cli.command()
@click.argument("name")
def delete(name: str) -> None:
    """Delete a habit by name."""
    init_db()
    if delete_habit(name):
        click.echo(f"Deleted habit '{name}'.")
    else:
        click.echo(f"No habit found with name '{name}'.")


@cli.command()
def list() -> None:
    """List all habits."""
    init_db()
    habits = list_habits()
    if not habits:
        click.echo("No habits found.")
        return
    for h in habits:
        click.echo(f"{h.id}: {h.name} ({h.periodicity.value})")


@cli.command("list-by")
@click.argument("periodicity")
def list_by(periodicity: str) -> None:
    """List habits by periodicity."""
    init_db()
    habits = list_habits_by(Periodicity(periodicity))
    for h in habits:
        click.echo(f"{h.id}: {h.name} ({h.periodicity.value})")


@cli.command()
@click.argument("name")
def check(name: str) -> None:
    """Check off a habit."""
    init_db()
    habit = get_habit_by_name(name)
    if habit is None:
        raise click.ClickException(f"No habit found with name '{name}'.")
    add_checkoff(habit, when=datetime.now(timezone.utc))
    click.echo(f"Checked off '{habit.name}'.")


@cli.group()
def analyze() -> None:
    """Analytics commands."""
    pass


@analyze.command("all")
def analyze_all() -> None:
    init_db()
    result = longest_streak_across_all()
    if result:
        click.echo(
            f"Longest streak overall: {result.streak} "
            f"({result.habit_name}, {result.periodicity.value})"
        )
    else:
        click.echo("No habits found.")


@analyze.command("habit")
@click.argument("name")
def analyze_habit(name: str) -> None:
    init_db()
    habit = get_habit_by_name(name)
    if habit is None:
        raise click.ClickException(f"No habit found with name '{name}'.")
    streak = longest_streak_for_habit(habit)
    click.echo(f"Longest streak for '{habit.name}': {streak}")


if __name__ == "__main__":
    cli()
