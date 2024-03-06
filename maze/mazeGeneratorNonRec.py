import random
from collections import deque
from turtle import *

width = 140
height = 140
border = 2
scale = 6

move_x = {'N': 0, 'S': 0, 'W': -1, 'E': 1}
move_y = {'N': -1, 'S': 1, 'W': 0, 'E': 0}
direction_deg = {'N': 0, 'S': 180, 'W': 270, 'E': 90}


def push_all(directions, stack, x, y, is_free):
    random.shuffle(directions)
    for direction in directions:
        nx = x + move_x[direction]
        ny = y + move_y[direction]
        if 0 <= nx < width and 0 <= ny < height and is_free[ny][nx]:
            stack.append((x, y, direction))


def carve_passages_from(ix, iy, is_free):
    stack = deque()
    directions = ['N', 'S', 'E', 'W']
    is_free[iy][ix] = False
    push_all(directions, stack, ix, iy, is_free)
    while stack:
        (x, y, dir_to_go) = stack.pop()
        up()
        goto((-width / 2 + x) * scale + border, (height / 2 - y) * scale - border)
        down()
        nx = x + move_x[dir_to_go]
        ny = y + move_y[dir_to_go]
        if is_free[ny][nx]:
            is_free[ny][nx] = False
            push_all(directions, stack, nx, ny, is_free)
            setheading(direction_deg[dir_to_go])
            forward(scale)


if __name__ == '__main__':
    setup(width=width * scale + border * 5, height=height * scale + border * 5, startx=0, starty=0)
    mode('logo')
    bgcolor("black")
    speed(0)
    color('red')
    pencolor('white')
    shapesize(2)
    pensize(scale - border)
    is_free_grid = [[True for i in range(width)] for j in range(height)]
    carve_passages_from(0, 0, is_free_grid)
    mainloop()
