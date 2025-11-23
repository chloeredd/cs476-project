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


#Edits that Seth made
import pybullet as p
import pybullet_data
import yaml
import os

from simulation.drone import Drone
from simulation.needle import Needle
from simulation.camera import Camera

class SimulationEnvironment:
    
    def __init__(self):

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
        #self.camera = Camera(self.drone)
        self.camera = Camera()

        #Spawn several example needles in fixed positions
        self.needles = [
            Needle([1, 0, 0.05]),
            Needle([0, 2, 0.05]),
        ]

        #The simulation has been initialized
        print("Simulation initialized")

    def step(self):
        #Advance the physics engine by one step
        p.stepSimulation()

    def shutdown(self):
        #Disconnect from PyBullet
        p.disconnect()
