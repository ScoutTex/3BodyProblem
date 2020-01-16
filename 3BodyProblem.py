import cv2
import numpy as np
import math
import copy

# init param
apos = [30, 0]
amass = 1
aspd = [0, 1]

bpos = [-15, 25.980762]
bmass = 1
bspd = [-0.8660254, -.5]

cpos = [-15, -25.980762]
cmass = 1
cspd = [0.8660254, -.5]

# video param

WIDTH = 512
HEIGHT = 512
BALLRADIUS = 5

LENGTH = 10000

GRAVITY_CONST = 40


def drawpix(img, pixpos, color):
    if pixpos[0] >= 0 and pixpos[0] < HEIGHT and pixpos[1] >= 0 and pixpos[1] < WIDTH:
        img[pixpos[0], pixpos[1]] = color

def ballpos2pixpos(ballpos):
    left = ballpos[0] + WIDTH // 2
    top = -ballpos[1] + HEIGHT // 2
    return (top, left)

def dist(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

def drawball(img, ballpos, color):
    (top, left) = ballpos2pixpos(ballpos)
    for t in range(top - BALLRADIUS, top + BALLRADIUS):
        for l in range(left - BALLRADIUS, left + BALLRADIUS):
            if dist((top, left), (t, l)) < BALLRADIUS:
                drawpix(img, (t, l), color)

def drawaxis(img):
    topc = HEIGHT // 2
    leftc = WIDTH // 2
    darkgray = [20, 20, 20]
    for l in range(WIDTH):
        drawpix(img, (topc, l), darkgray)
    for t in range(HEIGHT):
        drawpix(img, (t, leftc), darkgray)

def doublepos2intpos(doublepos):
    return (round(doublepos[0]), round(doublepos[1]))

def drawballs(img):
    drawball(img, doublepos2intpos(apos), [0, 0, 255])
    drawball(img, doublepos2intpos(bpos), [0, 255, 0])
    drawball(img, doublepos2intpos(cpos), [255, 0, 0])

def initimg():
    img = [[[0, 0, 0] for _ in range(WIDTH)] for _ in range(HEIGHT)]
    img = np.array(img, dtype='uint8')
    drawaxis(img)
    return img

def force(amass, apos, bmass, bpos):
    if apos[0] == bpos[0] and apos[1] == bpos[1]:
        return 0, 0
    f = GRAVITY_CONST * amass * bmass / (dist(apos, bpos) ** 2)
    if apos[0] == bpos[0]:
        return 0, f
    elif apos[1] == bpos[1]:
        return f, 0
    dx = abs(apos[0] - bpos[0])
    dy = abs(apos[1] - bpos[1])
    f0 = f / dist(apos, bpos) * dx
    f1 = f / dist(apos, bpos) * dy
    return f0, f1
    

def ballsmove():
    dab0, dab1 = force(amass, apos, bmass, bpos)
    dac0, dac1 = force(amass, apos, cmass, cpos)
    dbc0, dbc1 = force(bmass, bpos, cmass, cpos)

    if apos[0] > bpos[0]:
        dab0 = -dab0
    aspd[0] += dab0
    bspd[0] -= dab0
    if apos[1] > bpos[1]:
        dab1 = -dab1
    aspd[1] += dab1
    bspd[1] -= dab1
    if apos[0] > cpos[0]:
        dac0 = -dac0
    aspd[0] += dac0
    cspd[0] -= dac0
    if apos[1] > cpos[1]:
        dac1 = -dac1
    aspd[1] += dac1
    cspd[1] -= dac1
    if bpos[0] > cpos[0]:
        dbc0 = -dbc0
    bspd[0] += dbc0
    cspd[0] -= dbc0
    if bpos[1] > cpos[1]:
        dbc1 = -dbc1
    bspd[1] += dbc1
    cspd[1] -= dbc1

    apos[0] += aspd[0]
    apos[1] += aspd[1]
    bpos[0] += bspd[0]
    bpos[1] += bspd[1]
    cpos[0] += cspd[0]
    cpos[1] += cspd[1]


def main():
    imgarr = []

    baseimg = initimg()

    out = cv2.VideoWriter('3BodyProblem.avi', cv2.VideoWriter_fourcc(*'DIVX'), 60, (WIDTH, HEIGHT))

    for i in range(LENGTH):
        img = copy.deepcopy(baseimg)
        drawballs(img)
        # imgarr.append(img)
        ballsmove()

        out.write(img)

        # cv2.imshow('winname', img)
        # cv2.waitKey()

    # cv2.imshow('winname', baseimg)
    # cv2.waitKey()

    out.release()


if __name__ == '__main__':
    main()