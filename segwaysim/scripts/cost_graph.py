from PIL import Image
import numpy as np
import os
import sys


def makeGraph():
    try:

        dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        map1 = Image.open(dir_path + "/data/segwaysim/mi2.png")
        map2 = Image.open(dir_path + "/data/segwaysim/mi3.png")

    except:
        print("can't open the image in cost_graph")
        sys.exit(1)

    x, y = map1.size
    x1, y1 = map2.size
    height = np.zeros((y1, x1))
    height1 = np.zeros((35, 35))
    mi = np.zeros((y, x))
    mi1 = np.zeros((35, 35))
    for i in range(1, x):
        for p in range(1, y):

            r, g, b, a = map1.getpixel((i, p))
            if (r == 185 and g == 122 and b == 87):
                mi[p, i] = 10
            if (r == 34 and g == 177 and b == 76):
                mi[p, i] = 2
            if (r == 127 and g == 127 and b == 127):
                mi[p, i] = 1
            if (r == 255 and g == 174 and b == 201):
                mi[p, i] = 200

    for i in range(1, x1):
        for p in range(1, y1):
            r, g, b, a = map2.getpixel((i, p))
            if (r == 63 and g == 72 and b == 204):
                height[p, i] = 10

    for i in range(0, 34):
        for p in range(0, 34):
            for q in range(0, 20):
                for l in range(0, 20):
                    height1[i][p] = height1[i][p] + height[i * 20 + q][p * 20 + l]

    for i in range(0, 34):
        for p in range(0, 34):
            height1[i][p] /= 400
    for i in range(0, 34):
        for p in range(0, 34):
            for q in range(0, 20):
                for l in range(0, 20):
                    mi1[i][p] = mi1[i][p] + mi[i * 20 + q][p * 20 + l]

    for i in range(0, 34):
        for p in range(0, 34):
            mi1[i][p] /= 400
            mi1[i][p] += height1[i][p]

    return mi1

