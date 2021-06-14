#!/usr/bin/env python
import math
import numpy as np
import random

from rgbmatrix import RGBMatrix, RGBMatrixOptions

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

def get_next_tree(last_tree):
    '''
        Takes a a previous tree state and generates the next
        tree state
    '''
    pass

def generate_random_dots(n_dots, left=0, right=63, top=0, bottom=31):
    dots = np.zeros((right - left, bottom - left))
    for _ in range(n_dots):
        x = random.randint(left, right)
        y = random.randint(top, bottom)
        dots[x][y] = 1
    return dots

def draw_tree():
    pass

def draw_dots(dots):
    for col in range(options.cols):
        for row in range(options.rows):
            canvas.SetPixel(col, row, (0, 255, 0))

def draw(canvas):
    tree = get_next_tree()
    dots = generate_random_dots(100)

    draw_tree(canvas, tree)
    draw_dots(canvas, dots)
    
    canvas = matrix.SwapOnVSync(canvas)
    canvas.Clear()

    return canvas

# Entrypoint
while True:
    canvas = matrix.CreateFrameCanvas()
    canvas = draw()  
