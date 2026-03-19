import numpy as np
import math

def mse(a: np.ndarray, b: np.ndarray) -> float:
    return np.mean((a.astype(float) - b.astype(float)) ** 2)

def psnr(a: np.ndarray, b: np.ndarray) -> float:
    m = mse(a, b)
    if m == 0:
        return float('inf')
    return 20 * math.log10(255.0 / math.sqrt(m))
