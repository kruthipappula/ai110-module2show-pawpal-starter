from pawpal_system import Task, Pet, Owner, Scheduler

owner = Owner("Jordan")

# Tasks are added out of chronological order on purpose, to prove the
# scheduler sorts them rather than relying on insertion order.
mochi = Pet("Mochi", "dog")
mochi.add_task(Task("Dinner", "18:00", "daily"))
mochi.add_task(Task("Vet checkup", "08:15", "once", duration=60))
mochi.add_task(Task("Morning walk", "08:00", "daily", duration=30))
mochi.add_task(Task("Medication", "08:00", "daily", duration=5))  # same pet, same exact time as the walk

whiskers = Pet("Whiskers", "cat")
whiskers.add_task(Task("Evening snack", "20:00", "daily"))
whiskers.add_task(Task("Feed breakfast", "07:30", "daily"))
whiskers.add_task(Task("Litter box cleaning", "08:00", "daily"))  # overlaps Mochi's walk

owner.add_pet(mochi)
owner.add_pet(whiskers)

# Mark one task complete so status filtering has something to exclude.
mochi.get_tasks()[0].mark_complete()  # "Dinner"

scheduler = Scheduler(owner)

print(f"Owner: {owner.name}")

print("Pets:")
for pet in owner.pets:
    print(f"- {pet.name} ({pet.species})")

print("\nToday's Schedule (sorted):")
for task in scheduler.get_daily_schedule():
    print(f"{task.time} - {task.description} ({task.frequency})")

print("\nMochi's Schedule Only (filtered by pet):")
for task in scheduler.get_daily_schedule(pet_name="Mochi"):
    print(f"{task.time} - {task.description}")

print("\nPending Tasks Only (filtered by status):")
for task in scheduler.get_daily_schedule(status="pending"):
    print(f"{task.time} - {task.description}")

print("\nConflicts Detected:")
warnings = scheduler.describe_conflicts()
if warnings:
    for warning in warnings:
        print(warning)
else:
    print("None")
