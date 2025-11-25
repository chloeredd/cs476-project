import os
import json
import numpy as np
from PIL import Image

# Settings
dataset_dir = "dataset"
splits = ["train", "val", "test"]
num_images_per_split = 5
image_size = (128, 128)  # width, height
num_objects_per_image = 1  # how many "syringes" per image

# Make dataset folders
for split in splits:
    images_path = os.path.join(dataset_dir, split, "images")
    ann_path = os.path.join(dataset_dir, split, "annotations")
    os.makedirs(images_path, exist_ok=True)
    os.makedirs(ann_path, exist_ok=True)

    # Generate dummy images and annotations
    for i in range(num_images_per_split):
        # Create a random image
        img_array = np.random.randint(0, 256, (image_size[1], image_size[0], 3), dtype=np.uint8)
        img = Image.fromarray(img_array)
        img_filename = f"img_{i+1}.jpg"
        img.save(os.path.join(images_path, img_filename))

        # Generate dummy bounding box coordinates
        boxes = []
        labels = []
        for _ in range(num_objects_per_image):
            x1 = np.random.randint(0, image_size[0]//2)
            y1 = np.random.randint(0, image_size[1]//2)
            x2 = np.random.randint(image_size[0]//2, image_size[0])
            y2 = np.random.randint(image_size[1]//2, image_size[1])
            boxes.append([x1, y1, x2, y2])
            labels.append(1)  # class 1 = syringe

        # Save annotation as JSON
        ann_filename = f"img_{i+1}.json"
        ann_data = {"boxes": boxes, "labels": labels}
        with open(os.path.join(ann_path, ann_filename), "w") as f:
            json.dump(ann_data, f)

print("Dummy dataset created successfully!")
