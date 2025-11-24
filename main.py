from simulation.environment import SimulationEnvironment
from perception.detector import NeedleDetector
from simulation.navigation import SLAMNavigator
import time
import pybullet as p
import numpy as np

def main():
    
    #Create the simulation world (drone, needles, camera, physics, 
    #etc.)
    environment = SimulationEnvironment()

    
    #Initialize detector with syringe body IDs
    try:
        detector = NeedleDetector([s.body for s in environment.syringes])
    #Model cannot be found. Disable perception for now
    except FileNotFoundError:
        detector = None

    navigator = SLAMNavigator(environment.drone)

    try:

        while True: 

            #Update drone pose
            navigator.updatePose()

            #Get the RGB camera image and segmentation mask (perfect
            #object ID mask from PyBullet)

            rgbFrame, segMask = environment.camera.getFrame()

            #Detector works on the (rgb, mask) tuple
            detections = detector.detect((rgbFrame, segMask))

            #Print detections if any are found
            if detections:
                print(f"Detected {len(detections)} syringes")

                #Print bounding boxes and object IDs
                for detection in detections:

                    syringeID = detection["id"]

                    #Convert bounding box center to world coordinates
                    syringeBody = next((s for s in environment.syringes if s.body == syringeID), None)

                    if syringeBody:
                        position = p.getBasePositionAndOrientation(syringeBody)[0]
                        navigator.addSyringeTarget(position, syringeID)

                    print(f"Needle ID {detection['id']} at box {detection['box']}")

                #Drop a marker below the drone
                #This simulates a marking action
                environment.drone.dropMarker()

            
            #Move toward the next target
            targetInfo = navigator.getNextTarget()
            if targetInfo:

                targetPosition, syringeID = targetInfo 
                #Move drone to the syringe
                p.resetBasePositionAndOrientation(environment.drone.body, targetPosition, [0, 0, 0, 1])

                #Drop marker
                environment.drone.dropMarker()
                navigator.markVisited(syringeID)


            #Advance to the next step
            environment.step()

            #sleep for a short period of time
            time.sleep(environment.time_step)

        print("All syringes have been visited. Shutting down the simulation")


    #End the simulation if the user uses ctrl+C
    except KeyboardInterrupt:
        print("Shutting down simulation")

    finally:
        environment.shutdown()
    

if __name__ == "__main__":
    main()
