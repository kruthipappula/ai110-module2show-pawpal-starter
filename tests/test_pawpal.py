import datetime

import pytest

from pawpal_system import Task, Pet, Owner, Scheduler


def test_mark_complete_changes_status():
    task = Task(description="Feed", time="08:00", frequency="daily")
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Rex", species="Dog")
    assert len(pet.get_tasks()) == 0

    pet.add_task(Task(description="Walk", time="09:00", frequency="daily"))

    assert len(pet.get_tasks()) == 1


def test_sort_by_time_returns_chronological_order():
    today = datetime.date.today()
    pet = Pet(name="Rex", species="Dog")
    # Added out of order on purpose so the test actually proves sorting happened.
    pet.add_task(Task(description="Dinner", time="18:00", frequency="once", due_date=today))
    pet.add_task(Task(description="Breakfast", time="07:00", frequency="once", due_date=today))
    pet.add_task(Task(description="Walk", time="12:30", frequency="once", due_date=today))

    owner = Owner(name="Alex")
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    schedule = scheduler.get_daily_schedule(date=today)

    assert [task.description for task in schedule] == ["Breakfast", "Walk", "Dinner"]


def test_complete_task_creates_next_daily_occurrence():
    today = datetime.date.today()
    task = Task(description="Feed", time="08:00", frequency="daily", due_date=today)
    pet = Pet(name="Rex", species="Dog")
    pet.add_task(task)

    owner = Owner(name="Alex")
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    next_task = scheduler.complete_task(task)

    assert task.completed is True
    assert next_task is not None
    assert next_task.due_date == today + datetime.timedelta(days=1)
    assert next_task.completed is False
    # The new occurrence should actually be attached to the pet, not just returned.
    assert next_task in pet.get_tasks()


def test_find_conflicts_detects_duplicate_times():
    today = datetime.date.today()
    pet = Pet(name="Rex", species="Dog")
    pet.add_task(Task(description="Walk", time="09:00", frequency="once", due_date=today, duration=30))
    pet.add_task(Task(description="Vet visit", time="09:15", frequency="once", due_date=today, duration=30))

    owner = Owner(name="Alex")
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    conflicts = scheduler.find_conflicts(date=today)

    assert len(conflicts) == 1
    conflict = conflicts[0]
    assert conflict.same_pet is True
    assert {conflict.task_a.description, conflict.task_b.description} == {"Walk", "Vet visit"}


def test_invalid_frequency_raises():
    with pytest.raises(ValueError):
        Task(description="Groom", time="10:00", frequency="monthly")


def test_invalid_time_format_raises():
    with pytest.raises(ValueError):
        Task(description="Groom", time="25:00", frequency="daily")


def test_same_time_ties_keep_insertion_order():
    today = datetime.date.today()
    pet = Pet(name="Rex", species="Dog")
    pet.add_task(Task(description="Walk", time="08:00", frequency="daily", due_date=today))
    pet.add_task(Task(description="Medication", time="08:00", frequency="daily", due_date=today))

    owner = Owner(name="Alex")
    owner.add_pet(pet)
    schedule = Scheduler(owner).get_daily_schedule(date=today)

    assert [task.description for task in schedule] == ["Walk", "Medication"]


def test_filter_by_pet_name():
    today = datetime.date.today()
    mochi = Pet(name="Mochi", species="dog")
    mochi.add_task(Task(description="Walk", time="08:00", frequency="daily", due_date=today))
    whiskers = Pet(name="Whiskers", species="cat")
    whiskers.add_task(Task(description="Feed", time="07:30", frequency="daily", due_date=today))

    owner = Owner(name="Alex")
    owner.add_pet(mochi)
    owner.add_pet(whiskers)
    schedule = Scheduler(owner).get_daily_schedule(pet_name="Mochi", date=today)

    assert [task.description for task in schedule] == ["Walk"]


def test_filter_by_unknown_pet_name_returns_empty():
    owner = Owner(name="Alex")
    owner.add_pet(Pet(name="Mochi", species="dog"))

    schedule = Scheduler(owner).get_daily_schedule(pet_name="Ghost")

    assert schedule == []


def test_filter_by_status():
    today = datetime.date.today()
    pet = Pet(name="Rex", species="Dog")
    pet.add_task(Task(description="Walk", time="08:00", frequency="daily", due_date=today, completed=True))
    pet.add_task(Task(description="Feed", time="07:00", frequency="daily", due_date=today))

    owner = Owner(name="Alex")
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    pending = scheduler.get_daily_schedule(status="pending", date=today)
    completed = scheduler.get_daily_schedule(status="completed", date=today)

    assert [task.description for task in pending] == ["Feed"]
    assert [task.description for task in completed] == ["Walk"]


def test_pet_with_no_tasks_has_empty_schedule():
    owner = Owner(name="Alex")
    owner.add_pet(Pet(name="Ghost", species="cat"))

    schedule = Scheduler(owner).get_daily_schedule(pet_name="Ghost")

    assert schedule == []


def test_owner_with_no_pets_has_empty_schedule_and_no_conflicts():
    scheduler = Scheduler(Owner(name="Alex"))

    assert scheduler.get_daily_schedule() == []
    assert scheduler.describe_conflicts() == []


def test_cross_pet_conflict_detected():
    today = datetime.date.today()
    mochi = Pet(name="Mochi", species="dog")
    mochi.add_task(Task(description="Walk", time="08:00", frequency="daily", due_date=today, duration=30))
    whiskers = Pet(name="Whiskers", species="cat")
    whiskers.add_task(Task(description="Litter box", time="08:00", frequency="daily", due_date=today))

    owner = Owner(name="Alex")
    owner.add_pet(mochi)
    owner.add_pet(whiskers)
    conflicts = Scheduler(owner).find_conflicts(date=today)

    assert len(conflicts) == 1
    assert conflicts[0].same_pet is False


def test_conflicts_are_not_reported_twice():
    today = datetime.date.today()
    pet = Pet(name="Rex", species="Dog")
    pet.add_task(Task(description="Walk", time="08:00", frequency="daily", due_date=today, duration=30))
    pet.add_task(Task(description="Medication", time="08:00", frequency="daily", due_date=today, duration=5))

    owner = Owner(name="Alex")
    owner.add_pet(pet)
    conflicts = Scheduler(owner).find_conflicts(date=today)

    pairs = {frozenset((c.task_a.description, c.task_b.description)) for c in conflicts}
    assert len(pairs) == len(conflicts) == 1


def test_touching_tasks_do_not_conflict():
    """One task ending exactly when the next starts is not an overlap."""
    first = Task(description="A", time="10:00", frequency="once", duration=30)
    second = Task(description="B", time="10:30", frequency="once", duration=30)

    assert first.overlaps(second) is False


def test_nested_overlap_chain_detected():
    """A long task overlapping two shorter, non-adjacent tasks (long-early and long-late, not early-late)."""
    today = datetime.date.today()
    pet = Pet(name="Rex", species="Dog")
    pet.add_task(Task(description="Long task", time="08:00", frequency="once", due_date=today, duration=60))
    pet.add_task(Task(description="Early nested", time="08:05", frequency="once", due_date=today, duration=10))
    pet.add_task(Task(description="Late nested", time="08:45", frequency="once", due_date=today, duration=10))

    owner = Owner(name="Alex")
    owner.add_pet(pet)
    conflicts = Scheduler(owner).find_conflicts(date=today)

    pairs = {frozenset((c.task_a.description, c.task_b.description)) for c in conflicts}
    assert pairs == {
        frozenset({"Long task", "Early nested"}),
        frozenset({"Long task", "Late nested"}),
    }


def test_complete_task_once_does_not_recur():
    today = datetime.date.today()
    task = Task(description="Vet checkup", time="09:00", frequency="once", due_date=today)
    pet = Pet(name="Rex", species="Dog")
    pet.add_task(task)

    owner = Owner(name="Alex")
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    next_task = scheduler.complete_task(task)

    assert next_task is None
    assert len(pet.get_tasks()) == 1


def test_uncompleted_daily_task_does_not_roll_over_automatically():
    """A daily task only reappears once complete_task() advances its due_date."""
    today = datetime.date.today()
    pet = Pet(name="Rex", species="Dog")
    pet.add_task(Task(description="Walk", time="08:00", frequency="daily", due_date=today))

    owner = Owner(name="Alex")
    owner.add_pet(pet)
    tomorrow = today + datetime.timedelta(days=1)

    assert Scheduler(owner).get_daily_schedule(date=tomorrow) == []
