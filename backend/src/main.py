from .io_utils import load_grayscale, save_image
from .interpolation import downscale, upscale, get_interpolated_positions
from .encryption import text_to_bits, bits_to_text, xor_encrypt, xor_decrypt
from .embed import embed_message
from .extract import extract_message
from .metrics import psnr
import numpy as np

def main():
    img = load_grayscale("./data/lucy.jpg")

    low = downscale(img)
    interp = upscale(low, img.shape)

    positions = get_interpolated_positions(img.shape)

    secret = "HELLO RDH"
    bits = text_to_bits(secret)

    key = np.random.randint(0, 2, size=10000)
    enc_bits = xor_encrypt(bits, key)

    stego, loc_map, used = embed_message(interp, positions, enc_bits)

    extracted_bits, recovered = extract_message(stego, positions, used)
    dec_bits = xor_decrypt(extracted_bits, key)

    recovered_text = bits_to_text(dec_bits)

    print("Recovered text:", recovered_text)
    print("PSNR:", psnr(interp, stego))

if __name__ == "__main__":
    main()
