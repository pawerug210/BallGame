from vpython import *
import math


class VGame(object):

    _targetDirection = True  # 1 right, 0 left
    Points = 0

    def __init__(self, params):
        self.params = params
        self.ball = sphere(radius=self.params.ballRadius, color=color.red)
        self.floor = box(pos=vector(0, 0, 0), size=vector(2 * self.params.floorRadius, self.params.wallThickness, 2 * self.params.floorRadius), color=color.green)
        self.target = ring(pos=vector(0, self.params.ringHeight, -self.params.floorRadius), axis=vector(0, 0, 1), radius=self.params.ringRadius, thickness=self.params.ringThickness,
                           color=color.red, velocity=vector(self.params.targetSpeed, 0, 0))
        self.score = label(pos=vector(self.params.floorRadius, 0, 0), depth=-0.1, color=color.orange, billboard=True)
        self.initialize()

        # events
        scene.bind("mouseup", self.throwBall)
        scene.bind("mousedown", self.startIncreasingForce)

    def initialize(self):
        # ball
        self.ball.pos = vector(0, self.params.wallThickness + self.params.ballRadius, self.params.floorRadius)
        self.ball.velocity = vector(0, 0, 0)

        # params
        self._blockBall = False
        self._throw = False
        self._force = 0
        self._dt = 0
        self.gameBoundsX = (-self.params.floorRadius, self.params.floorRadius)

    def run(self, _rate=60):
        while True:
            rate(_rate)
            self._updateScene()
            if self._updateScore() or self.isFinished():
                self.restart()

    def restart(self):
        self.initialize()

    def isFinished(self):
        return self.ball.pos.y - self.params.ballRadius < 0 or self.ball.pos.z + self.params.ballRadius < -self.params.floorRadius

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
        if ballPositionX > self.gameBoundsX[1]:
            ballPositionX = self.gameBoundsX[1]
        if ballPositionX < self.gameBoundsX[0]:
            ballPositionX = self.gameBoundsX[0]
        self.ball.pos.x = ballPositionX

    def _flyBall(self):
        self._changeBallVelocityZ()
        self._changeBallVelocityY()
        self.ball.pos = self.ball.pos + self.ball.velocity

    def _changeBallVelocityY(self):
        self.ball.velocity.y = self._force + self.params.g * self._dt

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
            self._force += self.params.increaseStep

    def _updateTarget(self):
        self.target.pos = self.target.pos + self.target.velocity
        positionBound = self.target.pos.x + (self.params.ringRadius if self._targetDirection else -self.params.ringRadius)
        if (positionBound < self.gameBoundsX[0] and not self._targetDirection) or \
                (positionBound > self.gameBoundsX[1] and self._targetDirection):
            self._targetDirection = not self._targetDirection
            self.target.velocity.x = -self.target.velocity.x

    # check distances between target center and ball center
    def _ballFitTarget(self):
        targetPos = self.target.pos
        ballPos = self.ball.pos
        dist = math.sqrt((targetPos.x - ballPos.x) ** 2 + (targetPos.y - ballPos.y) ** 2)
        return abs(targetPos.z - ballPos.z) < (self.params.ballRadius / 2) and dist < self.target.radius - (self.params.ballRadius / 2)
