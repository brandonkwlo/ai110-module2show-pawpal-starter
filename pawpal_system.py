from dataclasses import dataclass, field


@dataclass
class Pet:
    name: str
    age: int
    health_condition: str
    species: str

    def get_name(self) -> str:
        pass

    def set_name(self, name: str) -> None:
        pass

    def get_age(self) -> int:
        pass

    def set_age(self, age: int) -> None:
        pass

    def get_health_condition(self) -> str:
        pass

    def set_health_condition(self, condition: str) -> None:
        pass

    def get_species(self) -> str:
        pass

    def set_species(self, species: str) -> None:
        pass


@dataclass
class Task:
    task_id: str
    activity_name: str
    description: str
    priority: str
    constraint: str
    time: str

    def get_info(self) -> dict:
        pass


@dataclass
class Planner:
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task_id: str) -> None:
        pass

    def select_tasks(self, constraint: str) -> list[Task]:
        pass

    def organize_tasks(self, priority: str) -> list[Task]:
        pass

    def get_tasks(self) -> list[Task]:
        pass


@dataclass
class Owner:
    name: str
    pets_owned: list[Pet] = field(default_factory=list)

    def add_task(self, task: Task, planner: Planner) -> None:
        pass

    def modify_task(self, task_id: str, updated_task: Task, planner: Planner) -> None:
        pass

    def provide_task_data(self) -> dict:
        pass
