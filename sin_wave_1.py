#!/usr/bin/env python
import time
import sys
import math

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

offset = 0

def get_ys(t, func):
    y1 = math.floor(func(t) * 15.5 + 15.5)
    y2 = math.ceil(func(t) * 15.5 + 15.5)
    return y1, y2

def plot_ys(c, t, func, canvas, color):
    y1, y2 = get_ys(t, func)
    canvas.SetPixel(c, y1, *color)
    canvas.SetPixel(c, y2, *color)

def next_color(r, g, b, rate):
    if r > 0 and g == 255:
        return max(r - rate, 0), g, b
    if g > 0 and b == 255:
        return r, max(g - rate, 0), b
    if b > 0 and r == 255:
        return r, g, max(b - rate, 0)
    if r == 255:
        return r, min(g + rate, 255), b
    if g == 255:
        return r, g, min(b + rate, 255)
    if b == 255:
        return min(r + rate, 255), g, b

#columns = [*range(options.cols)]

color_sin = (255, 0, 0)
color_cos = (0, 255, 0)

rate = round(256 * 12 / 64)

while True:

    offset += 2 * math.pi / 64

    color_sin = next_color(*color_sin, rate)
    color_cos = next_color(*color_cos, rate)

    local_color_sin = color_sin
    local_color_cos = color_cos

#    t = [2 * math.pi * c / 64 + offset for c in columns]

    for c in range(options.cols):
        local_color_sin = next_color(*local_color_sin, rate)
        local_color_cos = next_color(*local_color_cos, rate)

        t = 2 * math.pi * c / options.cols + offset

        plot_ys(c, t, math.sin, canvas, local_color_sin)
        plot_ys(c, t, math.cos, canvas, local_color_cos)

    canvas = matrix.SwapOnVSync(canvas)
    canvas.Clear()

try:
    print("Press CTRL-C to stop.")
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    sys.exit(0)
