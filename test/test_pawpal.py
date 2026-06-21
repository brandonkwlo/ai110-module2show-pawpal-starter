import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Pet, Task, Planner


def make_task(task_id="1"):
    return Task(
        task_id=task_id,
        activity_name="Walk",
        description="Walk in the park",
        priority="High",
        constraint="Morning",
        time="7:00 AM",
    )


def test_mark_complete_changes_status():
    task = make_task()
    assert task.status == "incomplete"
    task.mark_complete()
    assert task.status == "complete"


def test_add_task_to_pet_increases_count():
    pet = Pet(name="Buddy", age=3, health_condition="Good", species="Dog")
    assert len(pet.tasks) == 0
    pet.add_task(make_task("1"))
    pet.add_task(make_task("2"))
    assert len(pet.tasks) == 2


# --- Sorting correctness ---

def test_sort_by_time_returns_chronological_order():
    """Tasks added out of order should come back sorted earliest to latest."""
    planner = Planner()
    planner.add_task(Task("3", "Dinner",    "", "Low",  "", "6:00 PM"))
    planner.add_task(Task("1", "Walk",      "", "High", "", "7:00 AM"))
    planner.add_task(Task("2", "Grooming",  "", "Med",  "", "12:00 PM"))

    sorted_tasks = planner.sort_by_time()

    assert [t.activity_name for t in sorted_tasks] == ["Walk", "Grooming", "Dinner"]


# --- Recurrence logic ---

def test_completing_daily_task_schedules_next_day():
    """Completing a daily task should add a new task due the following day."""
    planner = Planner()
    planner.add_task(Task(
        task_id="1",
        activity_name="Morning Feed",
        description="Feed Buddy",
        priority="High",
        constraint="Morning",
        time="8:00 AM",
        pet_name="Buddy",
        recurrence="daily",
        due_date="2024-06-15",
    ))

    next_task = planner.complete_task("1")

    assert next_task is not None
    assert next_task.due_date == "2024-06-16"
    assert next_task.status == "incomplete"
    assert len(planner.get_tasks()) == 2  # original + new occurrence


# --- Conflict detection ---

def test_find_conflicts_flags_duplicate_times():
    """Two incomplete tasks at the same time should produce a conflict warning."""
    planner = Planner()
    planner.add_task(Task("1", "Walk",  "", "High", "", "8:00 AM", pet_name="Buddy"))
    planner.add_task(Task("2", "Bath",  "", "Med",  "", "8:00 AM", pet_name="Buddy"))

    warnings = planner.find_conflicts()

    assert len(warnings) == 1
    assert "8:00 AM" in warnings[0].upper()


def test_find_conflicts_ignores_completed_tasks():
    """A completed task sharing a time slot should not trigger a conflict."""
    planner = Planner()
    planner.add_task(Task("1", "Walk", "", "High", "", "8:00 AM", status="complete"))
    planner.add_task(Task("2", "Bath", "", "Med",  "", "8:00 AM"))

    warnings = planner.find_conflicts()

    assert warnings == []
