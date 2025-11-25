import pybullet as p
import time
from simulation.environment import SimulationEnvironment
from simulation.slamManager import slamManager
from perception.detector import NeedleDetector
from simulation.marker import drop_marker

def main():
    print("[main] Starting simulation")

    # Initialize full environment (drone, syringes, distractions)
    env = SimulationEnvironment()
    drone_id = env.drone.drone_id  # assume Drone class has drone_id attribute
    slam = slamManager(drone_id)

    # Load detector
    cfg_detector_path = "faster_rcnn_syringe.pth"
    print(f"[main] LOADING DETECTOR FROM: {cfg_detector_path}")
    detector = NeedleDetector(cfg_detector_path)
    print("[main] Entering main loop. Press Ctrl+C to stop early.")

    try:
        while True:
            # 1. Get camera frame
            rgb_image = slam.get_camera_frame()  # HxWx3 numpy array

            # 2. Detect syringes
            detections = detector.detect(rgb_image)
            print(f"[main] Detected {len(detections)} candidate(s)")

            # 3. Move drone and drop markers
            for box, label in detections:
                if label == 1:  # syringe
                    x, y, z = slam.convert_box_to_world(box)
                    slam.move_to(x, y, z + 0.05)
                    drop_marker(x, y, z)

            # 4. Step simulation
            env.step()

    except KeyboardInterrupt:
        print("[main] Simulation stopped by user")

    finally:
        env.shutdown()
        print("[main] Environment shutdown complete")

if __name__ == "__main__":
    main()
