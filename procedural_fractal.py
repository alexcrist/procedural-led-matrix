#!/usr/bin/env python
import time
import sys
import math
import noise
import numpy as np

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

canvas = matrix.CreateFrameCanvas()
shape = (64, 32)
scale = 10

def intensity_to_color(intensity):
    intensity *= -1
    if intensity < 0.05:
        return (0, 0, 150)
    if intensity < 0.13:
        return (255, 255, 40)
    if intensity < 0.250:
        return (0, 255, 0)
    if intensity < 0.35:
        return (200, 100, 50)
    return (255, 255, 255)

def make_map():
    world = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            world[i][j] = noise.pnoise2(
                i/scale,
                j/scale,
                octaves=6,
                persistence=0.5,
                lacunarity=2.0,
                repeatx=shape[0],
                repeaty=shape[1],
                base=0,
            )
    return world

fractal_map = make_map()

flat_map = [v for row in fractal_map for v in row]

print('max', max(flat_map))
print('min', min(flat_map))
print('hist', np.histogram(flat_map))

while True:

    cols, rows = shape

    for col in range(cols):
        for row in range(rows):


            intensity = fractal_map[col][row]

            color = intensity_to_color(intensity)

            canvas.SetPixel(col, row, *color)



    canvas = matrix.SwapOnVSync(canvas)
    canvas.Clear()

try:
    print("Press CTRL-C to stop.")
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    sys.exit(0)
