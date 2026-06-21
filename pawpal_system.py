from dataclasses import dataclass, field
from datetime import date, datetime, timedelta


def _parse_time(time_str: str) -> datetime:
    """Convert a time string to a datetime for comparison.

    Tries 12-hour format ("8:00 AM") first, then 24-hour ("08:00").
    Returns datetime.max for any string that matches neither format so that
    unrecognized times sort to the end rather than raising an exception.

    Args:
        time_str: A time string entered by the owner, e.g. "7:00 AM" or "14:30".

    Returns:
        A datetime whose time component can be compared with < and sorted.
    """
    for fmt in ("%I:%M %p", "%H:%M"):
        try:
            return datetime.strptime(time_str.strip(), fmt)
        except ValueError:
            continue
    return datetime.max  # unparseable times sort last


@dataclass
class Pet:
    name: str
    age: int
    health_condition: str
    species: str
    tasks: list = field(default_factory=list)

    def add_task(self, task) -> None:
        """Append a task to this pet's task list."""
        self.tasks.append(task)

    def get_name(self) -> str:
        """Return the pet's name."""
        pass

    def set_name(self, name: str) -> None:
        """Update the pet's name."""
        pass

    def get_age(self) -> int:
        """Return the pet's age."""
        pass

    def set_age(self, age: int) -> None:
        """Update the pet's age."""
        pass

    def get_health_condition(self) -> str:
        """Return the pet's current health condition."""
        pass

    def set_health_condition(self, condition: str) -> None:
        """Update the pet's health condition."""
        pass

    def get_species(self) -> str:
        """Return the pet's species."""
        pass

    def set_species(self, species: str) -> None:
        """Update the pet's species."""
        pass


@dataclass
class Task:
    task_id: str
    activity_name: str
    description: str
    priority: str
    constraint: str
    time: str
    status: str = "incomplete"
    pet_name: str = ""
    recurrence: str = ""       # "daily", "weekly", or "" for one-time
    due_date: str = ""         # "YYYY-MM-DD"; empty means no specific date

    def get_info(self) -> dict:
        """Return all task fields as a dictionary."""
        pass

    def mark_complete(self) -> None:
        """Mark this task as complete."""
        self.status = "complete"

    def next_occurrence(self, new_id: str) -> "Task":
        """Return a new Task scheduled for the next recurrence date.

        Parses self.due_date as an ISO date, advances it by 1 day (daily) or
        7 days (weekly) using timedelta, and returns a fresh Task with the
        same fields but a reset status of "incomplete" and the new due date.
        The original task is not modified.

        Args:
            new_id: The task_id to assign to the newly created Task.

        Returns:
            A new Task instance with due_date set to the next occurrence.

        Raises:
            ValueError: If self.recurrence is empty or self.due_date is empty.
        """
        if not self.recurrence:
            raise ValueError(f"Task '{self.activity_name}' is not a recurring task.")
        if not self.due_date:
            raise ValueError(f"Task '{self.activity_name}' has no due_date to advance from.")

        current = date.fromisoformat(self.due_date)
        delta = timedelta(days=1) if self.recurrence == "daily" else timedelta(weeks=1)
        next_date = current + delta

        return Task(
            task_id=new_id,
            activity_name=self.activity_name,
            description=self.description,
            priority=self.priority,
            constraint=self.constraint,
            time=self.time,
            pet_name=self.pet_name,
            recurrence=self.recurrence,
            due_date=next_date.isoformat(),
        )


@dataclass
class Planner:
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to the planner."""
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> None:
        """Remove a task from the planner by its ID."""
        pass

    def select_tasks(self, status: str = None, pet_name: str = None) -> list[Task]:
        """Return tasks filtered by completion status and/or pet name.

        Both filters are optional and can be combined. Each filter narrows the
        result of the previous one, so passing both returns only tasks that satisfy
        both conditions simultaneously. All comparisons are case-insensitive.

        Args:
            status:   "complete" or "incomplete". Pass None to skip status filtering.
            pet_name: Name of the pet whose tasks to return. Pass None to include
                      tasks for all pets.

        Returns:
            A list of Task objects that match every supplied filter. Returns all
            tasks when both arguments are None.
        """
        results = self.tasks
        if status is not None:
            results = [t for t in results if t.status.lower() == status.lower()]
        if pet_name is not None:
            results = [t for t in results if t.pet_name.lower() == pet_name.lower()]
        return results

    def complete_task(self, task_id: str) -> "Task | None":
        """Mark a task complete and auto-schedule the next occurrence if recurring.

        Looks up the task by task_id, calls mark_complete() on it, then checks
        whether it has a recurrence and a due_date. If both are present, calls
        next_occurrence() and appends the result to the planner automatically.

        Args:
            task_id: The unique ID of the task to complete.

        Returns:
            The newly created next-occurrence Task if one was scheduled, or None
            for one-time tasks.

        Raises:
            ValueError: If no task with the given task_id exists in the planner.
        """
        target = next((t for t in self.tasks if t.task_id == task_id), None)
        if target is None:
            raise ValueError(f"No task found with id '{task_id}'.")

        target.mark_complete()

        if target.recurrence and target.due_date:
            new_id = str(len(self.tasks) + 1)
            next_task = target.next_occurrence(new_id)
            self.add_task(next_task)
            return next_task

        return None

    def organize_tasks(self, priority: str) -> list[Task]:
        """Return tasks sorted by the given priority level."""
        pass

    def sort_by_time(self) -> list[Task]:
        """Return all tasks sorted in chronological order by their time attribute.

        Uses _parse_time as the sort key so that times are compared as datetime
        objects rather than raw strings. Without this, "9:00 AM" would sort after
        "12:00 PM" alphabetically. Tasks with unrecognized time strings are placed
        at the end of the list.

        Returns:
            A new list of Task objects ordered earliest to latest. The original
            self.tasks list is not modified.
        """
        return sorted(self.tasks, key=lambda t: _parse_time(t.time))

    def find_conflicts(self) -> list[str]:
        """Return warning messages for every time slot that has more than one incomplete task.

        Groups incomplete tasks by their normalized time string (uppercased and
        stripped) and reports any group with two or more tasks. Completed tasks are
        excluded because they no longer occupy a time slot in the active schedule.

        This is a lightweight exact-match strategy: two tasks conflict only when
        they share the same start time. Overlapping durations are not detected
        because Task has no duration field.

        Returns:
            A list of human-readable warning strings, one per conflicting time slot.
            Returns an empty list when the schedule has no conflicts. Never raises.
        """
        warnings = []
        slots: dict[str, list[Task]] = {}

        for task in self.tasks:
            if task.status == "complete":
                continue
            # Normalize to a consistent key so "8:00 AM" and "8:00 am" match
            key = task.time.strip().upper()
            slots.setdefault(key, []).append(task)

        for time_key, clashing in slots.items():
            if len(clashing) < 2:
                continue
            names = ", ".join(
                f"'{t.activity_name}'" + (f" ({t.pet_name})" if t.pet_name else "")
                for t in clashing
            )
            warnings.append(f"WARNING: Conflict at {time_key} — {names}")

        return warnings

    def get_tasks(self) -> list[Task]:
        """Return the full list of tasks in the planner."""
        return self.tasks


@dataclass
class Owner:
    name: str
    pets_owned: list[Pet] = field(default_factory=list)

    def add_task(self, task: Task, planner: Planner) -> None:
        """Add a new task to the given planner."""
        pass

    def modify_task(self, task_id: str, updated_task: Task, planner: Planner) -> None:
        """Replace an existing task in the planner with an updated version."""
        pass

    def provide_task_data(self) -> dict:
        """Return raw task input data supplied by the owner."""
        pass
