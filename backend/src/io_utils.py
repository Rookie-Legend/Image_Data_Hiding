import cv2
import numpy as np

def load_grayscale(path: str) -> np.ndarray:
    # Load as grayscale directly
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("Image not found or invalid format")
    return img

def save_image(path: str, img: np.ndarray):
    # Save as 3-channel BGR where all channels are equal for maximum compatibility
    color_img = cv2.merge([img, img, img])
    cv2.imwrite(path, color_img)
