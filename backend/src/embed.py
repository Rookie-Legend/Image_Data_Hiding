import numpy as np
from .prediction_ee import predict_pixel, embed_bit, can_embed

def embed_message(img: np.ndarray, positions: list, bits: np.ndarray):
    stego = img.copy()
    location_map = []
    bit_idx = 0

    for (i, j) in positions:
        if bit_idx >= len(bits):
            break

        p = predict_pixel(stego, i, j)
        stego[i, j] = embed_bit(stego[i, j], p, bits[bit_idx])
        location_map.append(1)
        bit_idx += 1

    return stego, np.array(location_map), bit_idx
