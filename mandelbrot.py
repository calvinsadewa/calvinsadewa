# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 00:12:00 2017

@author: calvin-pc
"""

from timeit import default_timer as timer
from matplotlib.pylab import imshow, jet, show, ion
import matplotlib.pyplot as plt
import math
import numpy as np

plt.rcParams["figure.figsize"] = (10,10)

from numba import jit

rgbs = []
def setRgb(x,y,z):
    global rgbs
    a = list(rgbs)
    a.append([x,y,z])
    rgbs = np.array(a)

setRgb(66, 30, 15);
setRgb(25, 7, 26);
setRgb(9, 1, 47);
setRgb(4, 4, 73);
setRgb(0, 7, 100);
setRgb(12, 44, 138);
setRgb(24, 82, 177);
setRgb(57, 125, 209);
setRgb(134, 181, 229);
setRgb(211, 236, 248);
setRgb(241, 233, 191);
setRgb(248, 201, 95);
setRgb(255, 170, 0);
setRgb(204, 128, 0);
setRgb(153, 87, 0);
setRgb(106, 52, 3);
l_rgbs = len(rgbs)

@jit
def mandel(x, y, max_iters,f):
    """
    Given the real and imaginary parts of a complex number,
    determine if it is a candidate for membership in the Mandelbrot
    set given a fixed number of iterations.
    """
    i = 0
    c = complex(x,y)
    z = 0.0j
    for i in range(max_iters):
        z = z*z + c
        if (z.real*z.real + z.imag*z.imag) >= 4:
            return 256 - (i % (256/f) * f)
    return 0

@jit
def create_fractal(min_x, max_x, min_y, max_y, image, iters,f):
    height = image.shape[0]
    width = image.shape[1]

    pixel_size_x = (max_x - min_x) / width
    pixel_size_y = (max_y - min_y) / height
    for x in range(width):
        real = min_x + x * pixel_size_x
        for y in range(height):
            imag = min_y + y * pixel_size_y
            color = mandel(real, imag, iters,f)
            image[y, x] = color

    return image
    
width = 1000
height = 1000
iterat = 255*8
#x1,x2,y1,y2 = (-0.10309486080000001, -0.10309375488000001, 0.9479814164479998, 0.947982522368) wave of hand
#x1,x2,y1,y2 = (-2.0, 2.0, -2.0, 2.0) Whole mandelbrot
#x1,x2,y1,y2 = (-0.10309429899264001, -0.10309429014528002, 0.947982190592, 0.9479821994393599) another mandelbrot
#x1,x2,y1,y2 = (-1.420689408000051, -1.4198364160000487, 0.0023086079999994663, 0.003161599999999487) cross
def zoom(z_x1,z_x2,z_y1,z_y2):
    l_x = x2 - x1
    o_x = x1
    l_y = y2-y1
    o_y = y1
    return (l_x*z_x1/width + o_x,l_x*z_x2/width + o_x,l_y*z_y1/height + o_y,l_y*z_y2/height + o_y)
def set_zoom(z_x1,z_x2,z_y1,z_y2):
    global x1,x2,y1,y2
    x1,x2,y1,y2 = zoom(z_x1,z_x2,z_y1,z_y2)
    print((x1,x2,y1,y2))
def zoom_out(mag):
    return zoom(width-width*mag,width*mag,height-height*mag,height*mag)
def set_zoom_out(mag):
    global x1,x2,y1,y2
    x1,x2,y1,y2 = zoom_out(mag)
    print((x1,x2,y1,y2))
    
def show_picture(f = 1):
    image = np.zeros((height, width), dtype=np.uint8)
    s = timer()
    create_fractal(x1,x2,y1,y2, image, iterat,f)
    e = timer()
    print(e - s)
    imshow(image)
    show()
    return image