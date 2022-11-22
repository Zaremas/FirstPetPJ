from tkinter import messagebox, Tk
from turtledemo import clock

import pygame
import sys

window_width = 800
window_height = 800

window = pygame.display.set_mode((window_width, window_height))

columns = 50
rows = 50

box_width = window_width // columns
box_height = window_height // rows

grid = []
queue = []
path = []


class Box:
    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.start = False
        self.wall = False
        self.target = False
        self.queued = False
        self.visited = False
        self.neighbours = []
        self.prior = None

    def draw(self, win, color):
        pygame.draw.rect(win, color, (self.x * box_width, self.y * box_height, box_width-2, box_height-2))

    def set_neighbours(self):
        if self.x > 0:
            self.neighbours.append(grid[self.x - 1][self.y])
        if self.x < columns - 1:
            self.neighbours.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.neighbours.append(grid[self.x][self.y - 1])
        if self.y < rows - 1:
            self.neighbours.append(grid[self.x][self.y + 1])


# Create Grid
for i in range(columns):
    arr = []
    for j in range(rows):
        arr.append(Box(i, j))
    grid.append(arr)

# Set Neighbours
for i in range(columns):
    for j in range(rows):
        grid[i][j].set_neighbours()

def main():
    begin_search = False
    target_box_set = False
    start_box_set = False
    searching = True
    target_box = None

    while True:

        for event in pygame.event.get():
            # Quit Window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Mouse Controls
            elif event.type == pygame.MOUSEMOTION and searching:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                i = x // box_width
                j = y // box_height
                # Draw Wall
                if event.buttons[0]:
                    grid[i][j].wall = True
                # Set Target

            elif event.type == pygame.MOUSEBUTTONDOWN and searching:
                i = pygame.mouse.get_pos()[0] // box_width
                j = pygame.mouse.get_pos()[1] // box_height

                if event.button == 1 and not start_box_set:

                    start_box = grid[i][j]
                    start_box.start = True
                    start_box.visited = True
                    start_box_set = True
                    queue.append(start_box)
                    
                if event.button == 1 and start_box_set:
                    start_box.start = False
                    start_box.visited = False
                    start_box = grid[i][j]
                    start_box.start = True
                    start_box.visited = True
                    queue.clear()
                    queue.append(start_box)

                if event.button==3 and not target_box_set:
                    target_box = grid[i][j]
                    target_box.target = True
                    target_box_set = True

                if event.button==3 and target_box_set:
                    target_box.target = False
                    target_box = grid[i][j]
                    target_box.target = True
            # Start Algorithm
            if event.type == pygame.KEYDOWN and target_box_set and start_box_set:
                begin_search = True

        if begin_search:
            if len(queue) > 0 and searching:
                current_box = queue.pop(0)
                current_box.visited = True
                if current_box == target_box:
                    searching = False
                    while current_box.prior != start_box:
                        path.append(current_box.prior)
                        current_box = current_box.prior
                else:
                    for neighbour in current_box.neighbours:
                        if not neighbour.queued and not neighbour.wall:
                            neighbour.queued = True
                            neighbour.prior = current_box
                            queue.append(neighbour)
            else:
                if searching:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No Solution", "There is no solution!")
                    searching = False

        window.fill((0, 0, 0))

        for i in range(columns):
            for j in range(rows):
                box = grid[i][j]
                box.draw(window, (100, 100, 100))

                if box.queued:
                    box.draw(window, (219, 96, 90))
                if box.visited:
                    box.draw(window, (145, 217, 106))
                if box in path:
                    box.draw(window, (50, 56, 227))

                if box.start:
                    box.draw(window, (217, 37, 30))
                if box.wall:
                    box.draw(window, (10, 10, 10))
                if box.target:
                    box.draw(window, (200, 200, 0))

        pygame.display.flip()


main()
