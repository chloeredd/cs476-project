import open3d as o3d
import numpy as np

class SLAMNavigator:
    '''
    Simulate SLAM navigation using Open3D odometry.
    Provide waypoints for the drone to move through
    '''

    def __init__(self, drone):
        self.drone = drone
        #Initial pose
        self.pose = np.eye(4)
        self.waypoints = []
        #Track which syringes have been marked 
        self.visitedSyringes = set()

    def addSyringeTarget(self, syringePosition, syringeID):
        #Add syringe location as a new waypoint if not already
        #visited
        if syringeID not in self.visitedSyringes:
            self.waypoints.append((syringePosition, syringeID))

    def getNextTarget(self):
        #Get the next waypoint to move toward
        if not self.waypoints:
            return None
        return self.waypoints.pop(0)
    
    def markVisited(self, syringeID):
        self.visitedSyringes.add(syringeID)
    
    def updatePose(self):
        '''
        Update pose using current drone position
        '''

        self.pose[:3, 3] = self.drone.getPosition()
        return self.pose