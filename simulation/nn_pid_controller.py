import pybullet as p
import pybullet_data
import time
import torch
import torch.nn as nn
import numpy as np
from simple_pid import PID
from drone import Drone      # <-- your file
                             # (import path may be simulation.drone)

DT = 1/240.0

# ============================================================
# LOAD YOUR NEURAL NETWORK (.pth)
# ============================================================

class PIDGainNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(6, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 3)    # (Kp, Ki, Kd)
        )

    def forward(self, x):
        return self.model(x)

pid_net = PIDGainNet()
pid_net.load_state_dict(torch.load("pid_model.pth", map_location="cpu"))
pid_net.eval()

# ============================================================
# CONTROLLER
# ============================================================

class NeuralPIDController:
    def __init__(self):
        p.connect(p.GUI)
        p.setGravity(0, 0, -9.8)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())

        # plane + your drone
        p.loadURDF("plane.urdf")
        self.drone = Drone(startPos=[0,0,1])
        self.body = self.drone.body

        self.target_alt = 1.0

        # Dummy PID; NN will override gains each step
        self.alt_pid = PID(0, 0, 0, setpoint=self.target_alt)
        self.alt_pid.output_limits = (0, 20)

    def nn_pid_gains(self, alt, vz):
        err = self.target_alt - alt

        nn_in = torch.tensor([
            alt,
            vz,
            self.target_alt,
            err,
            abs(err),
            time.time() % 100
        ], dtype=torch.float32)

        Kp, Ki, Kd = pid_net(nn_in).detach().numpy()

        # Clip crazy values from the network
        Kp = np.clip(Kp, 0, 200)
        Ki = np.clip(Ki, 0, 20)
        Kd = np.clip(Kd, 0, 200)

        return float(Kp), float(Ki), float(Kd)

    def run(self):
        while True:
            p.stepSimulation()
            time.sleep(DT)

            pos, _ = p.getBasePositionAndOrientation(self.body)
            vel, _ = p.getBaseVelocity(self.body)
            alt = pos[2]
            vz = vel[2]

            # 1. NN computes PID gains
            kp, ki, kd = self.nn_pid_gains(alt, vz)

            # 2. Update PID controller
            self.alt_pid.Kp = kp
            self.alt_pid.Ki = ki
            self.alt_pid.Kd = kd

            # 3. Compute thrust
            thrust = self.alt_pid(alt)

            # 4. Apply thrust straight upward
            p.applyExternalForce(
                self.body,
                -1,
                [0, 0, thrust],
                pos,
                p.WORLD_FRAME
            )

if __name__ == "__main__":
    NeuralPIDController().run()
