# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

## 🧪 Testing PawPal+

Run the full test suite from the project root:

```bash
python -m pytest test/test_pawpal.py -v
```

### What the tests cover

| Test | What it verifies |
| ---- | ---------------- |
| `test_mark_complete_changes_status` | `Task.mark_complete()` flips status from `"incomplete"` to `"complete"` |
| `test_add_task_to_pet_increases_count` | `Pet.add_task()` appends to the pet's task list |
| `test_sort_by_time_returns_chronological_order` | `Planner.sort_by_time()` orders tasks earliest → latest regardless of insertion order |
| `test_completing_daily_task_schedules_next_day` | Completing a `"daily"` recurring task auto-schedules a new task for the following day |
| `test_find_conflicts_flags_duplicate_times` | `Planner.find_conflicts()` emits a warning when two incomplete tasks share the same start time |
| `test_find_conflicts_ignores_completed_tasks` | Completed tasks are excluded from conflict detection |

### Successful test run output

```
============================= test session starts ==============================
platform darwin -- Python 3.12.2, pytest-9.0.3, pluggy-1.6.0 -- /opt/miniconda3/bin/python
cachedir: .pytest_cache
rootdir: /Users/brandonlo/My Folder/[03] Learning/CPAI110TF/ai110-module2show-pawpal-starter
plugins: anyio-4.13.0
collecting ... collected 6 items

test/test_pawpal.py::test_mark_complete_changes_status PASSED            [ 16%]
test/test_pawpal.py::test_add_task_to_pet_increases_count PASSED         [ 33%]
test/test_pawpal.py::test_sort_by_time_returns_chronological_order PASSED [ 50%]
test/test_pawpal.py::test_completing_daily_task_schedules_next_day PASSED [ 66%]
test/test_pawpal.py::test_find_conflicts_flags_duplicate_times PASSED    [ 83%]
test/test_pawpal.py::test_find_conflicts_ignores_completed_tasks PASSED  [100%]

============================== 6 passed in 0.02s ==============================
```

### Confidence Level: ★★★★☆ (4/5)

The core scheduling behaviors — time sorting, daily recurrence, and conflict detection — are all tested and passing. The 4/5 rating reflects that the `Pet` getter/setter stubs (`get_name`, `set_age`, etc.) and `Planner.organize_tasks()` are not yet implemented, so those code paths have no coverage. Reliability is high for the features that are complete.

## 📐 Smarter Scheduling

| Feature           | Method(s) | Notes |
| ----------------- | --------- | ----- |
| Task sorting      | `Planner.sort_by_time()` | Sorts tasks chronologically using `datetime.strptime` via the `_parse_time` helper. Raw string comparison is avoided because it would sort "9:00 AM" after "12:00 PM" alphabetically. Unrecognized time strings fall to the end of the list instead of raising an error. |
| Filtering         | `Planner.select_tasks(status, pet_name)` | Filters the task list by completion status ("complete" / "incomplete"), pet name, or both combined. Both arguments are optional and case-insensitive, so callers can mix and match without needing separate methods. |
| Conflict detection | `Planner.find_conflicts()` | Groups all incomplete tasks by their normalized start time and reports any slot with two or more tasks. Returns a list of human-readable warning strings — one per conflict — and never raises. Completed tasks are excluded because they no longer occupy a slot. |
| Recurring tasks   | `Task.next_occurrence(new_id)` and `Planner.complete_task(task_id)` | Tasks carry a `recurrence` field ("daily" or "weekly") and a `due_date`. When `complete_task()` marks a recurring task done, it calls `next_occurrence()`, which uses `timedelta` to advance the due date by 1 day or 7 days and returns a fresh task with reset status. The new task is added to the planner automatically. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

## Sample Output

````
Owner: Alice
Pet: Buddy, Age: 5, Health: Good, Species: Dog
Pet: Mittens, Age: 3, Health: Fair, Species: Cat
Tasks:
Walk Buddy - Take Buddy for a walk in the park (Priority: High, Time: 7:00 AM)
Feed Buddy - Feed Buddy his breakfast (Priority: Medium, Time: 8:00 AM)
Vet Appointment - Take Mittens to the vet for a check-up (Priority: High, Time: 2:00 PM)
```
````
