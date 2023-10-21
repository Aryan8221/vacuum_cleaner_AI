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
]
random_block_pos = random.choice(random_block_possibility)

# random_block_pos = [[0, 1], [0, 3], [2, 2], [3, 2]]  # block positions
block_map = [[0 for _ in range(n)] for _ in range(n)]
for i in random_block_pos:
    block_map[i[0]][i[1]] = 1
    block_number += 1

# print(f"block map: {block_map}")

actions = []
next_action = "nothing"

def zig_zag_walk(n):
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

    # print(walk_instruction)
    #
    return walk_instruction


forward = zig_zag_walk(n)


def simple_reflex_agent(has_black_circles, vacuum_location):
    for i in random_block_pos:
        if i == vacuum_location:
            return "block"
    if has_black_circles[vacuum_location[0]][vacuum_location[1]] == 1:  # If the room is dirty, clean it
        return "clean"
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
    if row > 0:
        array[row][col] = 0  # Clear the current position
        array[row - 1][col] = 1  # Move up
        vacuum_location[0], vacuum_location[1] = row - 1, col

        board[vacuum_location[0]][vacuum_location[1]] = 1
        actions.append("move")
        return row - 1, col
    else:
        vacuum_location[0], vacuum_location[1] = current_position
        return next_action, [row, col + 1]  # If already at the top row, do nothing and return the same position


def move_down(array, current_position):
    row, col = current_position
    next_action = simple_reflex_agent(has_black_circles, [row + 1, col])
    if row < n - 1:
        array[row][col] = 0  # Clear the current position
        array[row + 1][col] = 1  # Move down
        vacuum_location[0], vacuum_location[1] = row + 1, col

        board[vacuum_location[0]][vacuum_location[1]] = 1
        actions.append("move")
        return row + 1, col
    else:
        vacuum_location[0], vacuum_location[1] = current_position
        return next_action, [row + 1, col]  # If already at the bottom row, do nothing and return the same position


def move_left(array, current_position):
    row, col = current_position
    next_action = simple_reflex_agent(has_black_circles, [row, col - 1])
    if col > 0 and next_action != "block":
        array[row][col] = 0  # Clear the current position
        array[row][col - 1] = 1  # Move to the left
        vacuum_location[0], vacuum_location[1] = row, col - 1

        board[vacuum_location[0]][vacuum_location[1]] = 1
        actions.append("move")
        return row, col - 1
    else:
        vacuum_location[0], vacuum_location[1] = current_position
        return next_action, [row, col - 1]  # If already at the leftmost position, do nothing and return the same position


def move_right(array, current_position):
    row, col = current_position
    next_action = simple_reflex_agent(has_black_circles, [row, col + 1])
    if col < n - 1 and next_action != "block":
        array[row][col] = 0  # Clear the current position
        array[row][col + 1] = 1  # Move to the right
        vacuum_location[0], vacuum_location[1] = row, col + 1

        board[vacuum_location[0]][vacuum_location[1]] = 1
        actions.append("move")
        return row, col + 1
    else:
        vacuum_location[0], vacuum_location[1] = current_position

        board[vacuum_location[0]][vacuum_location[1]] = 1
        return next_action, [row, col + 1]  # If already at the rightmost position, do nothing and return the same position


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

walk_instruction = forward

repetition_number = 0
performances = 0

row_col = []

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

    # print(action)
    # print(tmp)

    if action == "clean":
        actions.append("clean")
        # if random.random() <= 0.75:  # 25% of time it doesn't clean
        has_black_circles[vacuum_location[0]][vacuum_location[1]] = 0

    else:
        if tmp != len(walk_instruction):
            if walk_instruction[tmp] == 'right':
                next_action, row_col = move_right(board, (vacuum_location[0], vacuum_location[1]))
            elif walk_instruction[tmp] == 'down':
                next_action, row_col = move_down(board, (vacuum_location[0], vacuum_location[1]))
            elif walk_instruction[tmp] == 'up':
                next_action, row_col = move_up(board, (vacuum_location[0], vacuum_location[1]))
            elif walk_instruction[tmp] == 'left':
                next_action, row_col = move_left(board, (vacuum_location[0], vacuum_location[1]))

            if next_action == "block":
                # vacuum_location = [0, 0]
                # print("block")
                if 0 < row_col[0] < n - 1 and 0 < row_col[1] < n - 1:
                    insert_list_right = ["down", "right", "right", "up"]
                    insert_list_left = ["down", "left", "left", "up"]
                    if walk_instruction[tmp] == "right":
                        walk_instruction.pop(tmp)
                        walk_instruction.pop(tmp)
                        for i in range(len(insert_list_right)):
                            walk_instruction.insert(i + tmp, insert_list_right[i])
                        pass
                    else:
                        walk_instruction.pop(tmp)
                        walk_instruction.pop(tmp)
                        for i in range(len(insert_list_left)):
                            walk_instruction.insert(i + tmp, insert_list_left[i])
                        pass
                    # print(walk_instruction)
                    # print(f"number of ins: {len(walk_instruction)}")
                elif 0 == row_col[0] and 0 < row_col[1] < n - 1:
                    insert_list = ["down", "right", "right", "up"]

                    # walk_instruction.pop()
                    walk_instruction.pop(tmp)
                    walk_instruction.pop(tmp)
                    for i in range(len(insert_list)):
                        walk_instruction.insert(i + tmp, insert_list[i])
                next_action = "nothing"
            # print(next_action)
            else:
                tmp += 1

    if tmp != len(walk_instruction) or (tmp != len(walk_instruction) and action != "move"):
        pass
        # print(f"tmp: {tmp} {action}")

    elif print_performance_var == 0:
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
        random_block_pos = random.choice(random_block_possibility)
        walk_instruction = zig_zag_walk(n)
        # print(f"RESET ins: {walk_instruction}")
        block_map = [[0 for _ in range(n)] for _ in range(n)]
        for i in random_block_pos:
            block_map[i[0]][i[1]] = 1
            block_number += 1
        actions = []
        next_action = "nothing"

        if repetition_number == 100:
            print(f"avg performance: {performances / repetition_number}")
            break

    # print(action)

    # you can adjust speed here (speed up the vacuum to see avg performance in 100 times)
    # time.sleep(0.05)

# Quit Pygame
pygame.quit()
sys.exit()
