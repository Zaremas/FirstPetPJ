from tkinter import messagebox, Tk

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
        self.coffee = False
        self.queued1 = False
        self.queued2 = False
        self.visited1 = False
        self.visited2 = False
        self.neighbours = []
        self.prior1 = None

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
    coffee_box_set = False
    coffee_box_found = False
    searching = True
    target_box = None
    coffee_box = None

    while True:

        for event in pygame.event.get():
            # Quit Window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Mouse Controls
            elif searching and event.type == pygame.MOUSEMOTION:

                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                i = x // box_width
                j = y // box_height
                # Draw Wall

                if event.buttons[0] and not grid[i][j].start and not grid[i][j].target and not grid[i][j].coffee:
                    i = x // box_width
                    j = y // box_height

                    grid[i][j].wall = True
                # Set Target


            elif searching and event.type == pygame.MOUSEBUTTONDOWN:
                keys = pygame.key.get_pressed()
                i = pygame.mouse.get_pos()[0] // box_width
                j = pygame.mouse.get_pos()[1] // box_height
                if keys[pygame.K_s] and not start_box_set:

                    start_box = grid[i][j]
                    start_box.start = True
                    start_box.visited1 = True
                    start_box_set = True
                    queue.append(start_box)


                if keys[pygame.K_s] and start_box_set:

                    start_box.start = False
                    start_box.visited1 = False
                    start_box = grid[i][j]
                    start_box.start = True
                    start_box.visited1 = True
                    queue.clear()
                    queue.append(start_box)


                if keys[pygame.K_f] and not target_box_set:

                    target_box = grid[i][j]
                    target_box.target = True
                    target_box_set = True


                if keys[pygame.K_f] and target_box_set:

                    target_box.target = False
                    target_box = grid[i][j]
                    target_box.target = True

                if keys[pygame.K_c] and not coffee_box_set:
                    coffee_box = grid[i][j]
                    coffee_box.coffee = True
                    coffee_box_set = True

                if keys[pygame.K_c] and target_box_set:
                    coffee_box.coffee = False
                    coffee_box = grid[i][j]
                    coffee_box.coffee = True

            # Start Algorithm

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and start_box_set and target_box_set:

                begin_search = True

        if begin_search and not coffee_box_set:
            if len(queue) > 0 and searching:
                current_box = queue.pop(0)
                current_box.visited1 = True
                if current_box == target_box:
                    searching = False
                    while current_box.prior1 != start_box:
                        path.append(current_box.prior1)
                        current_box = current_box.prior1
                else:
                    for neighbour in current_box.neighbours:
                        if not neighbour.queued1 and not neighbour.wall:
                            neighbour.queued1 = True
                            neighbour.prior1 = current_box
                            queue.append(neighbour)
            else:
                if searching:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No Solution", "There is no solution!")
                    searching = False

        if begin_search and coffee_box_set:
            if len(queue) > 0 and searching and not coffee_box_found:
                current_box = queue.pop(0)
                current_box.visited1 = True
                if current_box == coffee_box:
                    queue.clear()
                    while current_box.prior1 != start_box:
                        path.append(current_box.prior1)
                        current_box = current_box.prior1
                    for neighbour in coffee_box.neighbours:
                        if not neighbour.wall:
                            neighbour.queued2 = True
                            neighbour.prior2 = coffee_box
                            queue.append(neighbour)
                    coffee_box_found = True
                else:
                    for neighbour in current_box.neighbours:
                        if not neighbour.queued1 and not neighbour.wall:
                            neighbour.queued1 = True
                            neighbour.prior1 = current_box
                            queue.append(neighbour)


            if len(queue) > 0 and searching and coffee_box_found:
                current_box = queue.pop(0)
                current_box.visited2 = True
                if current_box == target_box:
                    searching = False
                    while current_box.prior2 != coffee_box:
                        path.append(current_box.prior2)
                        current_box = current_box.prior2
                else:
                    for neighbour in current_box.neighbours:
                        if not neighbour.queued2 and not neighbour.wall:
                            neighbour.queued2 = True
                            neighbour.prior2 = current_box
                            queue.append(neighbour)

            if len(queue) == 0 and searching:
                if searching:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No Solution", "There is no solution!")
                    searching = False

        window.fill((0, 0, 0))

        for i in range(columns):
            for j in range(rows):
                box = grid[i][j]
                box.draw(window, (100, 100, 100))


                if box.queued1 and not box.queued2:
                    box.draw(window, (129, 85, 212))
                if box.visited1 and not box.visited2:
                    box.draw(window, (187, 162, 232))
                if box.queued2:
                    box.draw(window, (120, 204, 112))
                if box.visited2:
                    box.draw(window, (177, 232, 172))
                if box in path:
                    box.draw(window, (255, 234, 0))

                if box.start:
                    box.draw(window, (240, 64, 55))

                if box.wall:
                    box.draw(window, (10, 10, 10))
                if box.target:
                    box.draw(window, (39, 58, 230))
                if box.coffee:
                    box.draw(window, (148, 68, 34))

        pygame.display.flip()


main()
