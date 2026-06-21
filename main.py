from pawpal_system import Owner, Pet, Planner, Task


def print_tasks(label: str, tasks: list) -> None:
    print(f"\n--- {label} ---")
    if not tasks:
        print("  (no tasks)")
        return
    for task in tasks:
        pet_tag = f" [{task.pet_name}]" if task.pet_name else ""
        recur_tag = f" ({task.recurrence})" if task.recurrence else ""
        date_tag = f" due={task.due_date}" if task.due_date else ""
        print(f"  {task.time:<10} {task.activity_name:<25} priority={task.priority:<8} status={task.status}{recur_tag}{date_tag}{pet_tag}")


def main():
    owner = Owner(name="Alice")
    pet = Pet(name="Buddy", age=5, health_condition="Good", species="Dog")
    pet2 = Pet(name="Mittens", age=3, health_condition="Fair", species="Cat")
    owner.pets_owned.append(pet)
    owner.pets_owned.append(pet2)

    planner = Planner()

    # Tasks added intentionally out of order to prove sort_by_time works
    planner.add_task(Task(
        task_id="1", activity_name="Vet Appointment",
        description="Take Mittens to the vet", priority="High",
        constraint="Afternoon", time="2:00 PM", pet_name="Mittens",
    ))
    planner.add_task(Task(
        task_id="2", activity_name="Evening Walk",
        description="Walk Buddy after dinner", priority="Medium",
        constraint="Evening", time="6:30 PM", pet_name="Buddy",
    ))
    planner.add_task(Task(
        task_id="3", activity_name="Morning Walk",
        description="Walk Buddy before breakfast", priority="High",
        constraint="Morning", time="7:00 AM", pet_name="Buddy",
    ))
    planner.add_task(Task(
        task_id="4", activity_name="Feed Mittens",
        description="Give Mittens her morning meal", priority="Medium",
        constraint="Morning", time="8:30 AM", pet_name="Mittens",
    ))
    planner.add_task(Task(
        task_id="5", activity_name="Feed Buddy",
        description="Give Buddy his breakfast", priority="Medium",
        constraint="Morning", time="8:00 AM", pet_name="Buddy",
    ))

    # Add recurring tasks with due dates
    planner.add_task(Task(
        task_id="6", activity_name="Morning Walk",
        description="Walk Buddy before breakfast", priority="High",
        constraint="Morning", time="7:00 AM", pet_name="Buddy",
        recurrence="daily", due_date="2026-06-21",
    ))
    planner.add_task(Task(
        task_id="7", activity_name="Flea Treatment",
        description="Apply monthly flea treatment to Mittens", priority="Medium",
        constraint="Evening", time="7:00 PM", pet_name="Mittens",
        recurrence="weekly", due_date="2026-06-21",
    ))

    print(f"Owner: {owner.name}")
    print(f"Pets: {', '.join(p.name for p in owner.pets_owned)}")

    # 1. All tasks before completing anything
    print_tasks("All tasks — before completing any", planner.get_tasks())

    # 2. Complete the daily task — should auto-schedule tomorrow
    print("\n>>> Completing 'Morning Walk' (daily) via planner.complete_task()...")
    next_walk = planner.complete_task("6")
    if next_walk:
        print(f"    Auto-scheduled: '{next_walk.activity_name}' due {next_walk.due_date}")

    # 3. Complete the weekly task — should auto-schedule 7 days out
    print("\n>>> Completing 'Flea Treatment' (weekly) via planner.complete_task()...")
    next_flea = planner.complete_task("7")
    if next_flea:
        print(f"    Auto-scheduled: '{next_flea.activity_name}' due {next_flea.due_date}")

    # 4. All tasks after — completed originals + new occurrences visible
    print_tasks("All tasks — after completing recurring tasks", planner.get_tasks())

    # 5. Sorted by time
    print_tasks("All tasks — sorted by time", planner.sort_by_time())

    # 6. Filter: incomplete only (shows the newly generated occurrences)
    print_tasks("Incomplete tasks only", planner.select_tasks(status="incomplete"))

    # 7. Filter: Buddy's tasks only
    print_tasks("Buddy's tasks only", planner.select_tasks(pet_name="Buddy"))

    # 8. Filter: Mittens's incomplete tasks
    print_tasks("Mittens — incomplete tasks", planner.select_tasks(status="incomplete", pet_name="Mittens"))

    # 9. Conflict detection — add two deliberate same-time clashes then check
    print("\n>>> Adding conflicting tasks to demonstrate find_conflicts()...")

    # Same-pet conflict: Buddy has two tasks at 8:00 AM
    planner.add_task(Task(
        task_id="10", activity_name="Grooming Session",
        description="Brush Buddy's coat", priority="Low",
        constraint="Morning", time="8:00 AM", pet_name="Buddy",
    ))

    # Cross-pet conflict: both pets need attention at 2:00 PM
    planner.add_task(Task(
        task_id="11", activity_name="Playtime",
        description="Interactive play with Mittens", priority="Medium",
        constraint="Afternoon", time="2:00 PM", pet_name="Mittens",
    ))

    conflicts = planner.find_conflicts()
    print(f"\n--- Conflict Report ({len(conflicts)} conflict(s) found) ---")
    if conflicts:
        for warning in conflicts:
            print(f"  {warning}")
    else:
        print("  No conflicts detected.")


if __name__ == "__main__":
    main()
