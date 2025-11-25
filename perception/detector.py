import torch
import torchvision
from torchvision.transforms import functional as F

class NeedleDetector:
    def __init__(self, model_path):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Create model architecture
        self.model = torchvision.models.detection.fasterrcnn_resnet50_fpn(
            weights=None,
            num_classes=2
        )

        # Load state_dict from training
        state_dict = torch.load(model_path, map_location=self.device)
        self.model.load_state_dict(state_dict)

        self.model.to(self.device)
        self.model.eval()
        print("[Detector] Model loaded successfully.")

    def detect(self, image):
        """
        image: HxWx3 numpy array
        returns: list of (box, label) tuples
        """
        img_tensor = F.to_tensor(image).to(self.device)
        with torch.no_grad():
            outputs = self.model([img_tensor])

        detections = []
        for box, label in zip(outputs[0]["boxes"], outputs[0]["labels"]):
            detections.append((box.cpu().numpy(), int(label.cpu().item())))
        return detections
