from typing import Union

import cv2
import numpy as np
from PIL import Image

from src.service.image_service import ImageService

if __name__ == '__main__':

    image1: Union[Image.Image, np.ndarray] = Image.open('D://a.png')
    image2: Union[Image.Image, np.ndarray] = Image.open('D://d.png')

    print(ImageService.cv2_confidence(image1,image2))
