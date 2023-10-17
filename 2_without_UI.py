import random

n = 2  # Change n to adjust the grid size

# Initialize has_black_circles array to track black circles
board = [[0 for _ in range(n)] for _ in range(n)]
has_black_circles = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]

print(has_black_circles)

actions = []


def zig_zag_walk():
    walk_instruction = []
    for i in range(n):
        if i % 2 == 0:  # Even row (starting from 0)
            for j in range(n):

                if j < n - 1:
                    walk_instruction.append("right")
            if i < n - 1:
                walk_instruction.append("down")
        else:  # Odd row
            for j in range(n - 1, -1, -1):

                if j > 0:
                    walk_instruction.append("left")
            if i < n - 1:
                walk_instruction.append("down")

    print(walk_instruction)

    return walk_instruction


def simple_reflex_agent(has_black_circles, vacuum_location):
    if has_black_circles[vacuum_location[0]][vacuum_location[1]] == 1:  # If the room is dirty, clean it
        return "clean"
    else:
        return "move"


# Define the performance measure
def performance_measure(actions, a, b):
    num_moves = actions.count("move")
    num_cleans = actions.count("clean")
    return num_moves + (a * num_cleans) + (b * num_moves)


def move_up(array, current_position):
    row, col = current_position
    if row > 0:
        array[row][col] = 0  # Clear the current position
        array[row - 1][col] = 1  # Move up
        vacuum_location[0], vacuum_location[1] = row - 1, col

        board[vacuum_location[0]][vacuum_location[1]] = 1
        actions.append("move")
        return row - 1, col
    else:
        vacuum_location[0], vacuum_location[1] = current_position
        return current_position  # If already at the top row, do nothing and return the same position


def move_down(array, current_position):
    row, col = current_position
    if row < n - 1:
        array[row][col] = 0  # Clear the current position
        array[row + 1][col] = 1  # Move down
        vacuum_location[0], vacuum_location[1] = row + 1, col

        board[vacuum_location[0]][vacuum_location[1]] = 1
        actions.append("move")
        return row + 1, col
    else:
        vacuum_location[0], vacuum_location[1] = current_position
        return current_position  # If already at the bottom row, do nothing and return the same position


def move_left(array, current_position):
    row, col = current_position
    if col > 0:
        array[row][col] = 0  # Clear the current position
        array[row][col - 1] = 1  # Move to the left
        vacuum_location[0], vacuum_location[1] = row, col - 1

        board[vacuum_location[0]][vacuum_location[1]] = 1
        actions.append("move")
        return row, col - 1
    else:
        vacuum_location[0], vacuum_location[1] = current_position
        return current_position  # If already at the leftmost position, do nothing and return the same position


def move_right(array, current_position):
    row, col = current_position
    if col < n - 1:
        array[row][col] = 0  # Clear the current position
        array[row][col + 1] = 1  # Move to the right
        vacuum_location[0], vacuum_location[1] = row, col + 1

        board[vacuum_location[0]][vacuum_location[1]] = 1
        actions.append("move")
        return row, col + 1
    else:
        vacuum_location[0], vacuum_location[1] = current_position

        board[vacuum_location[0]][vacuum_location[1]] = 1
        return current_position  # If already at the rightmost position, do nothing and return the same position


FUNCTION_LIST = [move_up, move_down, move_right, move_left]

vacuum_location = [0, 0]
board[vacuum_location[0]][vacuum_location[1]] = 1

tmp = 0
print_performance_var = 0

walk_instruction = zig_zag_walk()

performances = 0
repetition_number = 100

for i in range(repetition_number):
    running = True
    tmp = 0
    vacuum_location = [0, 0]
    board[vacuum_location[0]][vacuum_location[1]] = 1
    has_black_circles = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    print_performance_var = 0
    actions = []
    # print(i)

    print(has_black_circles)
    for j in range(10):
        action = simple_reflex_agent(has_black_circles, vacuum_location)

        if action == "clean":
            actions.append("clean")
            has_black_circles[vacuum_location[0]][vacuum_location[1]] = 0
            # j -= 1
        else:
            if tmp != n * n - 1:
                if walk_instruction[tmp] == 'right':
                    move_right(board, (vacuum_location[0], vacuum_location[1]))
                elif walk_instruction[tmp] == 'down':
                    move_down(board, (vacuum_location[0], vacuum_location[1]))
                elif walk_instruction[tmp] == 'left':
                    move_left(board, (vacuum_location[0], vacuum_location[1]))
                tmp += 1

        if tmp == n * n - 1 and action == "clean":
            break

    print(f"performance = {performance_measure(actions, 2, 3)}")
    performances += performance_measure(actions, 2, 3)
    print_performance_var += 1
    print(actions)

    print("-------")

print(f"avg performance: {performances / repetition_number}")
