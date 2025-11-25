import pybullet as p
import pybullet_data
import random
import time
import yaml

from simulation.drone import Drone
from simulation.syringe import Syringe
from simulation.camera import Camera

class SimulationEnvironment:
    def __init__(self, numSyringes=8, numDistractions=8, areaSize=2.0):
        with open("configs/simulation_config.yaml") as f:
            self.cfg = yaml.safe_load(f)
        self.gui = self.cfg["simulation"]["gui"]
        self.time_step = self.cfg["simulation"]["time_step"]

        if self.gui:
            p.connect(p.GUI)
        else:
            p.connect(p.DIRECT)

        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, self.cfg["simulation"]["gravity"])
        p.setTimeStep(self.time_step)

        # Load plane
        self.plane = p.loadURDF("plane.urdf")

        # Load drone
        self.drone = Drone()

        # Camera wrapper
        self.camera = Camera(self.drone)

        # Spawn syringes
        self.syringes = []
        for _ in range(numSyringes):
            x = random.uniform(-areaSize/2, areaSize/2)
            y = random.uniform(-areaSize/2, areaSize/2)
            z = 0.05
            s = Syringe([x, y, z])
            self.syringes.append(s)

        # Spawn distractions (green boxes)
        self.distractions = []
        for _ in range(numDistractions):
            x = random.uniform(-areaSize/2, areaSize/2)
            y = random.uniform(-areaSize/2, areaSize/2)
            visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.05,0.05,0.05], rgbaColor=[0,1,0,1])
            collision = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.05,0.05,0.05])
            body = p.createMultiBody(baseMass=0.01, baseCollisionShapeIndex=collision,
                                     baseVisualShapeIndex=visual, basePosition=[x,y,0.05])
            self.distractions.append(body)

        print("[Environment] Initialized with", len(self.syringes), "syringes and", len(self.distractions), "distractors.")

    def step(self):
        p.stepSimulation()
        time.sleep(self.time_step)

    def shutdown(self):
        p.disconnect()
