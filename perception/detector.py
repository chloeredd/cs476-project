import torch
import torchvision.transforms as T
from perception.model_loader import loadModel
import yaml

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

    def detect(self, frame):

        return []

        '''
        Runs inference on a single RGB frame
        '''

        image = self.transform(frame).to(self.device)

        with torch.no_grad():
            outputs = self.model([image])[0]
        
        #Parse the results
        detections = []
        for box, score, label in zip(outputs["boxes"], outputs["scores"], outputs["labels"]):
            if score > 0.7:
                detections.append(
                    {
                        "box": box.tolist(),
                        "score": float(score),
                        "label": int(label)
                    }
                )

        return detections
