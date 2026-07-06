import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
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
schedule = scheduler.get_daily_schedule()

for warning in scheduler.describe_conflicts():
    st.warning(warning)

if schedule:
    for task in schedule:
        col1, col2 = st.columns([4, 1])
        with col1:
            status = "Done" if task.completed else "Pending"
            st.write(f"**{task.time}** — {task.description} ({task.frequency}) · {status}")
        with col2:
            if not task.completed:
                if st.button("Mark complete", key=f"complete-{id(task)}"):
                    scheduler.complete_task(task)
                    st.rerun()
else:
    st.info("No tasks to schedule yet.")
