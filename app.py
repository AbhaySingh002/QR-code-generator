from io import BytesIO
import streamlit as st
import base64
from qr_code import generate_qr_code, replace_black_with_symbols, adjust_transparency, get_image_download_link
from PIL import Image
import warnings
warnings.filterwarnings('ignore')

def main():
    # Load and set the background image
    with open("samurai-rabbit-katana-illustration-jl-3840x2160.jpg", "rb") as image_file:
        image_bytes = image_file.read()
    encoded_image = base64.b64encode(image_bytes).decode()

    # Set the background image
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded_image}");
            background-size: cover;
        }}
        .title-text {{
            color: black;
            font-size: 4em;
        }}
        /* Change the label color of the text input to black */
        label {{
            color: black;
            font-size: 1.5em;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    
    st.markdown('<h1 class="title-text">QR Code Generator with Customization</h1>', unsafe_allow_html=True)

    url = st.text_input("Enter the URL to generate QR code:")
    if st.checkbox("Customize QR Code Color"):
        fill_color = st.color_picker("Choose the QR code color:", "#000000")
        if st.button("Generate QR Code with Color"):
            if url:
                qr_img = generate_qr_code(url, fill_color)
                st.image(qr_img, caption='Generated QR Code', use_column_width=True)
                download_link = get_image_download_link(qr_img, "qr_code_colored.png", "Download QR Code with Color")
                st.markdown(download_link, unsafe_allow_html=True)
            else:
                st.error("Please enter a URL")

    if st.checkbox("Customize QR Code Symbols"):
        symbols = st.text_input("Enter symbols to replace the black parts of the QR code (multiple symbols allowed):")
        symbol_size = 6

        if st.button("Generate QR Code with Symbols"):
            if url:
                qr_img = generate_qr_code(url)  # Generate the QR code without color customization
                if symbols:
                    qr_img = replace_black_with_symbols(qr_img, symbols, symbol_size)
                st.image(qr_img, caption='Generated QR Code with Symbols', use_column_width=True)
                download_link = get_image_download_link(qr_img, "qr_code_symbols.png", "Download QR Code with Symbols")
                st.markdown(download_link, unsafe_allow_html=True)
            else:
                st.error("Please enter a URL")

    # Option for embedding QR Code into a background image
    if st.checkbox("Embed QR Code into Background Image"):
        uploaded_bg = st.file_uploader("Upload a background image (PNG format):", type=["png"])
        qr_transparency = st.slider("Adjust QR Code Transparency", 0.0, 1.0, 1.0)
        bg_transparency = st.slider("Adjust Background Image Transparency", 0.0, 1.0, 1.0)

        if st.button("Generate QR Code with Background"):
            if url:
                qr_img = generate_qr_code(url)
                qr_img = adjust_transparency(qr_img, qr_transparency)

                if uploaded_bg:
                    bg_img = Image.open(uploaded_bg).convert('RGBA')
                    bg_img = adjust_transparency(bg_img, bg_transparency)
                    qr_img = qr_img.resize((bg_img.width, bg_img.height), Image.Resampling.LANCZOS)

                    buffered = BytesIO()
                    qr_img.save(buffered, format="PNG")
                    qr_img_str = base64.b64encode(buffered.getvalue()).decode()

                    bg_img_buffered = BytesIO()
                    bg_img.save(bg_img_buffered, format="PNG")
                    bg_img_str = base64.b64encode(bg_img_buffered.getvalue()).decode()

                    st.markdown(
                        f"""
                        <div style="position: relative; display: inline-block;">
                            <img src="data:image/png;base64,{bg_img_str}" style="width: 100%; height: auto;">
                            <img src="data:image/png;base64,{qr_img_str}" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; mix-blend-mode: multiply;">
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    download_link = get_image_download_link(qr_img, "qr_code_with_bg.png", "Download QR Code with Background")
                    st.markdown(download_link, unsafe_allow_html=True)
                else:
                    st.error("Please upload a background image")
            else:
                st.error("Please enter a URL")

if __name__ == "__main__":
    main()
