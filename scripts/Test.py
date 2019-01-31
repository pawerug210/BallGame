from vpython import *

# GlowScript 2.4 VPython
ringThickness = 0.2
targetSpeed = 0.1
ballRadius = 1
ringRadius = 2
wallThickness = 0.1
ball = sphere(pos=vector(0, wallThickness + ballRadius, 10), radius=ballRadius, color=color.red)
floor = box(pos=vector(0, 0, 0), size = vector(20, wallThickness, 20), color=color.green)
target = ring(pos=vector(0, 10, -10), axis=vector(0,0,1), radius=ringRadius, thickness=ringThickness, color=color.green)
target.velocity=vector(targetSpeed,0,0)
ball.velocity=vector(0, 0, 0)
dt=0.01
t=0
g=-9.8

throw = False
force = 0
increaseStep = 10
blockBall = False
targetBounds = (-10, 10)
targetDirection = True  # 1 right, 0 left

while True:
    rate(100)


def updateScene():
    while True:
        pass

def updateTarget():
    target.pos = target.pos + target.velocity
    positionBound = target.pos.x + (ringRadius if targetDirection else -ringRadius)
    if (positionBound < targetBounds[0] and not targetDirection) or (positionBound > targetBounds[1] and targetDirection):
        targetDirection = not targetDirection
        target.velocity.x = -target.velocity.x

def updateBall():
    print('updating ball')
    global ball, blockBall
    if True:
        temp = scene.mouse.pos
        print(temp)
        if temp:  # temp is None if no intersection with plane
            ball.pos = temp


def throwBall():
    global throw
    throw = True
    print('throwing')

def startIncreasingForce():
    global throw, force, increaseStep, blockBall
    blockBall = True
    while not throw:
        force += increaseStep
    print(force)


scene.bind("mouseup", throwBall)
scene.bind("mousedown", startIncreasingForce)
scene.bind("mousemove", updateBall)
