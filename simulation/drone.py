import pybullet as p
import pybullet_data

class Drone:
    def __init__(self, start_pos=[0, 0, 1], start_ori=[0, 0, 0, 1]):
        """
        Loads the quadrotor URDF and stores its ID.
        """
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        self.drone_id = p.loadURDF("assets/drone.urdf", start_pos, start_ori)

    def get_id(self):
        return self.drone_id
