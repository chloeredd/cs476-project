import torch
import torchvision.transforms as T
from perception.model_loader import loadModel
import yaml
import numpy as np
import os

class NeedleDetector:
    '''
    Wraps a Faster R-CNN style model.
    Given a camera frame, returns bouding boxes for objects of interest
    '''

    def __init__(self, syringeIDs):
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
        self.syringeIDs = set(syringeIDs)

        #Load yaml configuration
        with open("configs/simulation_config.yaml") as f:
            config = yaml.safe_load(f)

        modelPath = config["model"]["detector_path"]

        #Set device (GPU is preferred)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        #Try loading Faster R-CNN
        try:
            if modelPath and os.path.exists(modelPath):
                self.model = loadModel(modelPath, self.device)
                self.useModel = True
                print(f"Faster R-CNN loaded on {self.device}")
            else:
                raise FileNotFoundError
            
        except:
            print("Faster R-CNN not found. Using segmentation-mask instead")
            self.model = None
            self.useModel = False
             
        self.transform = T.ToTensor()


    def detect(self, rgbAndMask):

        #Unpack the rgb and mask tuple
        rgb, mask = rgbAndMask

        #Case 1: using Faster R-CNN
        if self.useModel:
            inputTensor = self.transform(rgb).unsqueeze(0).to(self.device)
            with torch.no_grad():
                outputs = self.model([inputTensor])

            detections = []
            for i in range(len(outputs[0]['boxes'])):
                score = outputs[0]['scores'][i].item()
                if score > 0.5:
                    box = outputs[0]['boxes'][i].detach().cpu().numpy().astype(int).tolist()
                    detections.append({"id": i, "box": box, "score": score})
            return detections

        #Case 2: using segmentation mask
        
        #Set of detections
        detections = []

        #Find all unique object IDs in the segmentation mask
        uniqueIDs = set(mask.flatten())
        
        #Remove 0, which is "background"
        if 0 in uniqueIDs:
            uniqueIDs.remove(0)

        valid_objects = []

        #Only keep the IDs that correspond to syringes
        #uniqueIDs = uniqueIDs.intersection(self.syringeIDs)

        validIDs = [obj for obj in uniqueIDs if obj in self.syringeIDs]

        #If the only objects in the scene are needles, each 
        #unique ID = one needle
        for objID in validIDs:

            #Find (y, x) coordinates of every pixel representing this
            #object
            ys, xs = np.where(mask == objID)

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
                "id" : int(objID),
                "box": [int(left), int(top), int(right), int(bottom)],
                #1.0 is perfect confidence
                #we can say that we have perfect confidence because 
                #segmentation is ground truth
                "score": 1.0
            })

        return detections
