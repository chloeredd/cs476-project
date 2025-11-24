'''
import pybullet as p
import pybullet_data
import time

#connect to physics server
p.connect(p.GUI)



#insert models and other things here TODO


#running simulation
p.setGravity(0,0,-9.8)
while(True):
    p.stepSimulation()
    #time sleep

#disconnect may not be needed
p.disconnect()

'''

#Edits that Seth made
import pybullet as p
import pybullet_data
import yaml
import os
import random

from simulation.drone import Drone
from simulation.syringe import Syringe
from simulation.camera import Camera
from yag_slam import MonocularSLAM

class SimulationEnvironment:
    
    def __init__(self, numSyringes = 10, numDistractions = 10, areaSize = 2.0):

        #Load config (.yaml) file
        #Keeping configuration data outside of the code iself improves
        #maintainability
        with open("configs/simulation_config.yaml") as f:
            self.cfg = yaml.safe_load(f)

        #Get the gui and time_step parameter values from 
        #the yaml file 
        self.gui = self.cfg["simulation"]["gui"]
        self.time_step = self.cfg["simulation"]["time_step"]

        #Connect to the PyBullet physics engine
        if self.gui:
            #GUI mode is useful during development
            p.connect(p.GUI)
        else:
            #DIRECT mode is useful for testing
            p.connect(p.DIRECT)

        #PyBullet has some built-in URDFs (Unified Robot Description
        #Formats) and textures. We can add their search path
        p.setAdditionalSearchPath(pybullet_data.getDataPath())

        #Set the simulation parameters
        p.setGravity(0, 0, self.cfg["simulation"]["gravity"])
        p.setTimeStep(self.time_step)

        #Load a ground plane
        self.plane = p.loadURDF("plane.urdf")

        #Create the drone and attach a camera to it
        self.drone = Drone()
        self.camera = Camera(self.drone)

        self.syringes = []
        for _ in range(numSyringes):
            #x and y are random, but within the bounds of [-areaSize/2,
            #areaSize/2]
            #z will always be the same
            x = random.uniform(-areaSize/2, areaSize/2)
            y = random.uniform(-areaSize/2, areaSize/2)
            #Above the plane
            z = 0.05

            self.syringes.append(Syringe([x, y, z]))

        #Add distractions that the drone should ignore
        self.distractions = []
        
        #The distractions will be small yellow cubes
        for _ in range(numDistractions):
            visual = p.createVisualShape(p.GEOM_BOX, halfExtents = [0.05, 0.05, 0.05], rgbaColor = [0, 1, 0, 1])
            collision = p.createCollisionShape(p.GEOM_BOX, halfExtents = [0.05, 0.05, 0.05])
            body = p.createMultiBody(baseMass = 0.01, baseVisualShapeIndex = visual, baseCollisionShapeIndex = collision, 
                                     basePosition = [random.uniform(-areaSize/2, areaSize/2), random.uniform(-areaSize/2, areaSize/2), 
                                                     0.05])
            self.distractions.append(body)

        #The simulation has been initialized
        print("Simulation initialized with random syringe positions")

    def step(self):
        #Advance the physics engine by one step
        p.stepSimulation()

    def shutdown(self):
        #Disconnect from PyBullet
        p.disconnect()
