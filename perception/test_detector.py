import torch
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from torchvision.transforms import functional as F
from PIL import Image
import os

# Path to your trained model
MODEL_PATH = "faster_rcnn_syringe.pth"

# Sample test image
TEST_IMAGE = "dataset/test/images/img_1.jpg"

# Load the trained Faster R-CNN model
def load_model(model_path):
    model = fasterrcnn_resnet50_fpn(pretrained=False)
    # Adjust number of classes: background + syringe = 2
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes=2)
    model.load_state_dict(torch.load(model_path))
    model.eval()
    return model

def detect_syringes(model, image_path):
    image = Image.open(image_path).convert("RGB")
    image_tensor = F.to_tensor(image).unsqueeze(0)  # add batch dimension

    with torch.no_grad():
        outputs = model(image_tensor)

    boxes = outputs[0]['boxes']
    scores = outputs[0]['scores']
    labels = outputs[0]['labels']

    print(f"Detected {len(boxes)} syringe(s) in {image_path}")
    for i, box in enumerate(boxes):
        if scores[i] > 0.5:  # confidence threshold
            print(f"Box: {box.tolist()}, Score: {scores[i].item()}, Label: {labels[i].item()}")

if __name__ == "__main__":
    if not os.path.exists(TEST_IMAGE):
        print(f"Test image not found at {TEST_IMAGE}")
    else:
        model = load_model(MODEL_PATH)
        detect_syringes(model, TEST_IMAGE)
