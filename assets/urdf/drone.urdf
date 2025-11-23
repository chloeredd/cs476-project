import pybullet as p
import os

class Drone:
    '''
    This class provides:
    Initialization
    Position retrieval 
    Custom behaviors (marker dropping, movement commands, etc.)
    '''

    def __init__(self, startPos = [0, 0, 1]):
        #Path to the drone.urdf file
        #simulation and assets are on the same "level" as each other 
        #in the project hierarchy, so use os.path.join to create
        #a path to the .urdf file
        urdfPath = os.path.join(os.path.dirname(__file__), "..", "assets", "urdf", "drone.urdf")
        urdfPath = os.path.abspath(urdfPath)

        #Use a simple cube if the user doesn't have a drone URDF yet
        if not os.path.exists(urdfPath):
            print("Drone URDF not found. Using a simple cube instead")
            self.body = p.loadURDF("cube.urdf", startPos)
        else:
            self.body = p.loadURDF(urdfPath, startPos)

    def getPosition(self):
        #Return the drone's (x, y, z) position
        position, _ = p.getBasePositionAndOrientation(self.body)
        return position
    
    def dropMarker(self):
        '''
        Drop a marker below the drone
        The marker is created in simulation/marker.py
        '''
        from simulation.marker import dropMarker
        position = self.getPosition()
        #For the altitude of the marker have it be the drone's altitude
        #minus 0.2
        dropMarker([position[0], position[1], position[2] - 0.2])
        
        
