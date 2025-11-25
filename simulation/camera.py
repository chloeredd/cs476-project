import pybullet as p
import numpy as np
import yaml

class Camera:
    """
    Simple camera wrapper using PyBullet rendering.
    Returns (rgb_uint8, seg_mask) as numpy arrays.
    """
    def __init__(self, drone):
        self.drone = drone
        with open("configs/simulation_config.yaml") as f:
            cfg = yaml.safe_load(f)
        cam = cfg["camera"]
        self.w = cam["width"]
        self.h = cam["height"]
        self.fov = cam["fov"]
        self.near = cam["near"]
        self.far = cam["far"]

    def getFrame(self):
        # extract drone pose
        pos, orn = p.getBasePositionAndOrientation(self.drone.body)
        # compute camera facing downwards
        rot = p.getMatrixFromQuaternion(orn)
        # approximate forward vector from rotation matrix
        forward = [rot[0], rot[3], rot[6]]
        eye = pos
        # look 1 meter downwards relative to vehicle frame
        target = [pos[0] + forward[0], pos[1] + forward[1], pos[2] - 1.0]
        up = [0, 0, 1]

        view = p.computeViewMatrix(eye, target, up)
        aspect = float(self.w)/float(self.h)
        projection = p.computeProjectionMatrixFOV(self.fov, aspect, self.near, self.far)

        width, height, rgb, depth, seg = p.getCameraImage(
            width=self.w, height=self.h,
            viewMatrix=view, projectionMatrix=projection,
            renderer=p.ER_TINY_RENDERER
        )
        # rgb is (H,W,4) RGBA
        rgb_np = np.array(rgb, dtype=np.uint8)
        seg_np = np.array(seg, dtype=np.int32)
        return rgb_np, seg_np
