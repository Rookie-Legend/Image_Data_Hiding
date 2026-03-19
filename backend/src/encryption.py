import numpy as np

def text_to_bits(text: str) -> np.ndarray:
    bits = []
    for ch in text:
        bits.extend([int(b) for b in format(ord(ch), '08b')])
    return np.array(bits, dtype=np.uint8)

def bits_to_text(bits: np.ndarray) -> str:
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        chars.append(chr(int("".join(map(str, byte)), 2)))
    return "".join(chars)

def xor_encrypt(bits: np.ndarray, key: np.ndarray) -> np.ndarray:
    return np.bitwise_xor(bits, key[:len(bits)])

def xor_decrypt(bits: np.ndarray, key: np.ndarray) -> np.ndarray:
    return np.bitwise_xor(bits, key[:len(bits)])

def bits_to_hex(bits: np.ndarray) -> str:
    # Convert bits to packed bytes, then to hex
    byte_array = np.packbits(bits)
    return byte_array.tobytes().hex()

def hex_to_bits(hex_str: str) -> np.ndarray:
    # Convert hex back to bits
    byte_array = bytes.fromhex(hex_str)
    return np.unpackbits(np.frombuffer(byte_array, dtype=np.uint8))
