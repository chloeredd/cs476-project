import torch

def loadModel(path, device="cpu"):
    """
    Load a PyTorch Faster R-CNN model from disk.
    """
    print(f"[model_loader] Loading model from {path}")
    model = torch.load(path, map_location=device)
    model.to(device)
    model.eval()
    print(f"[model_loader] Model loaded to device: {device}")
    return model
