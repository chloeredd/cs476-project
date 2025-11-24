from simulation.environment import SimulationEnvironment
from perception.detector import NeedleDetector
import time
import pybullet as p

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

    try:

        while True: 

            pose = environment.slam.processFrame(rgbFrame)
            if pose is not None:
                print()
            #Move drone slightly forward each step
            position = environment.drone.getPosition()
            #Slightly move along the x-axis
            environment.drone.bodyPosition = [position[0] + 0.01, position[1], position[2]]
            p.resetBasePositionAndOrientation(environment.drone.body, environment.drone.bodyPosition, [0, 0, 0, 1])

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
                    print(f"Needle ID {detection['id']} at box {detection['box']}")

                #Drop a marker below the drone
                #This simulates a marking action
                environment.drone.dropMarker()

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
