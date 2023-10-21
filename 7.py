import time
import pygame
import sys
import random

# Initialize Pygame
pygame.init()

n = 6  # Change n to adjust the grid size

# Constants
WIDTH, HEIGHT = n * 100, n * 100
WHITE = (255, 255, 255)  # RGB color for WHITE
BLACK = (0, 0, 0)  # RGB color for black

# Square grid parameters
square_size = WIDTH // n
border_width = 2

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("WHITE Squares with Vacuum Images")

# Initialize has_black_circles array to track black circles
board = [[0 for _ in range(n)] for _ in range(n)]

has_black_circles = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
has_black_circles[n - 1][n - 1] = 0
has_black_circles[0][0] = 0

# print(has_black_circles)

# random_block_pos = [random.randrange(0, n), random.randrange(0, n)]
block_number = 0
random_block_possibility = [
    [[0, 1], [0, 3], [2, 2], [3, 2]],
    [[0, 1], [0, 3], [3, 2]],
    [[0, 1], [0, 3], [1, 1], [3, 2]],
    [[0, 1], [1, 3], [1, 1], [3, 2]],
    [[0, 1], [1, 1], [3, 2]],
    [[0, 1], [1, 4], [1, 1], [3, 2]],
    [[0, 1], [1, 4], [3, 1], [3, 3]],
    [[0, 1], [1, 4], [3, 1], [3, 4]],
    [[0, 1], [1, 4], [3, 1], [4, 4]],
    [[0, 1], [1, 4], [3, 1], [4, 1]],
    [[0, 1], [1, 4], [3, 1]],
    [[0, 1], [1, 1], [2, 1], [3, 1]],
    [[0, 1], [1, 1], [3, 1]],
    [[2, 2], [2, 3], [3, 2], [3, 3]]
]
random_block_pos = random.choice(random_block_possibility)

move_options = ["up", "down", "left", "right"]
# random_block_pos = [[0, 1], [0, 3], [2, 2], [3, 2]]  # block positions
block_map = [[0 for _ in range(n)] for _ in range(n)]

for i in random_block_pos:
    has_black_circles[i[0]][i[1]] = 0
    block_map[i[0]][i[1]] = 1
    block_number += 1

# print(f"block map: {block_map}")

actions = []
next_action = "nothing"

predicted_map = [[False for _ in range(n)] for _ in range(n)]
predicted_map[0][0] = True
predicted_map[n - 1][n - 1] = True
# print(predicted_map)


def four_way_block(row, col):
    # block_map
    # predicted_map
    # if row + 1 < n < col + 1 and row - 1 >= 0 and col - 1 > 0:

    if row == n - 1 and 0 < col < n - 1:
        if (predicted_map[row - 1][col] or block_map[row - 1][col] == 1 or row - 1 < 0) \
                and (predicted_map[row][col + 1] or block_map[row][col + 1] == 1 or col + 1 == n) \
                and (predicted_map[row][col - 1] or block_map[row][col - 1] == 1 or col - 1 < 0):
            return True

    elif row == 0 and 0 < col < n - 1:
        if (predicted_map[row + 1][col] or block_map[row - 1][col] == 1 or row - 1 < 0) \
                and (predicted_map[row][col + 1] or block_map[row][col + 1] == 1 or col + 1 == n) \
                and (predicted_map[row][col - 1] or block_map[row][col - 1] == 1 or col - 1 < 0):
            return True

    elif col == 0 and 0 < row < n - 1:
        if (predicted_map[row + 1][col] or block_map[row + 1][col] == 1 or row + 1 == n) \
                and (predicted_map[row - 1][col] or block_map[row - 1][col] == 1 or row - 1 < 0) \
                and (predicted_map[row][col + 1] or block_map[row][col + 1] == 1 or col + 1 == n):
            return True

    elif col == n - 1 and 0 < row < n - 1:
        if (predicted_map[row + 1][col] or block_map[row + 1][col] == 1 or row + 1 == n) \
                and (predicted_map[row - 1][col] or block_map[row - 1][col] == 1 or row - 1 < 0) \
                and (predicted_map[row][col - 1] or block_map[row][col - 1] == 1 or col + 1 == n):
            return True

    elif col == 0 and row == 0:
        if (predicted_map[row + 1][col] or block_map[row + 1][col] == 1 or row + 1 == n) \
                and (predicted_map[row][col + 1] or block_map[row][col + 1] == 1 or col + 1 == n):
            return True

    elif col == n - 1 and row == n - 1:
        if (predicted_map[row - 1][col] or block_map[row - 1][col] == 1 or row - 1 < 0) \
                and (predicted_map[row][col - 1] or block_map[row][col - 1] == 1 or col - 1 < 0):
            return True

    elif row == n - 1 and col == 0:
        if (predicted_map[row - 1][col] or block_map[row - 1][col] == 1 or row - 1 < 0) \
                and (predicted_map[row][col + 1] or block_map[row][col + 1] == 1 or col + 1 == n):
            return True

    elif row == 0 and col == n - 1:
        if (predicted_map[row + 1][col] or block_map[row + 1][col] == 1 or row - 1 < 0) \
                and (predicted_map[row][col - 1] or block_map[row][col - 1] == 1 or col + 1 == n):
            return True

    elif (predicted_map[row + 1][col] or block_map[row + 1][col] == 1 or row + 1 == n) \
            and (predicted_map[row - 1][col] or block_map[row - 1][col] == 1 or row - 1 < 0) \
            and (predicted_map[row][col + 1] or block_map[row][col + 1] == 1 or col + 1 == n) \
            and (predicted_map[row][col - 1] or block_map[row][col - 1] == 1 or col - 1 < 0):
        return True
    # else:
    #     walk_instruction.append(random.choice(move_options))
    return False


def all_rooms_are_clean():
    for row in has_black_circles:
        for element in row:
            if element != 0:
                return False
    return True


def simple_reflex_agent(has_black_circles, vacuum_location):
    for i in random_block_pos:
        if i == vacuum_location:
            return "block"
    if 0 <= vacuum_location[0] < n or 0 <= vacuum_location[1] < n:
        try:
            if has_black_circles[vacuum_location[0]][vacuum_location[1]] == 1:  # If the room is dirty, clean it
                return "clean"
            else:
                return "move"
        except IndexError:
            pass
            # print(f"vacuum_location: {vacuum_location}")
            # print(f"has_black_circles: {has_black_circles[vacuum_location[0]][vacuum_location[1]]}")
    else:
        return "move"


# Define the performance measure
def performance_measure(actions, a, b):
    num_moves = actions.count("move")
    num_cleans = actions.count("clean")
    return num_moves + (a * num_cleans) + (b * num_moves)


def show_vacuum():
    vacuum_image = pygame.image.load('Assets/vacuum-cleaner.png')
    vacuum_image = pygame.transform.scale(vacuum_image, (square_size // 2, square_size // 2))
    screen.blit(vacuum_image, (x + square_size // 4, y + square_size // 7))


def move_up(array, current_position):
    row, col = current_position
    next_action = simple_reflex_agent(has_black_circles, [row - 1, col])
    if row > 0 and next_action != "block":
        # print(f"foru way : {four_way_block(row, col)}")
        if predicted_map[row - 1][col] and four_way_block(row, col) == False:
            walk_instruction.pop()
            walk_instruction.append(random.choice(move_options))
            vacuum_location[0], vacuum_location[1] = current_position
            return next_action, [row - 1, col]  # If already at the rightmost position, do nothing and return the same
        else:
            array[row][col] = 0  # Clear the current position
            array[row - 1][col] = 1  # Move up
            vacuum_location[0], vacuum_location[1] = row - 1, col

            board[vacuum_location[0]][vacuum_location[1]] = 1
            actions.append("move")
            return next_action, [row - 1, col]
    else:
        vacuum_location[0], vacuum_location[1] = current_position
        return next_action, [row - 1, col]  # If already at the top row, do nothing and return the same position


def move_down(array, current_position):
    row, col = current_position
    next_action = simple_reflex_agent(has_black_circles, [row + 1, col])
    if row < n - 1 and next_action != "block":
        # print(f"foru way : {four_way_block(row, col)}")
        if predicted_map[row + 1][col] and four_way_block(row, col) == False:
            walk_instruction.pop()
            walk_instruction.append(random.choice(move_options))
            vacuum_location[0], vacuum_location[1] = current_position
            return next_action, [row + 1, col]  # If already at the rightmost position, do nothing and return the same
        else:
            array[row][col] = 0  # Clear the current position
            array[row + 1][col] = 1  # Move down
            vacuum_location[0], vacuum_location[1] = row + 1, col

            board[vacuum_location[0]][vacuum_location[1]] = 1
            actions.append("move")
            return next_action, [row + 1, col]
    else:
        vacuum_location[0], vacuum_location[1] = current_position
        return next_action, [row + 1, col]  # If already at the bottom row, do nothing and return the same position


def move_left(array, current_position):
    row, col = current_position
    next_action = simple_reflex_agent(has_black_circles, [row, col - 1])
    if col > 0 and next_action != "block":
        # print(f"foru way : {four_way_block(row, col)}")
        if predicted_map[row][col - 1] and four_way_block(row, col) == False:
            walk_instruction.pop()
            walk_instruction.append(random.choice(move_options))
            vacuum_location[0], vacuum_location[1] = current_position
            return next_action, [row, col - 1]  # If already at the rightmost position, do nothing and return the same
        else:
            array[row][col] = 0  # Clear the current position
            array[row][col - 1] = 1  # Move to the left
            vacuum_location[0], vacuum_location[1] = row, col - 1

            board[vacuum_location[0]][vacuum_location[1]] = 1
            actions.append("move")
            return next_action, [row, col - 1]
    else:
        vacuum_location[0], vacuum_location[1] = current_position
        return next_action, [row, col - 1]  # If already at the leftmost position, do nothing and return the same
        # position


def move_right(array, current_position):
    row, col = current_position
    next_action = simple_reflex_agent(has_black_circles, [row, col + 1])

    if col < n - 1 and next_action != "block":
        # print(f"foru way : {four_way_block(row, col)}")
        if predicted_map[row][col + 1] and four_way_block(row, col) == False:
            walk_instruction.pop()
            walk_instruction.append(random.choice(move_options))
            vacuum_location[0], vacuum_location[1] = current_position
            return next_action, [row, col + 1]  # If already at the rightmost position, do nothing and return the same
        else:
            array[row][col] = 0  # Clear the current position
            array[row][col + 1] = 1  # Move to the right
            vacuum_location[0], vacuum_location[1] = row, col + 1

            board[vacuum_location[0]][vacuum_location[1]] = 1
            actions.append("move")
            return next_action, [row, col + 1]
    else:
        vacuum_location[0], vacuum_location[1] = current_position
        return next_action, [row, col + 1]  # If already at the rightmost position, do nothing and return the same
        # position


# Function to draw a square with a vacuum image
def draw_square_with_vacuum(vacuum_location, x, y, has_black_circle, block_map, row, column):
    pygame.draw.rect(screen, BLACK, (x, y, square_size, square_size), border_width)
    pygame.draw.rect(screen, WHITE, (
        x + border_width, y + border_width, square_size - 2 * border_width, square_size - 2 * border_width))

    if block_map:
        block_image = pygame.image.load('Assets/block.png')
        block_image = pygame.transform.scale(block_image, (square_size, square_size))

        screen.blit(block_image, (x, y))

    if has_black_circle:
        stain_image = pygame.image.load('Assets/stain.png')
        stain_image = pygame.transform.scale(stain_image, (square_size // 3, square_size // 3))

        screen.blit(stain_image, (x + square_size // 3, y + square_size // 1.5))

        if vacuum_location == [column, row]:
            show_vacuum()
    else:
        if vacuum_location == [column, row]:
            show_vacuum()


# Main loop
running = True

vacuum_location = [0, 0]
board[vacuum_location[0]][vacuum_location[1]] = 1

tmp = 0
print_performance_var = 0

# walk_instruction = forward
walk_instruction = []

repetition_number = 0
performances = 0

row_col = []

FUNCTION_LIST = [
    move_right(board, (vacuum_location[0], vacuum_location[1])),
    move_down(board, (vacuum_location[0], vacuum_location[1])),
    move_right(board, (vacuum_location[0], vacuum_location[1])),
    move_left(board, (vacuum_location[0], vacuum_location[1]))
]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a white background
    screen.fill((255, 255, 255))

    # Draw the grid of WHITE squares with vacuum images and update the has_black_circles array
    for i in range(n):
        for j in range(n):
            x = i * square_size
            y = j * square_size
            has_black_circle = has_black_circles[j][i]
            block = block_map[j][i]
            draw_square_with_vacuum(vacuum_location, x, y, has_black_circle, block, i, j)

    pygame.display.flip()

    action = simple_reflex_agent(has_black_circles, vacuum_location)

    # print(vacuum_location)
    # print(action)
    # print(tmp)

    if action == "clean":
        actions.append("clean")
        # if random.random() <= 0.75:  # 25% of time it doesn't clean
        has_black_circles[vacuum_location[0]][vacuum_location[1]] = 0

    else:
        if not all_rooms_are_clean():

            walk_instruction.append(random.choice(move_options))

            predicted_map[vacuum_location[0]][vacuum_location[1]] = True

            # walk_instruction.append("down")
            # print(f"walk_ins: {walk_instruction}")

            # print(f"len ins {len(walk_instruction)}")
            # print(f"tmp{tmp}")
            # print(f"vacuum_location: {vacuum_location}")

            # for z in predicted_map:
            #     for q in z:
            #         print(f"{q}", end=" ")
            #     print("\n")
            # print("----------")

            if walk_instruction[tmp] == 'right':
                next_action, row_col = move_right(board, (vacuum_location[0], vacuum_location[1]))
            elif walk_instruction[tmp] == 'down':
                next_action, row_col = move_down(board, (vacuum_location[0], vacuum_location[1]))
            elif walk_instruction[tmp] == 'up':
                next_action, row_col = move_up(board, (vacuum_location[0], vacuum_location[1]))
            elif walk_instruction[tmp] == 'left':
                next_action, row_col = move_left(board, (vacuum_location[0], vacuum_location[1]))

            if next_action == "block":
                next_action = "nothing"
                tmp += 1
            # print(next_action)
            else:
                tmp += 1

    predicted_map[vacuum_location[0]][vacuum_location[1]] = True

    if all_rooms_are_clean() == False:
        pass
        # print(f"tmp: {tmp} {action}")

    elif print_performance_var == 0 or all_rooms_are_clean() == False:
        # time.sleep(0.7)
        print(f"time {repetition_number}")
        performance = performance_measure(actions, 10, 5)
        print(f"performance = {performance}")
        print_performance_var += 1
        performances += performance
        print(actions)
        print("---------------")

        # print("DONE!")

        repetition_number += 1

        vacuum_location = [0, 0]
        tmp = 0
        print_performance_var = 0

        has_black_circles = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        has_black_circles[n - 1][n - 1] = 0
        has_black_circles[0][0] = 0

        walk_instruction = []
        random_block_pos = random.choice(random_block_possibility)
        for i in random_block_pos:
            has_black_circles[i[0]][i[1]] = 0
            block_map[i[0]][i[1]] = 1
            block_number += 1
        # walk_instruction = zig_zag_walk(n)
        # print(f"RESET ins: {walk_instruction}")
        block_map = [[0 for _ in range(n)] for _ in range(n)]
        for i in random_block_pos:
            block_map[i[0]][i[1]] = 1
            block_number += 1
        actions = []
        next_action = "nothing"

        if repetition_number == 100:
            print(f"avg performance: {performances / repetition_number}")
            # print(all_rooms_are_clean())
            # print(predicted_map)
            break

    # print(action)

    # you can adjust speed here (speed up the vacuum to see avg performance in 100 times)
    # time.sleep(0.5)

# Quit Pygame
pygame.quit()
sys.exit()
