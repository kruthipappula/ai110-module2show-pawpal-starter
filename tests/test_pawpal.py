from pawpal_system import Task, Pet


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
