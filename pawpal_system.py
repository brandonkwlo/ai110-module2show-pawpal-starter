from dataclasses import dataclass, field


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

    def get_info(self) -> dict:
        """Return all task fields as a dictionary."""
        pass

    def mark_complete(self) -> None:
        """Mark this task as complete."""
        self.status = "complete"


@dataclass
class Planner:
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to the planner."""
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> None:
        """Remove a task from the planner by its ID."""
        pass

    def select_tasks(self, constraint: str) -> list[Task]:
        """Return tasks that match the given constraint."""
        pass

    def organize_tasks(self, priority: str) -> list[Task]:
        """Return tasks sorted by the given priority level."""
        pass

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
