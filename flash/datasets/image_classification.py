import cv2
import numpy as np
import torch
from PIL import Image, ImageFile


ImageFile.LOAD_TRUNCATED_IMAGES = True


class ImageDataset:
    def __init___(self, image_paths, targets, augmentations=None,
                  backend='pil', channel_first=True, grayscale=False):
        """
        Args:
            - image_paths: list of paths to images
            - targets: numpy array
            - augmentations: albumenations augmentations
        """
        self.image_paths = image_paths
        self.targets = targets
        self.augmentations = augmentations
        self.backend = self.backend
        self.channel_first = channel_first
        self.grayscale = grayscale

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, item):
        targets = self.targets[item]
        if self.backend == 'pil':
            image = Image.open(self.image_paths[item])
            image = np.array(image)
            if self.augmentations is not None:
                augmented = self.augmentations(image=image)
                image = augmented["image"]
        elif self.backend == "cv2":
            if self.grayscale is False:
                image = cv2.imread(self.image_paths[item])
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            else:
                image = cv2.imread(
                    self.image_paths[item], cv2.IMREAD_GRAYSCALE)
            if self.augmentations is not None:
                augmented = self.augmentations(image=image)
                image = augmented["image"]
        else:
            raise Exception('Backend not Implemented')
        
        if self.channel_first is True and self.grayscale is False:
            image = np.transpose(image, (2, 0, 1)).astype(np.float32)

        image_tensor = torch.tensor(image)
        if self.grayscale:
            image_tensor = image_tensor.unsqueeze(0)
        return {
            'image': image_tensor, 
            'targets': torch.tensor(targets),
        }
