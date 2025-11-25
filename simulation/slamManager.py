import pybullet as p
import numpy as np

class slamManager:
    def __init__(self, drone_id, camera_width=640, camera_height=480, area_size=2.0):
        self.drone_id = drone_id        # integer PyBullet body ID
        self.img_width = camera_width
        self.img_height = camera_height
        self.area_size = area_size

        # Camera parameters
        self.fov = 60                    # degrees
        self.aspect = camera_width / camera_height
        self.near = 0.01
        self.far = 10.0

    def get_camera_frame(self):
        # Get drone position and orientation
        pos, ori = p.getBasePositionAndOrientation(self.drone_id)
        rot_matrix = p.getMatrixFromQuaternion(ori)
        # Camera looks straight down
        cam_eye = pos
        cam_target = [pos[0], pos[1], pos[2] - 1.0]
        cam_up = [0, 1, 0]
        view_matrix = p.computeViewMatrix(cam_eye, cam_target, cam_up)
        proj_matrix = p.computeProjectionMatrixFOV(self.fov, self.aspect, self.near, self.far)

        width, height, rgb_img, depth_img, seg_img = p.getCameraImage(
            width=self.img_width,
            height=self.img_height,
            viewMatrix=view_matrix,
            projectionMatrix=proj_matrix,
        )
        return np.array(rgb_img)[:, :, :3]  # HxWx3

    def convert_box_to_world(self, box):
        """
        Convert bounding box (xmin, ymin, xmax, ymax) in image to world coordinates
        assuming the camera points straight down.
        """
        x_min, y_min, x_max, y_max = box
        x_center = (x_min + x_max) / 2.0
        y_center = (y_min + y_max) / 2.0

        world_x = (x_center / self.img_width - 0.5) * self.area_size
        world_y = (y_center / self.img_height - 0.5) * self.area_size
        world_z = 0.05  # approximate syringe height

        return world_x, world_y, world_z

    def move_to(self, x, y, z):
        """
        Simple movement: set drone position directly. In real sim, use PID/velocity.
        """
        p.resetBasePositionAndOrientation(self.drone_id, [x, y, z], [0, 0, 0, 1])
