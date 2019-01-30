from math import pi, sin, cos

import sys

from direct.gui.OnscreenText import OnscreenText, Material
from direct.showbase.ShowBase import ShowBase, TextNode, CardMaker, CollisionSphere, CollisionNode
from direct.showbase.ShowBaseGlobal import globalClock
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import Point3
from panda3d.ode import OdeWorld, OdeBody, OdeMass, OdeSimpleSpace
from panda3d.core import Quat


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.base = self

        # circle to throw to
        self.circle = self.loader.loadModel("models/circle.egg")
        self.circle.reparentTo(self.render)
        self.circle.setColor(0.2, 0, 0.7)
        self.circle.setPos(0, 300, 0)
        self.circle.setScale(10)

        # ball
        self.ballRoot = self.render.attachNewNode("ballRoot")
        self.ball = self.loader.loadModel("models/ball")
        self.ball.reparentTo(self.ballRoot)
        self.ball.setPos(0, 0, 0)
        self.ball.setScale(10)
        self.ball.setColor(0.7, 0.4, 0.4)
        m = Material()
        m.setSpecular((1, 1, 1, 1))
        m.setShininess(96)
        self.ball.setMaterial(m, 1)

        self.ball.ls()

        # Setup our physics world and the body
        self.world = OdeWorld()
        self.world.setGravity(0, 0, -9.81)
        # self.world.initSurfaceTable(1)
        # self.world.setSurfaceEntry(0, 0, 150, 0.0, 9.1, 0.9, 0.00001, 0.0, 0.002)
        self.body = OdeBody(self.world)
        self.M = OdeMass()
        self.M.setSphereTotal(5, 1.0)
        self.body.setMass(self.M)
        self.body.setPosition(self.ball.getPos(self.render))
        self.body.setQuaternion(self.ball.getQuat(self.render))

        # self.cs = CollisionSphere(0, 0, 0, 20)
        # self.cnodePath = myNodePath.attachNewNode(CollisionNode('cnode'))
        # self.cnodePath.node().addSolid(cs)
        # self.cnodePath.show()


        # Add a plane to collide with
        self.cm = CardMaker("ground")
        self.cm.setFrame(-300, 300, 0, 300)
        self.ground = self.render.attachNewNode(self.cm.generate())
        self.ground.setPos(0, 0, 0)
        self.ground.lookAt(0, 0, -1)

        # self.space = OdeSimpleSpace()
        # self.space.setAutoCollideWorld(self.world)

        # self.disableMouse()

        self.base.accept('escape', sys.exit, [0])
        self.base.accept('mouse1', lambda: self.startIncreasingForce())
        self.base.accept('mouse1-up', lambda: self.throwBall())
        self.mouseText = self.genLabelText("", 5)
        # self.mouseTask = taskMgr.add(self.mouseTask, "Mouse Task")

        # Set the camera position
        self.camera.setPos(0, -1000, 0)
        self.camera.lookAt(0, 0, 100)

        # Create an accumulator to track the time since the sim
        # has been running
        self.deltaTimeAccumulator = 0.0
        # This stepSize makes the simulation run at 30 frames per second
        self.stepSize = 1.0 / 30
        self.force = 0


    def throwBall(self):
        print('throw')
        self.taskMgr.remove("Increase Force")
        self.body.setForce(0, self.force, self.force)
        self.updateBallTask = taskMgr.add(self.updateBallPosTask, "Update Ball Position Task")


    def genLabelText(self, text, i):
        text = OnscreenText(text = text, pos=(-1.3, .5-.05*i), fg=(0, 1, 0, 1),
                      align = TextNode.ALeft, scale = .05)
        return text

    def increaseForceTask(self, task):
        self.taskMgr.remove("Mouse Task")
        print(self.force)
        increasingDelay = 100
        for i in range(0, increasingDelay):
            pass
        self.force += 100
        return task.cont

    def startIncreasingForce(self):
        self.increaseForceTask = taskMgr.add(self.increaseForceTask, "Increase Force")

    def mouseTask(self, task):
        x, y = 0, 0
        mw = self.base.mouseWatcherNode

        hasMouse = mw.hasMouse()
        if hasMouse:
            # get the window manager's idea of the mouse position
            x, y = mw.getMouseX(), mw.getMouseY()

        # scale position and delta to pixels for user
        w, h = self.win.getSize()
        x, y = int(x * (w / 2)), int(y * h)
        self.ball.setPos(x, 0, 0)
        self.body.setPosition(self.ball.getPos(self.render))
        self.body.setQuaternion(self.ball.getQuat(self.render))
        self.mouseText.setText("Mouse: {0}, {1}".format(x, y))

        return task.cont

    def updateBallPosTask(self, task):
        print('updating')
        self.deltaTimeAccumulator += globalClock.getDt()
        while self.deltaTimeAccumulator > self.stepSize:
            # Remove a stepSize from the accumulator until
            # the accumulated time is less than the stepsize
            self.deltaTimeAccumulator -= self.stepSize
            # Step the simulation
            self.world.quickStep(self.stepSize)
        self.ball.setPosQuat(self.render, self.body.getPosition(), Quat(self.body.getQuaternion()))
        return task.cont

    def ballCollision(self):
        print('hit')

app = MyApp()
app.run()