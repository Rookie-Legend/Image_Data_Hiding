import cv2
import numpy as np

def downscale(img: np.ndarray, factor: int = 2) -> np.ndarray:
    return img[::factor, ::factor]

def upscale(img: np.ndarray, target_shape: tuple) -> np.ndarray:
    return cv2.resize(img, (target_shape[1], target_shape[0]), interpolation=cv2.INTER_LINEAR)

def get_interpolated_positions(shape: tuple):
    """
    Returns list of (i, j) for interpolated pixels
    Beacuse we down scale by 2 original pixels surivive at even-even positions
    """
    h, w = shape
    positions = []
    for i in range(h):
        for j in range(w):
            if i % 2 != 0 or j % 2 != 0:
                positions.append((i, j))
    return positions
