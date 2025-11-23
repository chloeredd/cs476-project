import torch
import torchvision.transforms as T
from perception.model_loader import loadModel
import yaml
import numpy as np

class NeedleDetector:
    '''
    Wraps a Faster R-CNN style model.
    Given a camera frame, returns bouding boxes for objects of interest
    '''

    def __init__(self):
        '''
        #Open the yaml file
        with open("configs/simulation_config.yaml") as f:
            config = yaml.safe_load(f)
        
        modelPath = config["model"]["detector_path"]
        #Determine if we will use cuda or cpu
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        #Load model
        self.model = loadModel(modelPath, self.device)

        #Convert numpy array to PyTorch tensor
        #Faster R-CNN expects tensors in CHW format in [0, 1]
        self.transform = T.Compose([
            T.ToTensor()
        ])
        '''
        #We only needed to print that the NeedleDetector has been 
        #initialized when init is called
        print("NeedleDetector initialized")

    def detect(self, rgbAndMask):

        '''
        Input: rgb and segmentation mask
        
        output: detections
        '''

        #Unpack the rgb and mask tuple
        rgb, mask = rgbAndMask

        #Set of detections
        detections = []

        #Find all unique object IDs in the segmentation mask
        uniqueIDs = set(mask.flatten())
        
        #Remove 0, which is "background"
        if 0 in uniqueIDs:
            uniqueIDs.remove(0)

        #If the only objects in the scene are needles, each 
        #unique ID = one needle
        for uniqueID in uniqueIDs:

            #Find (y, x) coordinates of every pixel representing this
            #object
            ys, xs = np.where(mask == uniqueID)

            #If the object isn't visible, skip it
            if len(xs) == 0:
                continue

            #Create a bounding box
            #left = min(x)
            #right = max(x)
            #top = min(y)
            #bottom = max(y)

            left, right = xs.min(), xs.max()
            top, bottom = ys.min(), ys.max()

            #Save the detection
            detections.append({
                "id" : int(uniqueID),
                "box": [int(left), int(top), int(right), int(bottom)],
                #1.0 is perfect confidence
                #we can say that we have perfect confidence because 
                #segmentation is ground truth
                "score": 1.0
            })

        return detections