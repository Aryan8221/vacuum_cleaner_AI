import time
import pygame
import sys
import random

# Initialize Pygame
pygame.init()

n = 3  # Change n to adjust the grid size

# Constants
WIDTH, HEIGHT = n * 50, n*50
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


def show_vacuum():
    vacuum_image = pygame.image.load('Assets/vacuum-cleaner.png')
    vacuum_image = pygame.transform.scale(vacuum_image, (square_size // 2, square_size // 2))
    screen.blit(vacuum_image, (x + square_size // 4, y + square_size // 7))


def move_up(array, current_position):
    row, col = current_position
    if row > 0:
        array[row][col] = 0  # Clear the current position
        array[row - 1][col] = 1  # Move up
        vacuum_location[0], vacuum_location[1] = row - 1, col

        board[vacuum_location[0]][vacuum_location[1]] = 1
        # actions.append("move")
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
        # actions.append("move")
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
        # actions.append("move")
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
        # actions.append("move")
        return row, col + 1
    else:
        vacuum_location[0], vacuum_location[1] = current_position

        board[vacuum_location[0]][vacuum_location[1]] = 1
        return current_position  # If already at the rightmost position, do nothing and return the same position


FUNCTION_LIST = [move_up, move_down, move_right, move_left]


# Function to draw a square with a vacuum image
def draw_square_with_vacuum(vacuum_location, x, y, has_black_circle, row, column):
    pygame.draw.rect(screen, BLACK, (x, y, square_size, square_size), border_width)
    pygame.draw.rect(screen, WHITE, (
        x + border_width, y + border_width, square_size - 2 * border_width, square_size - 2 * border_width))

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

walk_instruction = zig_zag_walk()

repetition_number = 0

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
            draw_square_with_vacuum(vacuum_location, x, y, has_black_circle, i, j)

    pygame.display.flip()

    action = simple_reflex_agent(has_black_circles, vacuum_location)
    if action == "clean":
        actions.append("clean")
        has_black_circles[vacuum_location[0]][vacuum_location[1]] = 0
    else:
        # spiral_walk(board)
        # if vacuum is in the edges the list must be restricted ------------------------------------------

        # random.choice(FUNCTION_LIST)(board, (vacuum_location[0], vacuum_location[1]))
        # print(vacuum_location[0], vacuum_location[1])
        actions.append("move")
        if tmp != n * n - 1:
            if walk_instruction[tmp] == 'right':
                move_right(board, (vacuum_location[0], vacuum_location[1]))
            elif walk_instruction[tmp] == 'down':
                move_down(board, (vacuum_location[0], vacuum_location[1]))
            elif walk_instruction[tmp] == 'left':
                move_left(board, (vacuum_location[0], vacuum_location[1]))
            tmp += 1

    if tmp != n * n - 1 or (tmp == n * n - 1 and action != "move"):
        print(f"tmp: {tmp} {action}")

    elif print_performance_var == 0:
        # time.sleep(0.7)
        print(f"performance = {performance_measure(actions, 10, 5)}")
        print_performance_var += 1
        print(actions)

        print("DONE!")
        # break

    # print(action)
    time.sleep(0.4)


# Quit Pygame
pygame.quit()
sys.exit()


