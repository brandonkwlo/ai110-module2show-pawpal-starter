import streamlit as st

from pawpal_system import Planner, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")
st.title("🐾 PawPal+")

# ── Session state ────────────────────────────────────────────────────────────
if "planner" not in st.session_state:
    st.session_state.planner = Planner()

planner: Planner = st.session_state.planner

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Owner & Pet")
    owner_name = st.text_input("Owner name", value="Jordan")
    default_pet = st.text_input("Default pet name", value="Mochi")
    st.divider()
    if st.button("Clear all tasks", type="secondary"):
        st.session_state.planner = Planner()
        st.rerun()

# ── Tabs ─────────────────────────────────────────────────────────────────────
tab_add, tab_schedule, tab_filter, tab_conflicts = st.tabs(
    ["➕ Add Task", "📅 Schedule", "🔍 Filter", "⚠️ Conflicts"]
)

# ── Tab 1: Add Task ──────────────────────────────────────────────────────────
with tab_add:
    st.subheader("Add a New Task")
    with st.form("add_task_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            task_title = st.text_input("Task title", value="Morning walk")
            task_time = st.text_input("Time (e.g. 8:00 AM or 14:30)", value="8:00 AM")
            task_pet = st.text_input("Pet name", value=default_pet)
        with col2:
            priority = st.selectbox("Priority", ["high", "medium", "low"])
            constraint = st.selectbox("Constraint", ["Morning", "Afternoon", "Evening", "Any"])
            recurrence = st.selectbox(
                "Recurrence",
                ["", "daily", "weekly"],
                format_func=lambda x: x or "One-time",
            )
        due_date_val = st.date_input("Start date (required for recurring tasks)")

        if st.form_submit_button("Add Task", type="primary"):
            task_id = str(len(planner.get_tasks()) + 1)
            planner.add_task(Task(
                task_id=task_id,
                activity_name=task_title,
                description=task_title,
                priority=priority,
                constraint=constraint,
                time=task_time,
                pet_name=task_pet,
                recurrence=recurrence,
                due_date=due_date_val.isoformat() if recurrence else "",
            ))
            suffix = f" — recurs {recurrence}" if recurrence else ""
            st.success(f"Added: **{task_title}** at {task_time}{suffix}")

# ── Tab 2: Schedule (sorted by time) ─────────────────────────────────────────
with tab_schedule:
    st.subheader(f"Daily Schedule for {owner_name}")

    sorted_tasks = planner.sort_by_time()

    if not sorted_tasks:
        st.info("No tasks yet. Add some in the **Add Task** tab.")
    else:
        # Surface conflict warnings at the top of the schedule
        for warning in planner.find_conflicts():
            st.warning(warning)

        st.dataframe(
            [
                {
                    "Time": t.time,
                    "Task": t.activity_name,
                    "Pet": t.pet_name or "—",
                    "Priority": t.priority.capitalize(),
                    "Constraint": t.constraint,
                    "Recurrence": t.recurrence or "one-time",
                    "Due Date": t.due_date or "—",
                    "Status": t.status,
                }
                for t in sorted_tasks
            ],
            use_container_width=True,
        )

        st.divider()
        st.subheader("Complete a Task")
        incomplete = [t for t in planner.get_tasks() if t.status == "incomplete"]
        if incomplete:
            label_map = {t.task_id: f"{t.task_id}: {t.activity_name} at {t.time}" for t in incomplete}
            selected_id = st.selectbox(
                "Select task to mark complete",
                options=list(label_map.keys()),
                format_func=lambda x: label_map[x],
            )
            if st.button("Mark Complete", type="primary"):
                next_task = planner.complete_task(selected_id)
                if next_task:
                    st.success(
                        f"Done! Next occurrence auto-scheduled for "
                        f"**{next_task.due_date}** (task ID {next_task.task_id})."
                    )
                else:
                    st.success("Task marked complete.")
                st.rerun()
        else:
            st.success("All tasks are complete!")

# ── Tab 3: Filter Tasks ───────────────────────────────────────────────────────
with tab_filter:
    st.subheader("Filter Tasks")
    fc1, fc2 = st.columns(2)
    with fc1:
        filter_status = st.selectbox("Status", ["(any)", "incomplete", "complete"])
    with fc2:
        all_pets = sorted({t.pet_name for t in planner.get_tasks() if t.pet_name})
        filter_pet = st.selectbox("Pet", ["(any)"] + list(all_pets))

    status_arg = None if filter_status == "(any)" else filter_status
    pet_arg = None if filter_pet == "(any)" else filter_pet

    filtered = planner.select_tasks(status=status_arg, pet_name=pet_arg)

    if not filtered:
        st.info("No tasks match the selected filters.")
    else:
        st.caption(f"{len(filtered)} task(s) found")
        st.table(
            [
                {
                    "Time": t.time,
                    "Task": t.activity_name,
                    "Pet": t.pet_name or "—",
                    "Priority": t.priority.capitalize(),
                    "Status": t.status,
                    "Recurrence": t.recurrence or "one-time",
                }
                for t in filtered
            ]
        )

# ── Tab 4: Conflicts ──────────────────────────────────────────────────────────
with tab_conflicts:
    st.subheader("Conflict Report")
    conflicts = planner.find_conflicts()

    if not conflicts:
        st.success("No scheduling conflicts detected.")
    else:
        st.error(f"{len(conflicts)} conflict(s) found in the active schedule.")
        for warning in conflicts:
            st.warning(warning)
        st.caption("Tip: open the **Add Task** tab, then reschedule one of the conflicting tasks to a different time slot.")
