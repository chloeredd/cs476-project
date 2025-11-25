# navigation.py
import pybullet as p
import numpy as np
import math

class SLAMNavigator:
    def __init__(self, robot_id):
        self.robot_id = robot_id

        # Internal pose estimate
        self.x = 0.0
        self.y = 0.0
        self.yaw = 0.0

        # Map representation (simple occupancy grid)
        self.map_resolution = 0.1   # meters per cell
        self.map_size = 200         # 20m x 20m
        self.occupancy_grid = np.zeros((self.map_size, self.map_size))

    # ------------------------------------------------
    # Read simulated odometry from PyBullet
    # ------------------------------------------------
    def update_odometry(self):
        pos, quat = p.getBasePositionAndOrientation(self.robot_id)
        euler = p.getEulerFromQuaternion(quat)

        self.x, self.y = pos[0], pos[1]
        self.yaw = euler[2]

    # ------------------------------------------------
    # Very simple simulated lidar (raycasts)
    # ------------------------------------------------
    def run_lidar_scan(self, num_rays=60, max_dist=5.0):
        angles = np.linspace(-math.pi, math.pi, num_rays)
        distances = []

        for ang in angles:
            world_ang = self.yaw + ang

            dx = math.cos(world_ang) * max_dist
            dy = math.sin(world_ang) * max_dist

            start = [self.x, self.y, 0.2]
            end   = [self.x + dx, self.y + dy, 0.2]

            result = p.rayTest(start, end)[0]
            hit_fraction = result[2]

            distances.append(hit_fraction * max_dist)

        return distances

    # ------------------------------------------------
    # Add lidar results to occupancy grid
    # ------------------------------------------------
    def update_map(self, lidar_ranges):
        for i, r in enumerate(lidar_ranges):
            angle = self.yaw + (i / len(lidar_ranges)) * 2*math.pi

            hit_x = self.x + r * math.cos(angle)
            hit_y = self.y + r * math.sin(angle)

            gx = int((hit_x + 10) / self.map_resolution)
            gy = int((hit_y + 10) / self.map_resolution)

            if 0 <= gx < self.map_size and 0 <= gy < self.map_size:
                self.occupancy_grid[gx][gy] = 1  # mark as occupied

    # ------------------------------------------------
    # Move robot toward a target point
    # ------------------------------------------------
    def move_to(self, target_x, target_y, speed=0.5):
        self.update_odometry()

        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.sqrt(dx*dx + dy*dy)

        if dist < 0.1:
            return True  # reached destination

        target_yaw = math.atan2(dy, dx)

        # Point robot toward target
        yaw_error = target_yaw - self.yaw
        p.applyExternalTorque(self.robot_id, -1, [0,0,yaw_error], p.WORLD_FRAME)

        # Move forward
        p.applyExternalForce(self.robot_id, -1, [math.cos(self.yaw)*speed, math.sin(self.yaw)*speed, 0], [0,0,0], p.WORLD_FRAME)

        return False
import numpy as np

class SLAMNavigator:
    """
    Minimal navigation + target selection module.
    Keeps a list of detected target positions and visits them one-by-one.
    """

    def __init__(self):
        self.targets = []       # world positions to visit
        self.current_idx = 0    # which target are we on?
        self.last_pose = None

    def update(self, detections, drone_pose):
        """
        detections: list of (x1, y1, x2, y2) from perception
        drone_pose: (x, y, z, roll, pitch, yaw)
        """
        self.last_pose = drone_pose

        # Convert each detection to a 3D world coordinate.
        # Here we fake it using pixel center + constant depth.
        for box in detections:
            (x1, y1, x2, y2) = box
            cx = (x1 + x2) / 2.0
            cy = (y1 + y2) / 2.0

            # Placeholder: convert pixel → world by dropping in front of drone.
            # (Assume target 1m ahead)
            wx = drone_pose[0] + 1.0 * np.cos(drone_pose[5])
            wy = drone_pose[1] + 1.0 * np.sin(drone_pose[5])
            wz = drone_pose[2]

            self.targets.append((wx, wy, wz))

    def getNextTarget(self):
        """Return (x, y, z) of the next target, or None if none left."""
        if self.current_idx >= len(self.targets):
            return None  # nothing left to visit
        return self.targets[self.current_idx]

    def stepToward(self, target, drone_pose):
        """
        Compute a simple velocity command that drives the drone toward target.
        Returns (vx, vy, vz, yaw_rate)
        """
        if target is None or drone_pose is None:
            return 0, 0, 0, 0

        x, y, z, _, _, yaw = drone_pose
        tx, ty, tz = target

        # Position error
        ex = tx - x
        ey = ty - y
        ez = tz - z

        # Proportional controller
        k = 0.5
        vx = k * ex
        vy = k * ey
        vz = k * ez

        # Yaw: point toward target
        desired_yaw = np.arctan2(ey, ex)
        yaw_err = desired_yaw - yaw
        yaw_rate = 0.5 * yaw_err

        # Check if we are "close enough"
        if np.linalg.norm([ex, ey, ez]) < 0.2:
            self.current_idx += 1  # move to next target

        return vx, vy, vz, yaw_rate
