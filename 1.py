import time
import pygame
import sys
import random

# Initialize Pygame
pygame.init()

n = 2  # Change n to adjust the grid size

# Constants
WIDTH, HEIGHT = n * 100, 1 * 100
WHITE = (255, 255, 255)  # RGB color for WHITE
BLACK = (0, 0, 0)  # RGB color for black

# Square grid parameters
square_size = WIDTH // n
border_width = 2

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("WHITE Squares with Vacuum Images")

# Initialize has_black_circles array to track black circles
board = [[0 for _ in range(2)] for _ in range(1)]

has_black_circles = [[random.choice([0, 1]) for _ in range(2)] for _ in range(1)]
# has_black_circles[n - 1][n - 1] = 0
# has_black_circles[0][0] = 0

print(has_black_circles)

actions = []


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


# Function to draw a square with a vacuum image
def draw_square_with_vacuum(vacuum_location, x, y, has_black_circle, row, column):
    pygame.draw.rect(screen, BLACK, (x, y, square_size, square_size), border_width)
    pygame.draw.rect(screen, WHITE, (
        x + border_width, y + border_width, square_size, square_size - 2 * border_width))

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

repetition_number = 0
performances = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a white background
    screen.fill((255, 255, 255))

    # Draw the grid of WHITE squares with vacuum images and update the has_black_circles array
    for i in range(n):
        for j in range(1):
            x = i * square_size
            y = j * square_size
            has_black_circle = has_black_circles[j][i]
            draw_square_with_vacuum(vacuum_location, x, y, has_black_circle, i, j)

    pygame.display.flip()

    action = simple_reflex_agent(has_black_circles, vacuum_location)
    # print(action)

    if action == "clean":
        actions.append("clean")
        has_black_circles[vacuum_location[0]][vacuum_location[1]] = 0

    else:
        if tmp != n * n - 1:

            move_right(board, (vacuum_location[0], vacuum_location[1]))

            tmp += 1

    if tmp != n * n - 1 or (tmp == n * n - 1 and action != "move"):
        pass
        # print(f"tmp: {tmp} {action}")

    elif print_performance_var == 0:

        print(f"time {repetition_number}")
        # print(if_all_rooms_are_clean())
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

        actions = []

        if (repetition_number == 100):
            print(f"avg performance: {performances / repetition_number}")
            break
        else:
            tmp = 0
            print_performance_var = 0

    # print(action)

    # you can adjust speed here (speed up the vacuum to see avg performance in 100 times)
    time.sleep(0.5)

# Quit Pygame
pygame.quit()
sys.exit()
