import random
import time
from tkinter import *

move_x = {'N': 0, 'S': 0, 'W': -1, 'E': 1}
move_y = {'N': -1, 'S': 1, 'W': 0, 'E': 0}
opposite = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
width = 40
height = 40
border = 3
scale = 20


def carve_passages_from(x, y, grid, canvas):
    draw_visit(x, y, canvas)
    # time.sleep(0.0001)
    directions = ['N', 'S', 'E', 'W']
    random.shuffle(directions)
    for direction in directions:
        nx = x + move_x[direction]
        ny = y + move_y[direction]
        if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] == '':
            grid[y][x] += direction
            grid[ny][nx] += opposite[direction]
            draw_passage(x, y, direction, canvas)
            carve_passages_from(nx, ny, grid, canvas)
            draw_current(x, y, canvas, 'red')
            # time.sleep(0.0001)
            draw_visit(x, y, canvas)


def draw_visit(x, y, canvas):
    canvas.create_rectangle(x * scale + border, y * scale + border, x * scale + scale - border,
                            y * scale + scale - border, fill='white')
    canvas.update()


def draw_current(x, y, canvas, colour):
    canvas.create_oval(x * scale + (border * 2), y * scale + (border * 2), x * scale + scale - (border * 2),
                            y * scale + scale - (border * 2), fill=colour)
    canvas.update()


def draw_passage(x, y, direction, canvas):
    match direction:
        case 'N':
            canvas.create_rectangle(x * scale + border, y * scale - border, x * scale + scale - border,
                                    y * scale + border, fill='white')
        case 'S':
            canvas.create_rectangle(x * scale + border, y * scale + scale - border, x * scale + scale - border,
                                    y * scale + scale + border, fill='white')
        case 'E':
            canvas.create_rectangle(x * scale + scale - border, y * scale + border, x * scale + scale + border,
                                    y * scale + scale - border, fill='white')
        case 'W':
            canvas.create_rectangle(x * scale - border, y * scale + border, x * scale + border,
                                    y * scale + scale - border, fill='white')
    canvas.update()


if __name__ == '__main__':
    root = Tk()
    canvas = Canvas(root, bg="black", height=height * scale, width=width * scale)
    canvas.pack()

    grid = [['' for i in range(width)] for j in range(height)]
    carve_passages_from(0, 0, grid, canvas)
    root.mainloop()
