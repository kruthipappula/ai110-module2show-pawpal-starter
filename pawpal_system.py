from __future__ import annotations
from dataclasses import dataclass, field, replace
from typing import List, Optional, Dict, Any, Tuple
import datetime


@dataclass
class Task:
    description: str
    time: str
    frequency: str
    duration: int = 15  # minutes
    due_date: datetime.date = field(default_factory=datetime.date.today)
    completed: bool = False

    def mark_complete(self):
        """Mark the task as completed."""
        self.completed = True

    def next_due_date(self) -> Optional[datetime.date]:
        """Return this task's next due date, or None if it doesn't recur.

        "daily" advances by one day, "weekly" by seven — both via timedelta,
        which rolls over month/year boundaries correctly on its own.
        """
        if self.frequency == "daily":
            return self.due_date + datetime.timedelta(days=1)
        if self.frequency == "weekly":
            return self.due_date + datetime.timedelta(days=7)
        return None  # "once" tasks don't recur

    def next_occurrence(self) -> Optional["Task"]:
        """Return a fresh, pending copy of this task due on its next occurrence.

        Only "daily" and "weekly" tasks recur; "once" tasks return None.
        """
        next_date = self.next_due_date()
        if next_date is None:
            return None
        return replace(self, due_date=next_date, completed=False)

    def occurs_on(self, date: datetime.date) -> bool:
        """Return True if this task is due on the given date."""
        if self.frequency == "once":
            return self.due_date == date and not self.completed
        return self.due_date == date  # "daily" / "weekly": due on this specific occurrence's date

    def start_datetime(self) -> datetime.datetime:
        """Parse the task's time string into a comparable datetime."""
        return datetime.datetime.strptime(self.time, "%H:%M")

    def end_datetime(self) -> datetime.datetime:
        """Return when this task finishes, based on its duration."""
        return self.start_datetime() + datetime.timedelta(minutes=self.duration)

    def overlaps(self, other: "Task") -> bool:
        """Return True if this task's time window overlaps another's."""
        return self.start_datetime() < other.end_datetime() and other.start_datetime() < self.end_datetime()


@dataclass
class Pet:
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to this pet."""
        self.tasks.append(task)

    def get_tasks(self):
        """Return all tasks for this pet."""
        return self.tasks


@dataclass
class Conflict:
    task_a: Task
    pet_a: Pet
    task_b: Task
    pet_b: Pet

    @property
    def same_pet(self) -> bool:
        """True if both overlapping tasks belong to the same pet."""
        return self.pet_a is self.pet_b

    def warning_message(self) -> str:
        """Return a plain-English warning describing this conflict."""
        kind = "same pet" if self.same_pet else "different pets"
        return (
            f"Warning [{kind}]: {self.pet_a.name}'s {self.task_a.description} ({self.task_a.time}) "
            f"overlaps {self.pet_b.name}'s {self.task_b.description} ({self.task_b.time})"
        )


class Owner:
    def __init__(self, name: str):
        """Initialize the owner with a name and an empty pet list."""
        self.name = name
        self.pets = []

    def add_pet(self, pet: Pet):
        """Add a pet to the owner's list."""
        self.pets.append(pet)

    def get_all_tasks(self):
        """Return all tasks from every pet."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    def __init__(self, owner: Owner):
        """Initialize the scheduler for a given owner."""
        self.owner = owner

    def get_daily_schedule(
        self,
        pet_name: Optional[str] = None,
        status: Optional[str] = None,
        date: Optional[datetime.date] = None,
    ):
        """Build a day's schedule, optionally filtered by pet and/or status.

        pet_name: only include tasks belonging to this pet (default: all pets)
        status: "completed", "pending", or None for both
        date: which day to build the schedule for (default: today); controls
            which recurring tasks are included via Task.occurs_on()
        """
        date = date or datetime.date.today()
        tasks = self.filter_tasks(pet_name=pet_name, status=status)
        tasks = [task for task in tasks if task.occurs_on(date)]
        return self.sort_by_time(tasks)

    def filter_tasks(self, pet_name: Optional[str] = None, status: Optional[str] = None) -> List[Task]:
        """Return tasks filtered by pet name and/or completion status.

        pet_name: only include tasks belonging to this pet (default: all pets)
        status: "completed", "pending", or None for both
        """
        if pet_name is None:
            tasks = self.owner.get_all_tasks()
        else:
            pet = next((p for p in self.owner.pets if p.name == pet_name), None)
            tasks = pet.get_tasks() if pet else []

        if status == "completed":
            return [task for task in tasks if task.completed]
        if status == "pending":
            return [task for task in tasks if not task.completed]
        return tasks

    def sort_by_time(self, tasks: List[Task]):
        """Sort tasks by time."""
        return sorted(tasks, key=lambda task: task.start_datetime())

    def complete_task(self, task: Task) -> Optional[Task]:
        """Mark a task complete and, if it recurs, schedule its next occurrence.

        Returns the newly created Task for the next occurrence, or None if
        the task doesn't recur (frequency == "once").
        """
        task.mark_complete()
        next_task = task.next_occurrence()
        if next_task is None:
            return None

        owning_pet = next(
            (pet for pet in self.owner.pets if any(t is task for t in pet.get_tasks())),
            None,
        )
        if owning_pet is not None:
            owning_pet.add_task(next_task)
        return next_task

    def find_conflicts(self, date: Optional[datetime.date] = None) -> List[Conflict]:
        """Return every pair of tasks scheduled at overlapping times on the given day.

        Checks across the whole owner's calendar — two tasks conflict whether
        they belong to the same pet (that pet can't be in two places at once)
        or to different pets (the owner can't attend to both at once). Each
        Conflict records which pet each task belongs to via its `same_pet`
        property, so callers can tell the two cases apart.

        Uses a sweep over tasks sorted by start time, tracking every task
        still "active" (not yet finished), so nested/non-adjacent overlaps
        are caught too, not just overlaps between consecutive tasks.
        """
        date = date or datetime.date.today()
        scheduled = [
            (task, pet)
            for pet in self.owner.pets
            for task in pet.get_tasks()
            if task.occurs_on(date)
        ]
        scheduled.sort(key=lambda pair: pair[0].start_datetime())

        conflicts = []
        active: List[Tuple[Task, Pet]] = []
        for task, pet in scheduled:
            active = [(t, p) for t, p in active if t.end_datetime() > task.start_datetime()]
            for other_task, other_pet in active:
                conflicts.append(Conflict(other_task, other_pet, task, pet))
            active.append((task, pet))
        return conflicts

    def describe_conflicts(self, date: Optional[datetime.date] = None) -> List[str]:
        """Return conflicts as warning strings instead of Conflict objects.

        This never raises — an empty list means no conflicts. It's meant for
        callers (CLI output, a Streamlit warning box, logs) that just want a
        human-readable heads-up without inspecting Task/Pet objects directly,
        and without blocking whatever action triggered the check.
        """
        return [conflict.warning_message() for conflict in self.find_conflicts(date)]
