import torch
from torchvision.models.detection import fasterrcnn_resnet50_fpn

#Create a COCO-pretrained Faster R-CNN model
model = fasterrcnn_resnet50_fpn(weights = "DEFAULT")

#Save to assets folder
torch.save(model, "assets/models/faster_rcnn_syringe.pth")
