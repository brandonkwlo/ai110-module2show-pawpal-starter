# PawPal+ Project Reflection

## 1. System Design

### Core User Actions

The PawPal+ user has the ability to perform the following actions:

- Add owner and pet info - enter the owner info (i.e. name) and pet info (i.e. name, breed, age, species, health history)
- Add or edit their pet care tasks - tasks will be given a duration and priority level
- Generate a daily plan - System with generate a daily plan based on the information added and then generate an explanation for the system's chosen plan

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

I added four classes: Owner, Pet, Task, and Scheduler. Pet holds the animal's profile (name, age, breed, species, health history). Task represents a single care activity with a duration, priority, and time constraints. Owner can add and edit tasks, view the generated plan, and holds pet and personal info like time availability and preferences. Scheduler owns the task list, uses owner and pet data as inputs, and is responsible for generating the daily plan and explaining its reasoning.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Made a few changes to initial design.

Owner gained a scheduler reference. The Owner methods previously took scheduler as a parameter on every call and now its stores scheduler as optional as an attribute for consistency with how Scheduler already stored owner.

Removed redundant info methods such as Scheduler get owner and pet info and Owner get pet info because the objects are directly accessible as attributes.

Key design change was updating the pets object. I have now allowed the owner to have multiple pets and maintained this change to be consistent among the scheduler and owner objects.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The scheduler considers four constraints: the owner's total time_available, each task's duration, its priority, and whether it has a fixed must_occur_at time. Fixed-time tasks were prioritized first because missing them (like medication) has real consequences — they anchor the schedule. Duration and priority then determine which flexible tasks fill the remaining time, with higher priority tasks scheduled before lower ones. time_available acts as a hard cap — tasks that don't fit are skipped entirely.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The scheduler only checks for exact time matches rather than whether a task's duration overlaps with the next task's start time, meaning two tasks starting minutes apart could still conflict without triggering a warning. This tradeoff is reasonable because generate_plan() already spaces flexible tasks sequentially so they won't overlap each other — the main real-world conflict is a user accidentally assigning two fixed tasks the same must_occur_at time, which exact matching catches directly. Since PawPal+ is a planning aid reviewed by the owner before use, a lightweight warning is sufficient without needing strict interval enforcement.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

Claude Code helped me from designing the UML diagram to implementing and refining the algorithmic methods for the objects. The prompts that I found most useful followed an 'Action + Task' template — being specific about what to do and what to do it to. For example, "Evaluate my objects with its associated methods and attributes" produced a focused, structured critique rather than a generic response. Prompts that included context (like sharing the current code) were more effective than open-ended ones.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

There was one moment where I was trying to use 'uv' (a package manager) instead of the virtual environment, as it is more resource efficient and easier to set up. However, when setting it up, Claude kept defaulting back to the virtual environment workflow. So I went through the uv documentation myself, completed the foundational setup, and then asked Claude to properly integrate it into the project — verifying each step rather than accepting its defaults.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

Tests covered task completion status, pet task count after addition, full schedule generation across two pets, chronological sort order with correct AM/PM handling (including 12:00 AM/PM edge cases), daily recurrence creating a next-day occurrence via timedelta, conflict detection flagging duplicate scheduled times, and unscheduled recurring tasks being ignored by conflict detection. These were important because the scheduling and sorting logic relies on string-based time comparisons that fail silently at edge cases — for example, midnight was initially sorted as the first task of the day rather than the last, which also broke conflict detection.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am moderately confident the scheduler works correctly for the behaviors tested — conflict detection, sorting, filtering, and recurrence all pass their tests. The main known gap is duration-overlap detection: two tasks scheduled minutes apart won't trigger a warning even if they run into each other. The next edge cases I would test are overlapping task durations and flexible tasks being assigned to time slots already occupied by fixed tasks. Duration-overlap detection was not implemented because it increases time complexity from O(n) back to O(n²) interval comparisons.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am most satisfied with the backend system design — specifically the decision to move tasks into Pet rather than Scheduler, and to have Owner and Scheduler share a bidirectional reference. These were deliberate design choices that kept responsibilities cleanly separated and made the scheduling logic straightforward to implement and test.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would improve the scheduling logic so that flexible tasks are not assigned to time slots already occupied by fixed tasks — currently generate_plan() starts flexible tasks at 8:00 AM regardless of what fixed tasks are anchored there, which can create conflicts that the system then flags as warnings. I would also redesign the Streamlit UI to make the plan display more visually clear.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

I had the notion that AI would not be that great for coding as the code is not great and breaks systems. However, now that I have access to Claude Code and can experiment without worrying about token limits, I view it differently, especially with CodePath's guidance. The code generator can still be incorrect, but it is up to the human or user to decide if they want it implemented.
