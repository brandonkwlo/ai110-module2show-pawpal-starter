# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

My initial UML design included four classes: `Owner`, `Pet`, `Task`, and `Planner`.

- **Owner** is the central user of the system. It holds a list of pets and has methods to add or modify tasks in the planner, as well as provide raw task data as input.
- **Pet** stores a pet's profile — name, age, species, and health condition — with explicit getters and setters for each field so the owner can update pet info over time.
- **Task** represents a single care activity. It stores identifying info (task ID, activity name, description) along with scheduling metadata like priority and constraint, and exposes a `get_info()` method to return all fields as a dictionary.
- **Planner** acts as the scheduling engine. It holds a list of tasks and provides methods to add, remove, filter by constraint, and sort by priority so it can produce an organized daily plan.

The relationships reflect that an Owner manages one Planner and owns one or more Pets, while the Planner aggregates Tasks that can also be associated with specific Pets.

**b. Design changes**

Yes, the design changed during implementation. After converting the UML to Python class stubs, I realized the `Task` class was missing a `time` attribute. Time is essential for scheduling — without it, the `Planner` has no way to order tasks chronologically or check for conflicts in a daily plan. I added `time: str` to the `Task` dataclass and updated the UML accordingly to keep both in sync.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers four constraints: time of day, priority level, time-of-day window, and pet name.

- **Time** is the primary sort key. The `sort_by_time()` method parses each task's `time` string using `datetime.strptime` so tasks are ordered chronologically, not alphabetically. Without this, "9:00 AM" would incorrectly sort after "12:00 PM" as a raw string.
- **Priority** ("high", "medium", "low") serves as a tiebreaker when two tasks share the same time slot, so more urgent care — like a vet appointment — is surfaced first.
- **Time-of-day window** (the `constraint` field: "Morning", "Afternoon", "Evening") lets the owner associate tasks with a general part of the day, which feeds into `select_tasks()` filtering.
- **Pet name** allows the planner to scope a schedule to one pet when an owner has multiple, making the daily plan readable per animal rather than as one undifferentiated list.

I prioritized time first because scheduling is meaningless without it — every other constraint is secondary to knowing *when* something happens.

**b. Tradeoffs**

The conflict detection in `find_conflicts()` flags only tasks with an identical `time` string. It does not account for task duration, so two tasks that *overlap* without sharing an exact start time go undetected. For example, a 45-minute grooming session starting at 7:00 AM and a feeding scheduled at 7:30 AM would not trigger a warning even though they cannot both happen simultaneously.

This tradeoff is reasonable for this scenario because `Task` has no `duration_minutes` field — there is no data available to compute overlap intervals, and adding duration would require every task to carry that information accurately. For a single owner managing a small number of daily pet care tasks, exact double-bookings (the same start time) are the most critical case to catch. A lightweight string-match check surfaces the most obvious scheduling mistakes without complicating the data model or the logic needed to maintain it.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI tools at three different stages of the project. During the design phase, I asked for help identifying edge cases that my initial UML hadn't accounted for — specifically asking what happens when a pet has no tasks, or when two tasks land at exactly the same time. That conversation surfaced the conflict detection requirement before I had written any code, which is easier to design for upfront than to retrofit later.

During implementation, the most useful prompts were narrow and specific rather than open-ended. For example: "Given this `_parse_time` function that returns `datetime.max` for unrecognized strings, write a `sort_by_time` method that uses it as a sort key and doesn't modify the original list." Framing the prompt around the existing design prevented the AI from proposing an entirely different approach that would conflict with what I had already built.

During testing, I asked the AI to help me think through what the most important edge cases were for sorting and conflict detection. The answer pointed me to the `"12:00 AM"` vs `"12:00 PM"` gotcha and the case-insensitive conflict normalization issue — both of which became explicit tests.

**b. Judgment and verification**

When the AI first suggested a conflict detection approach, it recommended grouping tasks by time and comparing them pairwise. I rejected this because pairwise comparison scales quadratically — O(n²) — and the simpler dictionary-grouping approach I already had (`slots.setdefault(key, []).append(task)`) produces the same result in a single linear pass. The AI's suggestion would have worked correctly but was unnecessarily complex for a list of daily pet care tasks.

To verify my own approach, I traced through it manually with three tasks — two at `"8:00 AM"` and one at `"9:00 AM"` — and confirmed that the dictionary accumulated the right groups before the loop over slots produced exactly one warning. I also wrote `test_find_conflicts_flags_duplicate_times` and `test_find_conflicts_ignores_completed_tasks` to confirm the behavior held in code.

---

## 4. Testing and Verification

**a. What you tested**

I wrote six tests covering four behaviors:

- **Status mutation** — `test_mark_complete_changes_status` confirms that `mark_complete()` flips `status` from `"incomplete"` to `"complete"`. This is the foundation everything else builds on; if marking complete is broken, recurrence and filtering both fail silently.
- **Collection growth** — `test_add_task_to_pet_increases_count` verifies that `Pet.add_task()` actually appends to the list. Simple, but without it a bug in `field(default_factory=list)` would go unnoticed.
- **Sorting correctness** — `test_sort_by_time_returns_chronological_order` adds tasks in reverse order and checks that `sort_by_time()` returns them earliest-to-latest. This specifically guards against falling back to alphabetical string comparison, which would sort `"9:00 AM"` after `"12:00 PM"`.
- **Recurrence** — `test_completing_daily_task_schedules_next_day` uses a fixed `due_date` of `"2024-06-15"` and asserts the auto-scheduled task lands on `"2024-06-16"`. It also checks that the planner now holds two tasks, confirming the new occurrence was appended and not just returned.
- **Conflict detection (two cases)** — `test_find_conflicts_flags_duplicate_times` checks that two incomplete tasks at the same time produce exactly one warning. `test_find_conflicts_ignores_completed_tasks` checks that a completed task at the same time slot as an incomplete one does not trigger a conflict.

These tests were important because they test *behavior*, not just that the code runs. Each one would catch a specific class of bug — wrong sort key, off-by-one in date math, or incorrectly including completed tasks in the conflict check.

**b. Confidence**

I would rate my confidence at **4 out of 5**. The four core behaviors — sorting, filtering, conflict detection, and recurring auto-scheduling — are all tested and passing against edge cases, not just happy-path inputs. My confidence drops one point because the `Pet` getter/setter methods (`get_name`, `set_age`, etc.) and `Planner.organize_tasks()` are still stubs that return `None` silently. Any code path that calls them will not raise an error — it will just quietly return nothing — which is a harder class of bug to catch without explicit tests.

If I had more time, the next edge cases I would test are:
- A daily task with `due_date="2024-01-31"` advancing to `"2024-02-01"` (month boundary rollover via `timedelta`).
- `"12:00 AM"` sorting before `"1:00 AM"` — midnight is a classic failure point for 12-hour format parsing.
- `"8:00 AM"` and `"8:00 am"` being flagged as a conflict (case normalization in `find_conflicts`).
- `complete_task()` called with a nonexistent ID raising `ValueError` rather than silently doing nothing.

---

## 5. Reflection

**a. What went well**

I am most satisfied with the separation of concerns between the classes. `Task` is pure data — it knows nothing about the planner. `Planner` owns all scheduling logic and operates on lists of `Task` objects without caring what they contain. This made it straightforward to add `sort_by_time()`, `find_conflicts()`, and `complete_task()` to `Planner` without touching `Task` at all. When I needed to add recurrence, I only had to add two fields to `Task` and one method to `Planner` — the rest of the system didn't change. A design where those concerns were tangled together would have required changes in multiple places.

**b. What you would improve**

The biggest thing I would redesign is the `time` field on `Task`. Storing time as a free-text string (`"8:00 AM"`) means the system can never do arithmetic on it — it can only compare parsed copies. Every method that needs to reason about time has to call `_parse_time` first, and the original string is still what gets displayed and stored. If I had another iteration, I would store time as a `datetime.time` object internally and only convert to/from a string at the UI boundary. That would also make duration-based conflict detection possible, since you could compute end times by adding a `duration_minutes` field.

I would also implement the `Pet` getter/setter stubs and `Planner.organize_tasks()`. Right now they return `None` silently, which means the `Owner` class is effectively unusable and any UI feature that calls those methods will fail in a hard-to-diagnose way.

**c. Key takeaway**

The most important thing I learned is that AI tools are most useful when you already have a design to anchor the conversation. When I asked open-ended questions ("how should I implement scheduling?") the suggestions were generic and didn't fit what I had built. When I asked narrow questions that described my specific classes and constraints, the output was immediately usable. The lesson is that AI doesn't replace system design — it amplifies whatever design thinking you bring to it. A vague prompt produces a generic answer; a precise prompt that reflects your own understanding produces something you can actually use.
