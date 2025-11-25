import torch

sd = torch.load("faster_rcnn_syringe.pth", weights_only=False)
print(type(sd))
print(len(sd.keys()))
print(list(sd.keys())[:10])
