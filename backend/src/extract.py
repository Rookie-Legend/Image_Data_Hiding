import numpy as np
from .prediction_ee import predict_pixel, extract_bit

def extract_message(stego: np.ndarray, positions: list, bit_count: int):
    recovered = stego.copy()
    bits = []
    idx = 0

    for (i, j) in positions:
        if idx >= bit_count:
            break

        p = predict_pixel(recovered, i, j)
        bit, original = extract_bit(recovered[i, j], p)
        bits.append(bit)
        recovered[i, j] = original
        idx += 1

    return np.array(bits), recovered
