from vpython import *

ringThickness = 0.2
targetSpeed = 0.1
ballRadius = 1
ringRadius = 2
floorRadius = 10
wallThickness = 0.1

g = -9.8

increaseStep = 0.000005
blockBall = False
gameBoundsX = (-floorRadius, floorRadius)


class VGame(object):

    targetDirection = True  # 1 right, 0 left

    def __init__(self):
        self.ball = sphere(radius=ballRadius, color=color.red)
        self.floor = box(pos=vector(0, 0, 0), size=vector(2 * floorRadius, wallThickness, 2 * floorRadius), color=color.green)
        self.target = ring(pos=vector(0, 10, -10), axis=vector(0, 0, 1), radius=ringRadius, thickness=ringThickness,
                           color=color.green, velocity=vector(targetSpeed, 0, 0))
        self.initialize()

        # events
        scene.bind("mouseup", self.throwBall)
        scene.bind("mousedown", self.startIncreasingForce)

    def initialize(self):
        # ball
        self.ball.pos = vector(0, wallThickness + ballRadius, floorRadius)
        self.ball.velocity = vector(0, 0, 0)

        # params
        self.blockBall = False
        self.throw = False
        self.force = 0
        self.dt = 0

    def run(self, _rate=60):
        while True:
            rate(_rate)
            self._updateScene()
            if self.isFinished():
                self.restart()

    def restart(self):
        self.initialize()

    def isFinished(self):
        return self.ball.pos.y - ballRadius < 0 or self.ball.pos.z + ballRadius < -floorRadius

    def _updateScene(self):
        self._updateTarget()
        self._updateBall()

    def _updateBall(self):
        if not self.blockBall:
            self._moveBall()
        elif self.throw:
            self._flyBall()
            self.dt += 0.001

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
        self.ball.velocity.y = self.force + g * self.dt

    def _changeBallVelocityZ(self):
        # constant speed
        self.ball.velocity.z = -self.force

    def throwBall(self):
        self.throw = True

    def startIncreasingForce(self):
        self.blockBall = True
        while not self.throw:
            delay = 100
            while delay > 0:
                delay -= 1
            self.force += increaseStep

    def _updateTarget(self):
        self.target.pos = self.target.pos + self.target.velocity
        positionBound = self.target.pos.x + (ringRadius if self.targetDirection else -ringRadius)
        if (positionBound < gameBoundsX[0] and not self.targetDirection) or \
                (positionBound > gameBoundsX[1] and self.targetDirection):
            self.targetDirection = not self.targetDirection
            self.target.velocity.x = -self.target.velocity.x


game = VGame()
game.run()
