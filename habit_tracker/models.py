from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class Periodicity(str, Enum):
    daily = "daily"
    weekly = "weekly"


@dataclass(frozen=True)
class Habit:
    """Core OOP data model."""
    id: int
    name: str
    periodicity: Periodicity
    created_at: datetime
