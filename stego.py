import streamlit as st
import cv2
import numpy as np
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

def hash_password(password):
    """Hashes the password using SHA-256."""
    return hashlib.sha256(password.encode()).digest()

def encrypt_message(message, password):
    """Encrypts the message using AES encryption."""
    key = hash_password(password)
    cipher = AES.new(key, AES.MODE_CBC)
    encrypted = cipher.encrypt(pad(message.encode(), AES.block_size))
    return base64.b64encode(cipher.iv + encrypted).decode()

def decrypt_message(encrypted_message, password):
    """Decrypts the AES encrypted message."""
    key = hash_password(password)
    data = base64.b64decode(encrypted_message)
    iv = data[:16]
    encrypted = data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    try:
        return unpad(cipher.decrypt(encrypted), AES.block_size).decode()
    except:
        return "Authentication failed! Incorrect passcode."

def encode_message(img, message, password):
    """Encodes an encrypted message into an image using LSB."""
    encrypted_message = encrypt_message(message, password) + "%%"
    binary_message = ''.join(format(ord(c), '08b') for c in encrypted_message)
    img_flat = img.flatten()
    if len(binary_message) > len(img_flat):
        return None, "Message is too long for this image!"
    
    for i in range(len(binary_message)):
        img_flat[i] = (img_flat[i] & 254) | int(binary_message[i])  # ✅ Safe uint8 assignment

    
    img_encoded = img_flat.reshape(img.shape)
    return img_encoded, "Message encrypted successfully!"

def decode_message(img, password):
    """Extracts and decrypts the hidden message from an image."""
    img_flat = img.flatten()
    binary_message = ''.join(str(img_flat[i] & 1) for i in range(len(img_flat)))
    chars = [chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8)]
    extracted_message = ''.join(chars)
    if "%%" not in extracted_message:
        return "No hidden message found."
    extracted_message = extracted_message.split("%%")[0]
    return decrypt_message(extracted_message, password)

# Streamlit UI

# Page Configurations
st.set_page_config(page_title="Steganography Tool", page_icon="🔒", layout="wide")

# Custom CSS for Styling
st.markdown("""
    <style>
    /* Full Page Background */
    body {
        background: linear-gradient(to right, #1e3c72, #2a5298);
        color: white;
    }
    
    /* Title */
    .main-title {
        font-size: 48px;
        font-weight: bold;
        text-align: center;
        color: #ffffff;
        text-shadow: 2px 2px 5px rgba(0,0,0,0.5);
    }

    /* Subtitle */
    .subtitle {
        font-size: 22px;
        text-align: center;
        font-weight: 500;
        color: #ddd;
    }

    /* Sidebar */
    .stSidebar {
        background: #1e3c72;
        color: white;
    }

    /* Refresh Button */
     .reset-container {
        display: flex;
        justify-content: center;
        margin-top: 20px;
    }

    .reset-btn {
        display: flex;
        align-items: center;
        justify-content: center;
        background: #ff6600;
        color: white;
        border-radius: 10px;
        font-size: 18px;
        font-weight: bold;
        padding: 12px 20px;
        width: 100%;
        box-shadow: 3px 3px 8px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
        cursor: pointer;
        border: none;
        outline: none;
    }
    
    .reset-btn:hover {
        background: #ff4500;
        transform: scale(1.05);
    }

    /* Rotating icon animation */
    .reset-icon {
        margin-right: 8px;
        animation: spin 1.5s linear infinite;
        display: inline-block;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    /* Radio Buttons */
    .stRadio label {
        font-size: 20px;
        font-weight: bold;
        color: white;
    }

    /* File Upload Box */
    .uploaded-file {
        background: rgba(255, 255, 255, 0.2);
        padding: 15px;
        border-radius: 10px;
    }

    /* Buttons */
    .stButton > button {
        background: #ff6600;
        color: white;
        border-radius: 10px;
        font-size: 18px;
        font-weight: bold;
        padding: 12px 25px;
        box-shadow: 3px 3px 8px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: #ff4500;
        transform: scale(1.05);
    }
            
    
    
    </style>
""", unsafe_allow_html=True)

# Sidebar for Navigation
with st.sidebar:
    st.markdown("## 🔄 Reset")
    
    # Reset Button with Animation
    if st.button("🔄 Reset", key="reset_button"):
        st.rerun()  # Reloads the page

# Main Title
st.markdown('<h1 class="main-title">🔒 Image-Based Steganography Tool</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Hide & Reveal Secret Messages Securely!</p>', unsafe_allow_html=True)

# UI Layout - Side-by-Side Columns
col1, col2 = st.columns(2)

# Encode Section
with col1:
    st.markdown("## 📤 Encode a Secret Message")
    uploaded_file = st.file_uploader("📁 Upload an Image (PNG only)", type=["png"], key="encode_upload")

    if uploaded_file:
        image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)
        message = st.text_area("📝 Enter Secret Message", help="Your message will be hidden inside the image.")
        password = st.text_input("🔑 Set a Passcode", type="password", help="This passcode is needed for decoding.")

        if st.button("🔐 Encode & Save"):
            encoded_img, status = encode_message(image, message, password)
            if encoded_img is not None:
                cv2.imwrite("encoded_image.png", encoded_img)
                st.success(f"✅ {status}")
                with open("encoded_image.png", "rb") as file:
                    st.download_button("⬇️ Download Encrypted Image", file, "encoded_image.png")
            else:
                st.error(f"❌ {status}")

# Decode Section
with col2:
    st.markdown("## 📥 Decode a Hidden Message")
    uploaded_file = st.file_uploader("📁 Upload Encrypted Image", type=["png"], key="decode_upload")

    if uploaded_file:
        image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)
        password = st.text_input("🔑 Enter Passcode", type="password", key="decode_password")

        if st.button("🔓 Decode Message"):
            decrypted_message = decode_message(image, password)
            if decrypted_message:
                st.success(f"🔍 Decrypted Message: {decrypted_message}")
            else:
                st.error("❌ Incorrect password or no hidden message found.")
