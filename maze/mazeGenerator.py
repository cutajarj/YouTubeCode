import random
import time
from turtle import *

width = 7
height = 7
border = 8
scale = 35

move_x = {'N': 0, 'S': 0, 'W': -1, 'E': 1}
move_y = {'N': -1, 'S': 1, 'W': 0, 'E': 0}
direction_deg = {'N': 0, 'S': 180, 'W': 270, 'E': 90}

def carve_passages_from(x, y, is_free):
    is_free[y][x] = False
    directions = ['N', 'S', 'E', 'W']
    random.shuffle(directions)
    for direction in directions:
        nx = x + move_x[direction]
        ny = y + move_y[direction]
        if 0 <= nx < width and 0 <= ny < height and is_free[ny][nx]:
            setheading(direction_deg[direction])
            forward(scale)
            carve_passages_from(nx, ny, is_free)
            setheading(direction_deg[direction])
            backward(scale)


if __name__ == '__main__':
    setup(width=width * scale + border * 5, height=height * scale + border * 5, startx=700, starty=120)
    mode('logo')
    bgcolor("black")
    speed(4)
    color('red')
    pencolor('white')
    shapesize(2)
    up()
    goto(-width * scale / 2 + border, height * scale / 2 - border)
    down()
    pensize(scale - border)
    is_free_grid = [[True for i in range(width)] for j in range(height)]
    carve_passages_from(0, 0, is_free_grid)
    mainloop()
