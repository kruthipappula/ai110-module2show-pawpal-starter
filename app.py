import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file connects the simple Streamlit UI to your backend classes.
"""
)

st.divider()

st.subheader("Owner")
owner_name = st.text_input("Owner name", value="Jordan")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_name)
st.session_state.owner.name = owner_name
owner = st.session_state.owner

st.subheader("Add a Pet")
col1, col2 = st.columns(2)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    owner.add_pet(Pet(pet_name, species))

if owner.pets:
    st.write("Current pets:")
    st.table(
        [{"name": p.name, "species": p.species, "tasks": len(p.get_tasks())} for p in owner.pets]
    )
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Schedule a Task")

if owner.pets:
    pet_names = [p.name for p in owner.pets]
    selected_pet_name = st.selectbox("Pet", pet_names)
    selected_pet = next(p for p in owner.pets if p.name == selected_pet_name)

    col1, col2, col3 = st.columns(3)
    with col1:
        description = st.text_input("Task description", value="Morning walk")
    with col2:
        time = st.time_input("Time")
    with col3:
        frequency = st.selectbox("Frequency", ["daily", "weekly", "once"])

    if st.button("Add task"):
        selected_pet.add_task(Task(description, time.strftime("%H:%M"), frequency))
else:
    st.info("Add a pet before scheduling tasks.")

st.divider()

st.subheader("Today's Schedule")

scheduler = Scheduler(owner)

if flash := st.session_state.pop("flash", None):
    st.success(flash)

conflicts = scheduler.find_conflicts()
if conflicts:
    for conflict in conflicts:
        if conflict.same_pet:
            st.error(conflict.warning_message())
        else:
            st.warning(conflict.warning_message())
else:
    st.success("No scheduling conflicts today.")

filter_col1, filter_col2 = st.columns(2)
with filter_col1:
    pet_filter = st.selectbox("Filter by pet", ["All pets"] + [p.name for p in owner.pets])
with filter_col2:
    status_filter = st.selectbox("Filter by status", ["All", "pending", "completed"])

schedule = scheduler.get_daily_schedule(
    pet_name=None if pet_filter == "All pets" else pet_filter,
    status=None if status_filter == "All" else status_filter,
)

pet_by_task = {id(task): pet.name for pet in owner.pets for task in pet.get_tasks()}

if schedule:
    st.table(
        [
            {
                "Time": task.time,
                "Pet": pet_by_task.get(id(task), "—"),
                "Task": task.description,
                "Frequency": task.frequency,
                "Status": "✅ Done" if task.completed else "⏳ Pending",
            }
            for task in schedule
        ]
    )

    pending = [task for task in schedule if not task.completed]
    if pending:
        st.write("Mark a task complete:")
        for task in pending:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"**{task.time}** — {pet_by_task.get(id(task), '—')}: {task.description}")
            with col2:
                if st.button("Mark complete", key=f"complete-{id(task)}"):
                    scheduler.complete_task(task)
                    st.session_state.flash = f"Marked '{task.description}' complete!"
                    st.rerun()
else:
    st.info("No tasks to schedule yet.")
