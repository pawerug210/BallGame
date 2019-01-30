from math import pi, sin, cos

import sys

from direct.gui.OnscreenText import OnscreenText, Material
from direct.showbase.ShowBase import ShowBase, TextNode
from direct.showbase.ShowBaseGlobal import globalClock
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import Point3
from panda3d.ode import OdeWorld, OdeBody, OdeMass
from panda3d.core import Quat


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.base = self
        self.ball()
        self.setup()

        # # Load the cube where the ball will fall from
        # self.cube = self.loader.loadModel("box.egg")
        # self.cube.reparentTo(self.render)
        # self.cube.setColor(0.2, 0, 0.7)
        # self.cube.setScale(20)
        #
        # # Load the smiley model which will act as our iron ball
        # self.sphere = self.loader.loadModel("box.egg")
        # self.sphere.reparentTo(self.render)
        # self.sphere.setPos(10, 0, 21)
        # self.sphere.setColor(0.7, 0.4, 0.4)
        #
        # # Setup our physics world and the body
        # self.world = OdeWorld()
        # self.world.setGravity(0, 0, -9.81)
        # self.body = OdeBody(self.world)
        # self.M = OdeMass()
        # self.M.setSphere(7874, 1.0)
        # self.body.setMass(self.M)
        # self.body.setPosition(self.sphere.getPos(self.render))
        # self.body.setQuaternion(self.sphere.getQuat(self.render))
        #
        # # Set the camera position
        # self.disableMouse()
        # self.camera.setPos(80, -20, 40)
        # self.camera.lookAt(0, 0, 10)
        #
        # # Create an accumulator to track the time since the sim
        # # has been running
        # self.deltaTimeAccumulator = 0.0
        # # This stepSize makes the simulation run at 90 frames per second
        # self.stepSize = 1.0 / 90.0



        # Add the spinCameraTask procedure to the task manager.
        self.taskMgr.doMethodLater(1.0, self.simulationTask, "Physics Simulation")

    def genLabelText(self, text, i):
        text = OnscreenText(text = text, pos = (-1.3, .5-.05*i), fg=(0,1,0,1),
                      align = TextNode.ALeft, scale = .05)
        return text

    def ball(self):
        self.ball = self.loader.loadModel("box.egg")
        self.ball.reparentTo(self.render)
        self.ball.setScale(1)
        self.ball.setColor(0.7, 0.4, 0.4)
        # This section deals with adding a specular highlight to the ball to make
        # it look shiny.  Normally, this is specified in the .egg file.
        m = Material()
        m.setSpecular((1, 1, 1, 1))
        m.setShininess(96)
        self.ball.setMaterial(m, 1)

    def setup(self):
        # Disable the camera trackball controls.
        self.disableMouse()

        self.base.accept('escape', sys.exit, [0])
        self.mouseText = self.genLabelText("", 5)
        self.mouseTask = taskMgr.add(self.mouseTask, "Mouse Task")

    def mouseTask(self, task):
        x, y = 0, 0
        mw = self.base.mouseWatcherNode

        hasMouse = mw.hasMouse()
        if hasMouse:
            # get the window manager's idea of the mouse position
            x, y = mw.getMouseX(), mw.getMouseY()

        # scale position and delta to pixels for user
        w, h = self.win.getSize()
        x, y = int(x * w), int(y * h)
        self.ball.setPos(-8, 100, 0)
        self.mouseText.setText("Mouse: {0}, {1}".format(x, y))

        return Task.cont

    def simulationTask(self, task):
        # Set the force on the body to push it off the ridge
        self.body.setForce(0, min(task.time ** 4 * 500000 - 500000, 0), 0)
        # Add the deltaTime for the task to the accumulator
        self.deltaTimeAccumulator += globalClock.getDt()
        while self.deltaTimeAccumulator > self.stepSize:
            # Remove a stepSize from the accumulator until
            # the accumulated time is less than the stepsize
            self.deltaTimeAccumulator -= self.stepSize
            # Step the simulation
            self.world.quickStep(self.stepSize)
        # set the new positions
        print('now')
        self.sphere.setPosQuat(self.render, self.body.getPosition(), Quat(self.body.getQuaternion()))
        return task.cont

app = MyApp()
app.run()