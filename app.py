import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# --- Session state initialization ---
# Guard clauses ensure objects are created once per session, not on every rerun.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="", contact_info="", time_available=120)

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler(owner=st.session_state.owner)
    st.session_state.owner.scheduler = st.session_state.scheduler

if "plan_generated" not in st.session_state:
    st.session_state.plan_generated = False

# Convenience references — use these throughout the rest of the app
owner = st.session_state.owner
scheduler = st.session_state.scheduler

st.title("🐾 PawPal+")

# --- Owner Info ---
st.subheader("Owner Info")
col1, col2, col3 = st.columns(3)
with col1:
    owner.name = st.text_input("Your name", value=owner.name)
with col2:
    owner.contact_info = st.text_input("Contact info", value=owner.contact_info)
with col3:
    owner.time_available = st.number_input(
        "Time available today (min)", min_value=10, max_value=480, value=owner.time_available
    )

st.divider()

# --- Add a Pet ---
st.subheader("Add a Pet")
with st.form("add_pet_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        pet_name = st.text_input("Pet name")
        species = st.selectbox("Species", ["Dog", "Cat", "Bird", "Other"])
    with col2:
        breed = st.text_input("Breed")
        age = st.number_input("Age", min_value=0, max_value=30, value=1)
    with col3:
        activity_level = st.selectbox("Activity level", ["low", "medium", "high"])
        health_history = st.text_input("Health notes (comma-separated)")

    submitted = st.form_submit_button("Add Pet")
    if submitted and pet_name:
        health_list = [h.strip() for h in health_history.split(",") if h.strip()]
        new_pet = Pet(
            name=pet_name,
            age=age,
            breed=breed,
            species=species,
            activity_level=activity_level,
            health_history=health_list,
        )
        owner.add_pet(new_pet)
        st.success(f"Added {pet_name}!")

if owner.pets:
    st.write("**Your pets:**")
    for pet in owner.pets:
        st.markdown(f"- **{pet.name}** ({pet.species}, {pet.breed}, age {pet.age}) — activity: {pet.activity_level}")
else:
    st.info("No pets added yet.")

st.divider()

# --- Add a Task ---
st.subheader("Add a Task")

if not owner.pets:
    st.warning("Add a pet first before scheduling tasks.")
else:
    with st.form("add_task_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            task_pet = st.selectbox("For which pet?", [p.name for p in owner.pets])
            task_name = st.text_input("Task name", value="Morning walk")
            category = st.selectbox("Category", ["walk", "feeding", "meds", "grooming", "enrichment", "other"])
        with col2:
            duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
            priority = st.slider("Priority (1 = low, 5 = high)", min_value=1, max_value=5, value=3)
            must_occur_at = st.text_input("Fixed time (e.g. 08:00 AM)", value="")

        description = st.text_input("Description (optional)")
        task_submitted = st.form_submit_button("Add Task")

        if task_submitted and task_name:
            new_task = Task(
                name=task_name,
                category=category,
                duration=int(duration),
                priority=priority,
                description=description,
                must_occur_at=must_occur_at.strip(),
            )
            owner.add_task(task_pet, new_task)
            st.session_state.plan_generated = False  # mark plan stale
            st.success(f"Added '{task_name}' to {task_pet}!")

    all_tasks = owner.get_all_tasks()
    if all_tasks:
        st.write("**Current tasks (sorted by time):**")
        sorted_tasks = scheduler.sort_by_time()
        st.table([
            {
                "Pet": t.pet_name,
                "Task": t.name,
                "Category": t.category,
                "Duration (min)": t.duration,
                "Priority": t.priority,
                "Fixed time": t.scheduled_time or t.must_occur_at or "flexible",
                "Done": "Yes" if t.is_completed else "No",
            }
            for t in sorted_tasks
        ])

        # --- Filter panel ---
        with st.expander("Filter tasks"):
            col1, col2 = st.columns(2)
            with col1:
                pet_filter = st.selectbox(
                    "By pet", ["All"] + [p.name for p in owner.pets], key="filter_pet"
                )
            with col2:
                status_filter = st.selectbox(
                    "By status", ["All", "Incomplete", "Completed"], key="filter_status"
                )

            pet_arg = None if pet_filter == "All" else pet_filter
            status_arg = None if status_filter == "All" else (status_filter == "Completed")
            filtered = scheduler.filter_tasks(pet_name=pet_arg, completed=status_arg)

            if filtered:
                st.table([
                    {
                        "Pet": t.pet_name,
                        "Task": t.name,
                        "Category": t.category,
                        "Duration (min)": t.duration,
                        "Priority": t.priority,
                        "Done": "Yes" if t.is_completed else "No",
                    }
                    for t in filtered
                ])
            else:
                st.info("No tasks match the selected filters.")
    else:
        st.info("No tasks added yet.")

st.divider()

# --- Generate Schedule ---
st.subheader("Generate Schedule")

if st.button("Generate schedule"):
    if not owner.pets or not owner.get_all_tasks():
        st.warning("Add at least one pet and one task first.")
    else:
        scheduler.generate_plan()
        st.session_state.plan_generated = True

if st.session_state.plan_generated and scheduler.plan:
    st.success(f"Schedule generated — {sum(t.duration for t, _ in scheduler.plan)} of {owner.time_available} min planned.")

    # --- Conflict warnings ---
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            st.warning(f"Scheduling conflict: {warning}")
    else:
        st.success("No scheduling conflicts detected.")

    # --- Sorted plan table ---
    st.write("**Today's Schedule (chronological):**")
    st.table([
        {
            "Time": time_slot,
            "Pet": task.pet_name,
            "Task": task.name,
            "Category": task.category,
            "Duration (min)": task.duration,
            "Priority": task.priority,
            "Type": "Fixed" if task.must_occur_at else "Flexible",
        }
        for task, time_slot in sorted(
            scheduler.plan,
            key=lambda x: scheduler._time_to_minutes(x[1])
        )
    ])

    # --- Skipped tasks ---
    skipped = [t for t in owner.get_all_tasks() if not t.scheduled_time]
    if skipped:
        st.write("**Skipped (insufficient time):**")
        for task in skipped:
            st.warning(f"{task.name} ({task.pet_name}) — {task.duration} min, priority {task.priority}")
