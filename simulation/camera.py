import pybullet as p
import numpy as np
import yaml

class Camera:
    def __init__(self, drone):
        self.drone = drone

        with open("configs/simulation_config.yaml") as f:
            config = yaml.safe_load(f)

        camera = config["camera"]
        self.w = camera["width"]
        self.h = camera["height"]
        self.fov = camera["fov"]
        self.near = camera["near"]
        self.far = camera["far"]

    def getFrame(self):
        #Get the position, orientation, and rotation of the drone
        position, orientation = p.getBasePositionAndOrientation(self.drone.body)
        rotation = p.getMatrixFromQuaternion(orientation)

        eye = position
        #Facing downwards
        target = [position[0] + rotation[0], position[1] + rotation[3], position[2] - 1] 

        #computeViewMatrix transforms world coordinates into camera
        #coordinates 
        view = p.computeViewMatrix(eye, target, [0, 0, 1])
        #generate the camera's intrinsic matrix 
        #this is used for rendering images in the simulation 
        projection = p.computeProjectionMatrixFOV(self.fov, 1.0, self.near, self.far)

        #capture an image from a virtual camera in the simulator
        #seg, a segmentation mask, is a pixel-level map in computer
        #vision that identifies and labels specific regions or objects
        #within an image
        _, _, rgb, _, seg = p.getCameraImage(
            width = self.w,
            height = self.h,
            viewMatrix = view,
            projectionMatrix = projection,
            renderer = p.ER_TINY_RENDERER
        )

        return np.array(rgb), np.array(seg)