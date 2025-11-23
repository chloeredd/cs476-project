from simulation.environment import SimulationEnvironment
from perception.detector import NeedleDetector
import time

def main():
    
    #Create the simulation world (drone, needles, camera, physics, 
    #etc.)
    environment = SimulationEnvironment()

    
    #Load the ML model (Faster R-CNN) if it exists
    try:
        detector = NeedleDetector()
    #Model cannot be found. Disable perception for now
    except FileNotFoundError:
        detector = None

    try:
    

        #Main loop
        
        '''
        while True:

            #Capture image from drone's camera
            frame = environment.camera.getFrame()

            #Run object detection
            detections = detector.detect(frame) if detector else []

            #Needles have been detected
            if detections:
                print(f"Found {len(detections)} potential needles")
            
                #Drop marker
                environment.drone.dropMarker()
            
            #Advance the physics simulation 
            environment.step()

            #Sleep for a short amount of time
            time.sleep(environment.time_step)
        '''

        for step in range(10):
            frame = environment.camera.getFrame()

            if detector:
                detections = detector.detect(frame)
            else:
                detections = [{}]

            if detections:
                environment.drone.dropMarker()
                print(f"Step {step}: Marker dropped at drone position")

            environment.step()
            time.sleep(environment.time_step)

        print("Test loop completed. Shutting down simulation")


    #End the simulation if the user uses ctrl+C
    except KeyboardInterrupt:
        print("Shutting down simulation")

    finally:
        environment.shutdown()
    

if __name__ == "__main__":
    main()
