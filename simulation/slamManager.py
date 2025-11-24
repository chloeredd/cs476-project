import orbslam2
import numpy as np 
import cv2
import os 

class SLAMManager:

    '''
    Wrapper around ORB-SLAM2.
    It receives frames from the simulation camera
    and updates drone pose.
    '''

    def __init__(self):

        #Path to ORB-SLAM2 vocab file
        vocab = "assets/slam/ORBvoc.txt"
        settings = "assets/slam/camera.yaml" 

        #If files don't exist, create placeholders
        #so ORB-SLAM2 still loads
        if not os.path.exists(vocab):
            os.makedirs(os.path.dirname(vocab), exist_ok = True)
            open(vocab, "w").close()
        
        if not os.path.exists(settings):
            os.makedirs(os.path.dirname(settings), exist_ok = True)
            with open(settings, "w") as f:
                f.write("%YAML:1.0\n")

        #Initialize SLAM system 
        self.slam = orbslam2.System(
            vocab, 
            settings, 
            orbslam2.Sensor.MONOCULAR
        )

        self.slam.initialize()
        print("SLAM initialized")

    def processFrame(self, frame):

        '''
        Feed a frame to SLAM. ORB-SLAM2 
        expects grayscale images
        '''

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        pose = self.slam.track_monocular(gray, 0.0)
        return pose 

    def shutdown(self):
        self.slam.shutdown()
        
