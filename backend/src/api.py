from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
import numpy as np
import cv2
import tempfile
import os
from fastapi.middleware.cors import CORSMiddleware
from .io_utils import load_grayscale
from .interpolation import downscale, upscale, get_interpolated_positions
from .encryption import text_to_bits, bits_to_text, xor_encrypt, xor_decrypt, bits_to_hex, hex_to_bits
from .embed import embed_message
from .extract import extract_message

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Secret-Key"],
)

@app.post("/embed")
async def embed_image(
    image: UploadFile = File(...),
    secret: str = Form(...)
):
    temp_path = f"temp_{image.filename}"
    with open(temp_path, "wb") as f:
        f.write(await image.read())

    img = load_grayscale(temp_path)
    # Global compression: Shift image to [1, 254] to ensure absolute steganographic room
    # for all pixels. This removes the need for complex skip logic.
    img = np.clip(img, 1, 254).astype(np.uint8)
    positions = get_interpolated_positions(img.shape)

    # Magic header + bits
    magic = [1,0,1,0,1,0,1,0]
    bits = np.concatenate([magic, text_to_bits(secret)])

    key = np.random.randint(0, 2, size=len(bits) + 1000)
    enc_bits = xor_encrypt(bits, key)

    stego, _, used = embed_message(img, positions, enc_bits)

    stego_path = f"stego_{image.filename}"
    from .io_utils import save_image
    save_image(stego_path, stego)

    # INTERNAL VERIFICATION TEST
    test_stego = load_grayscale(stego_path)
    test_bits, _ = extract_message(test_stego, positions, len(enc_bits))
    test_dec = xor_decrypt(test_bits, key)
    # Strip magic header for test comparison
    test_msg = bits_to_text(test_dec[8:])
    print(f"INTERNAL TEST: Original msg: '{secret}', Recovered msg: '{test_msg}'")
    if secret == test_msg:
        print("INTERNAL TEST PASSED!")
    else:
        print("INTERNAL TEST FAILED! Data corruption detected.")

    os.remove(temp_path)

    # Save key as hex to avoid truncation issues
    key_str = bits_to_hex(key[:used])

    return FileResponse(
        stego_path,
        media_type="image/png",
        filename=f"stego_{image.filename}",
        headers={
            "X-Secret-Key": key_str
        }
    )


@app.post("/extract")
async def extract_image(
    image: UploadFile = File(...),
    key: str = Form(...)
):
    temp_path = f"temp_{image.filename}"
    with open(temp_path, "wb") as f:
        f.write(await image.read())

    stego = load_grayscale(temp_path)
    positions = get_interpolated_positions(stego.shape)

    if not key or key.lower() == "null":
        return {"error": "Invalid secret key provided."}
    
    try:
        key_bits = hex_to_bits(key)
    except Exception:
        return {"error": "Invalid secret key format (must be a hex string)."}

    extracted_bits, _ = extract_message(
        stego,
        positions,
        len(key_bits)
    )

    dec_bits = xor_decrypt(extracted_bits, key_bits)
    
    # Check for magic header [1,0,1,0,1,0,1,0]
    magic = dec_bits[:8].tolist()
    if magic != [1,0,1,0,1,0,1,0]:
        print(f"EXTRACTION FAIL: Magic header mismatch. Got {magic}")
        # Note: We still proceed to show what we got, but this helps debugging
    
    message = bits_to_text(dec_bits[8:])

    os.remove(temp_path)

    return {
        "recovered_message": message
    }
