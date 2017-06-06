from PIL import Image
import numpy as np

def makeGraph():

    map1 = Image.open("mi.png")

    x, y = map1.size

    mi = np.zeros((y, x))
    mi1 = np.zeros((35, 35))
    print(x, y)
    for i in range(1, x):
        for p in range(1, y):

            r, g, b, a = map1.getpixel((i, p))
            if r == 185 and g == 122 and b == 87:
                mi[p, i] = 10
            if r == 34 and g == 177 and b == 76:
                mi[p, i] = 2
            if r == 127 and g == 127 and b == 127:
                mi[p, i] = 1
            if r == 255 and g == 174 and b == 201:
                mi[p, i] = 200

    for i in range(0, 34):
        for p in range(0, 34):
            for q in range(0, 20):
                for l in range(0, 20):
                    mi1[i][p] = mi1[i][p]+mi[i*20+q][p*20+l]

    for i in range(0, 35):
        for p in range(0, 35):
            mi1[i][p] /= 400

    img1 = Image.new("RGB", (681, 681))
    for i in range(0, 34):
        for p in range(0, 34):
            if mi1[i][p] < 12:
                r = int(mi1[p, i]*20)
                g = int(mi1[p, i]*20)
                b = int(mi1[p, i]*20)
            if mi1[i][p] > 12:
                r = int(mi1[p, i]*3)
                g = int(mi1[p, i]*3)
                b = int(mi1[p, i]*3)
            for q in range(0,20):
                for l in range(0, 20):
                    img1.putpixel((i*20+q, p*20+l), (r, g, b))
    #img1.save("output2.png")
    #print(mi1)
    return mi1

