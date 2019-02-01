from vpython import *
import math

ringThickness = 0.2
targetSpeed = 0.1
ballRadius = 1
ringRadius = 2
ringHeight = 10
floorRadius = 5
wallThickness = 0.1
gameBoundsX = (-floorRadius, floorRadius)

g = -9.8

increaseStep = 0.000005


class VGame(object):

    _targetDirection = True  # 1 right, 0 left
    Points = 0

    def __init__(self):
        self.ball = sphere(radius=ballRadius, color=color.red)
        self.floor = box(pos=vector(0, 0, 0), size=vector(2 * floorRadius, wallThickness, 2 * floorRadius), color=color.green)
        self.target = ring(pos=vector(0, ringHeight, -floorRadius), axis=vector(0, 0, 1), radius=ringRadius, thickness=ringThickness,
                           color=color.red, velocity=vector(targetSpeed, 0, 0))
        self.score = label(pos=vector(floorRadius, 0, 0), depth=-0.1, color=color.blue, billboard=True)
        self.initialize()

        # events
        scene.bind("mouseup", self.throwBall)
        scene.bind("mousedown", self.startIncreasingForce)

    def initialize(self):
        # ball
        self.ball.pos = vector(0, wallThickness + ballRadius, floorRadius)
        self.ball.velocity = vector(0, 0, 0)

        # params
        self._blockBall = False
        self._throw = False
        self._force = 0
        self._dt = 0

    def run(self, _rate=60):
        while True:
            rate(_rate)
            self._updateScene()
            if self._updateScore() or self.isFinished():
                self.restart()

    def restart(self):
        self.initialize()

    def isFinished(self):
        return self.ball.pos.y - ballRadius < 0 or self.ball.pos.z + ballRadius < -floorRadius

    def _updateScene(self):
        self._updateTarget()
        self._updateBall()

    def _updateBall(self):
        if not self._blockBall:
            self._moveBall()
        elif self._throw:
            self._flyBall()
            self._dt += 0.001

    def _moveBall(self):
        ballPositionX = scene.mouse.pos.x
        if ballPositionX > gameBoundsX[1]:
            ballPositionX = gameBoundsX[1]
        if ballPositionX < gameBoundsX[0]:
            ballPositionX = gameBoundsX[0]
        self.ball.pos.x = ballPositionX

    def _flyBall(self):
        self._changeBallVelocityZ()
        self._changeBallVelocityY()
        self.ball.pos = self.ball.pos + self.ball.velocity

    def _changeBallVelocityY(self):
        self.ball.velocity.y = self._force + g * self._dt

    def _changeBallVelocityZ(self):
        # constant speed
        self.ball.velocity.z = -self._force

    def _updateScore(self):
        updated = False
        if self._ballFitTarget():
            self.Points += 1
            updated = True
        self.score.text = "Points: {0}".format(str(self.Points))
        return updated

    def throwBall(self):
        self._throw = True

    def startIncreasingForce(self):
        self._blockBall = True
        while not self._throw:
            delay = 100
            while delay > 0:
                delay -= 1
            self._force += increaseStep

    def _updateTarget(self):
        self.target.pos = self.target.pos + self.target.velocity
        positionBound = self.target.pos.x + (ringRadius if self._targetDirection else -ringRadius)
        if (positionBound < gameBoundsX[0] and not self._targetDirection) or \
                (positionBound > gameBoundsX[1] and self._targetDirection):
            self._targetDirection = not self._targetDirection
            self.target.velocity.x = -self.target.velocity.x

    # check distances between target center and ball center
    def _ballFitTarget(self):
        targetPos = self.target.pos
        ballPos = self.ball.pos
        dist = math.sqrt((targetPos.x - ballPos.x) ** 2 + (targetPos.y - ballPos.y) ** 2)
        return abs(targetPos.z - ballPos.z) < (ballRadius / 2) and dist < self.target.radius - (ballRadius / 2)
