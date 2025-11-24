import torch

def loadModel(path, device="cpu"):
    '''
    Load a PyTorch model from disk.
    This project separates loading from inference for the sake of
    organization
    '''

    print(f"Loading model from {path}")

    #MapLocation lets model load onto CPU even if trained on GPU
    model = torch.load(path, map_location = device)
    model.to(device)
    model.eval()

    print(f"Model loaded to device: {device}")

    return model

