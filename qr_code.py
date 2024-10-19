import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import numpy as np
from io import BytesIO
import random
import base64
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6:
        return (0, 0, 0)
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

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

def generate_qr_codes(urls, fill_color="black"):
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(generate_qr_code, urls, [fill_color] * len(urls)))
    return results

def replace_symbols_in_qr_codes(qr_images, symbols, symbol_size=10):
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(replace_black_with_symbols, qr_images, [symbols] * len(qr_images), [symbol_size] * len(qr_images)))
    return results

def save_image(img, filename):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str  # Here you can implement your logic to save the image or create a download link

def save_images(images, filenames):
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(save_image, img, filename) for img, filename in zip(images, filenames)]
        for future in futures:
            future.result()  # Wait for all to finish

# Example usage
if __name__ == "__main__":
    urls = ["http://example.com", "http://example.org"]  # Add your URLs
    fill_color = "#000000"  # Default black color for QR code
    symbols = ["*", "#", "$", "%"]  # Your symbols

    # Generate QR Codes
    qr_images = generate_qr_codes(urls, fill_color)

    # Replace black pixels with symbols
    customized_images = replace_symbols_in_qr_codes(qr_images, symbols)

    # Save images or generate download links as needed
    filenames = [f"qr_code_{i}.png" for i in range(len(customized_images))]
    for img, filename in zip(customized_images, filenames):
        img.show()  # For demonstration, show the image
        download_link = get_image_download_link(img, filename, f"Download {filename}")
        print(download_link)  # Print download links in the console
