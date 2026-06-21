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

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
