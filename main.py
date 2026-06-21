from pawpal_system import Owner, Pet, Planner, Task

def main():
    # Create an owner
    owner = Owner(name="Alice")

    # Create and add pet to the owner list
    pet = Pet(name="Buddy", age=5, health_condition="Good", species="Dog")
    pet2 = Pet(name="Mittens", age=3, health_condition="Fair", species="Cat")

    owner.pets_owned.append(pet)
    owner.pets_owned.append(pet2)

    # Create a planner and add some tasks
    planner = Planner()
    task1 = Task(task_id="1", activity_name="Walk Buddy", description="Take Buddy for a walk in the park", priority="High", constraint="Morning", time="7:00 AM")
    task2 = Task(task_id="2", activity_name="Feed Buddy", description="Feed Buddy his breakfast", priority="Medium", constraint="Morning", time="8:00 AM")
    task3 = Task(task_id="3", activity_name="Vet Appointment", description="Take Mittens to the vet for a check-up", priority="High", constraint="Afternoon", time="2:00 PM")
    
    planner.add_task(task1)
    planner.add_task(task2)
    planner.add_task(task3)

    # Display the owner's pets and their tasks
    print(f"Owner: {owner.name}")
    for pet in owner.pets_owned:
        print(f"Pet: {pet.name}, Age: {pet.age}, Health: {pet.health_condition}, Species: {pet.species}")
    
    print("Tasks:")
    for task in planner.get_tasks():
        print(f"{task.activity_name} - {task.description} (Priority: {task.priority}, Time: {task.time})")

if __name__ == "__main__":
    main()