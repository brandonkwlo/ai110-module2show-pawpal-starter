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

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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
