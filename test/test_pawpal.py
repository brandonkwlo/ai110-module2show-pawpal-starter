import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Pet, Task


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
