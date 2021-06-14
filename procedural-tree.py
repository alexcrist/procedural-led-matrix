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

def generate_starter_tree():
    return [{
        'x': 0,
        'y': 16,
        'children': [{
            'x': 4,
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

def get_next_state(tree, dots):
    return tree, dots

# Drawing data to LED matrix ===================================================

def draw_tree(canvas, tree=[]):
    print(tree)
    for node in tree:
        start_x = node["x"]
        start_y = node["y"]
        for child in node.get("children", []):
            graphics.DrawLine(
                canvas, start_x, start_y, child["x"], child["y"], TREE_COLOR
            )
        draw_tree(canvas, node.get("children", []))


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




