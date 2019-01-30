from direct.directbase import DirectStart
from panda3d.ode import OdeWorld, OdeBody, OdeMass
from panda3d.core import Quat

# Load the cube where the ball will fall from
cube = loader.loadModel("box.egg")
cube.reparentTo(render)
cube.setColor(0.2, 0, 0.7)
cube.setScale(20)

# Load the smiley model which will act as our iron ball
sphere = loader.loadModel("smiley.egg")
sphere.reparentTo(render)
sphere.setPos(10, 1, 21)
sphere.setColor(0.7, 0.4, 0.4)

# Setup our physics world and the body
world = OdeWorld()
world.setGravity(0, 0, -9.81)
body = OdeBody(world)
M = OdeMass()
M.setSphereTotal(20, 1.0)
body.setMass(M)
body.setPosition(sphere.getPos(render))
body.setQuaternion(sphere.getQuat(render))
body.setForce(0, -2000, 8000)
# body.setLinearVel(0, -2, 0)


# Set the camera position
base.disableMouse()
base.camera.setPos(80, 0, 40)
base.camera.lookAt(0, 0, 10)

# Create an accumulator to track the time since the sim
# has been running
deltaTimeAccumulator = 0.0
# This stepSize makes the simulation run at 90 frames per second
stepSize = 1.0 / 90.0


# The task for our simulation
def simulationTask(task):
    global deltaTimeAccumulator
    # Set the force on the body to push it off the ridge
    # body.setLinearVel(0, -2, 0)
    # body.addRelForce(0, -2, 4000)
    # Add the deltaTime for the task to the accumulator
    deltaTimeAccumulator += globalClock.getDt()
    while deltaTimeAccumulator > stepSize:
        # Remove a stepSize from the accumulator until
        # the accumulated time is less than the stepsize
        deltaTimeAccumulator -= stepSize
        # Step the simulation
        world.quickStep(stepSize)
    # set the new positions
    print('now')
    sphere.setPosQuat(render, body.getPosition(), Quat(body.getQuaternion()))
    return task.cont


taskMgr.doMethodLater(1.0, simulationTask, "Physics Simulation")

run()