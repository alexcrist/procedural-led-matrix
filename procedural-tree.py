#!/usr/bin/env python
import math
import numpy as np
import random

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from rgbmatrix import graphics

# LED matrix config ============================================================

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'

# Create the RGBMatrix
matrix = RGBMatrix(options = options)

# Create a canvas to draw on
canvas = matrix.CreateFrameCanvas()

TREE_COLOR = graphics.Color(162, 42, 42)

# Data structures ==============================================================

# Tree structure
# [
#     {
#         x: 0,
#         y: 0,
#         children: [
#             {
#                 x: 1,
#                 y: 1
#             }
#         ]
#     }
# ]

# Random target stucture
# 32 x 64 matrix
# [
#     [0, 0, 1, ..., 1],
#     [0, 0, 1, ..., 1],
#     ...
#     [0, 0, 1, ..., 1]
# ]

# Initializers =================================================================

BRANCH_LENGTH = 3

def generate_starter_tree():
    return [{
        'x': 0,
        'y': 16,
        'children': [{
            'x': BRANCH_LENGTH,
            'y': 16
        }]
    }]

def generate_random_dots(n_dots, left=0, right=63, top=0, bottom=31):
    dots = np.zeros((right - left + 1, bottom - left + 1))
    for _ in range(n_dots):
        x = random.randint(left, right)
        y = random.randint(top, bottom)
        dots[x][y] = 1
    return dots

# Procedural updating ==========================================================

def find_nearby_points(x, y, radius = 12.0) -> List[Tuple[int, int]]:
    """ create a small collection of points in a neighborhood of some point 
    """
    neighborhood = []

    X = int(radius)
    for i in range(-X, X + 1):
        Y = int(pow(radius * radius - i * i, 1/2))
        for j in range(-Y, Y + 1):
            neighborhood.append((x + i, y + j))

    return neighborhood

def get_next_branch(parent, child, dots):
    min_radius = 2
    max_radius = 12

    dots = np.array(dots)

    nearby_dots = False
    for (x, y) in find_nearby_points(child["x"], child["y"], min_radius):
        if dots[x][y]:
            nearby_dots = True
            dots[x][y] = 0

    if nearby_dots:
        # TODO: branch
        return child, dots

    found_dots = []
    for (x, y) in find_nearby_points(child["x"], child["y"], max_radius):
        if dots[x][y]:
            found_dots.append((x,y))

    if len(found_dots) == 0:
        return child, dots
    
    # todo - what happens, if the vector is zero? hmm?
    x, y = zip(*found_dots)
    x_avg = sum(x) / len(x)
    y_avg = sum(y) / len(y)

    x_avg -= child['x']
    y_avg -= child['y']
    
    norm = np.linalg.norm((x_avg, y_avg))

    x = x_avg / norm * BRANCH_LENGTH
    y = y_avg / norm * BRANCH_LENGTH

    x += child['x']
    y += child['y']

    child['children'] = {
        'x': x,
        'y': y
    }

    return child, dots

def get_next_state(tree, dots):
    '''
        1. if no dots are near a branch-end, just grow straight
        2. if dots are < GROW_RADIUS from branch-end, grow towards nearby dots
        3. if dots are < BRANCH_RADIUS from branch-end, delete dots and branch 
    '''

    if 'children' not in tree:
        raise Exception('You goofed')

    dots = np.array(dots)

    for i, child in enumerate(tree['children']):

        if 'children' in child:
            tree['children'][i], child_dots = get_next_state(tree['children'], dots)
            dots *= child_dots

        else:
            tree['children'][i], child_dots = get_next_branch(tree, child, dots)
            dots *= child_dots

    return tree, dots

# Drawing data to LED matrix ===================================================

def draw_tree(canvas, tree=[]):
    print(tree)
    for node in tree:
        start_x = node["x"]
        start_y = node["y"]
        children = node.get("children", [])
        for child in children:
            graphics.DrawLine(
                canvas, 
                round(start_x), 
                round(start_y), 
                round(child["x"]), 
                round(child["y"]), 
                TREE_COLOR
            )
        if children:
            draw_tree(canvas, children)

def draw_dots(canvas, dots):
    for col in range(options.cols):
        for row in range(options.rows):
            if dots[col][row]:
                canvas.SetPixel(col, row, 0, 255, 0)

def draw(canvas, tree, dots):

    draw_tree(canvas, tree)
    draw_dots(canvas, dots)

    canvas = matrix.SwapOnVSync(canvas)
    canvas.Clear()

    return canvas

# Entrypoint ===================================================================

canvas = matrix.CreateFrameCanvas()

tree = generate_starter_tree()
dots = generate_random_dots(100)

while True:

    canvas = draw(canvas, tree, dots)

    tree, dots = get_next_state(tree, dots)




