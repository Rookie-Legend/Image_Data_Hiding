import numpy as np

def predict_pixel(img: np.ndarray, i: int, j: int) -> int:
    h, w = img.shape
    # Pick the nearest top-left even-even pixel. 
    # This is 100% stable and exists for all positions in the list.
    ni, nj = i - (i % 2), j - (j % 2)
    return int(img[ni, nj])

def can_embed(p: int, e: int) -> bool:
    x_prime = int(p) + (2 * int(e))
    return 0 <= x_prime <= 255

def embed_bit(x: int, p: int, bit: int):
    # LSB on Prediction Error: x' = p + ((x - p) & ~1 | bit)
    e = int(x) - int(p)
    e_prime = (e & ~1) | int(bit)
    return int(p) + e_prime

def extract_bit(x_prime: int, p: int):
    # LSB on Prediction Error: bit = (x' - p) % 2
    e_prime = int(x_prime) - int(p)
    bit = int(e_prime % 2)
    # Recover original pixel (p + original_error)
    # Since e_prime = (e & ~1) | bit, original_error is hard to get back exactly
    # but we only care about the bit for message recovery!
    return bit, x_prime
