import os
import json
from PIL import Image
import torch
from torch.utils.data import Dataset

class SyringeDataset(Dataset):
    def __init__(self, root_dir, transforms=None):
        self.root_dir = root_dir
        self.transforms = transforms
        self.imgs = sorted(os.listdir(os.path.join(root_dir, "images")))
        self.anns = sorted(os.listdir(os.path.join(root_dir, "annotations")))

    def __len__(self):
        return len(self.imgs)

    def __getitem__(self, idx):
        img_path = os.path.join(self.root_dir, "images", self.imgs[idx])
        ann_path = os.path.join(self.root_dir, "annotations", self.anns[idx])

        # Load image
        img = Image.open(img_path).convert("RGB")

        # Load annotation
        with open(ann_path, "r") as f:
            ann = json.load(f)

        boxes = torch.as_tensor(ann.get("boxes", []), dtype=torch.float32)
        labels = torch.as_tensor(ann.get("labels", []), dtype=torch.int64)

        # If no boxes exist, skip this sample
        if boxes.shape[0] == 0:
            return None

        target = {
            "boxes": boxes,
            "labels": labels,
            "image_id": torch.tensor([idx])
        }

        if self.transforms:
            img = self.transforms(img)

        return img, target

# Make sure this function is defined **at the bottom of the file**
def collate_fn(batch):
    # Filter out None items (images with no boxes)
    batch = list(filter(lambda x: x is not None, batch))
    return tuple(zip(*batch))
