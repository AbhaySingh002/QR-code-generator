
import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import numpy as np
from io import BytesIO
import random
import base64

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6:
        return (0, 0, 0)
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def generate_qr_code(url, fill_color="black"):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    fill_color_rgb = hex_to_rgb(fill_color)
    img = qr.make_image(fill_color=fill_color_rgb, back_color="white").convert('RGBA')
    
    return img

def replace_black_with_symbols(qr_img, symbols, symbol_size=10):
    qr_img = qr_img.convert('L')  # Convert to grayscale
    qr_data = np.array(qr_img)

    # Create a new image with white background
    img = Image.new('RGB', qr_img.size, 'white')
    draw = ImageDraw.Draw(img)
    
    # Define the size of the symbol
    font = ImageFont.load_default()
    
    # Draw symbols on the image
    for y in range(0, qr_data.shape[0], symbol_size):
        for x in range(0, qr_data.shape[1], symbol_size):
            if qr_data[y, x] == 0:  # Black pixel in original QR code
                symbol = random.choice(symbols)
                draw.text((x, y), symbol, fill='black', font=font)
    
    return img

def adjust_transparency(image, transparency):
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    alpha = image.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(transparency)
    image.putalpha(alpha)
    return image

def get_image_download_link(img, filename, text):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/png;base64,{img_str}" download="{filename}">{text}</a>'
    return href
