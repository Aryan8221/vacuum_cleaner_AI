import random


# Define the simple reflex agent
def simple_reflex_agent(room_states, vacuum_location):
    if room_states[vacuum_location] == 1:  # If the room is dirty, clean it
        return "clean"
    else:
        return "move"


# Define the performance measure
def performance_measure(actions, a, b):
    num_moves = actions.count("move")
    num_cleans = actions.count("clean")
    return num_moves + (a * num_cleans) + (b * num_moves)


# Function to run the agent and calculate performance
def run_agent(repetition_number, a, b):
    total_performance = 0

    for _ in range(repetition_number):
        room_states = [random.randrange(0, 2), random.randrange(0, 2)]  # Rooms: 0 clean, 1 dirty
        vacuum_location = random.randrange(0, 2)  # initial vacuum location

        actions = []
        while True:  # Run the agent for 10 steps
            action = simple_reflex_agent(room_states, vacuum_location)
            if "move" in actions and action == "move":
                break
            actions.append(action)
            if action == "move":
                vacuum_location = 1 - vacuum_location  # Switch rooms
            elif action == "clean":
                room_states[vacuum_location] = 0  # Clean the room

        # Calculate performance measure and add to the total
        performance = performance_measure(actions, a, b)
        total_performance += performance

    # Calculate the average performance measure
    avg_performance = total_performance / repetition_number
    print(avg_performance)


if __name__ == '__main__':
    a = 2
    b = 3
    repetition_number = 100
    run_agent(repetition_number, a, b)
