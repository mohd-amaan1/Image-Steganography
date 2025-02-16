
# **🔒 Image-Based Steganography Tool**  

![Steganography Banner](/img-main.webp)  

**🔍 Hide & Reveal Secret Messages Securely!**  

This tool allows you to **hide confidential messages inside images** using **AES encryption & LSB (Least Significant Bit) steganography**. Perfect for secure communication, data privacy, and digital watermarking!  

---

## **✨ Features**  
✅ **AES-256 Encryption**: Ensures message security before embedding.  
✅ **LSB Steganography**: Hides messages inside images without visible changes.  
✅ **Passcode Protection**: Only the correct password can decrypt the message.  
✅ **Intuitive UI**: Simple drag-and-drop functionality with a modern design.  
✅ **Download & Share**: Securely save and send encrypted images.  

---

## **📸 UI Preview**  

![Demo](/demo.png)  

---

## **🚀 Installation & Setup**  

### **1️⃣ Clone the Repository**  
```sh
git clone https://github.com/mohd-amaan1/image-steganography.git
cd image-steganography
```

### **2️⃣ Install Dependencies**  
```sh
pip install -r requirements.txt
```

### **3️⃣ Run the Application**  
```sh
streamlit run stego.py
```

---

## **🔧 Technologies Used**  

| **Technology**  | **Usage**  |
|----------------|------------|
| **Python** | Core programming language |
| **Streamlit** | Interactive UI framework |
| **OpenCV** | Image processing |
| **PyCrypto** | AES Encryption |
| **NumPy** | Numerical computing |

---

## **📖 How It Works?**  

🔷 **Encoding Process**  
1️⃣ Upload a **PNG image**.  
2️⃣ Enter a **secret message** and **passcode**.  
3️⃣ The tool **encrypts the message** and **hides it inside the image** using LSB.  
4️⃣ Download the **encoded image** & share it securely.  

🔷 **Decoding Process**  
1️⃣ Upload the **encoded image**.  
2️⃣ Enter the correct **passcode**.  
3️⃣ The tool extracts & **decrypts the hidden message**.  

---

## **🛠 Future Enhancements**  

- 🔹 **Support for multiple image formats (JPG, BMP, etc.)**  
- 🔹 **QR Code Steganography for mobile scanning**  
- 🔹 **AI-based Steganalysis Resistance**  

---

## **📜 License**  

This project is **open-source** under the **MIT License**. Feel free to use, modify, and contribute!  

---

## **🤝 Contributing**  

Contributions are **welcome!** If you have ideas, improvements, or bug fixes, feel free to **fork the repo and submit a PR.**  

---

## **💡 Want to Learn More?**  

📌 **Steganography Explained:** [Wikipedia - Steganography](https://en.wikipedia.org/wiki/Steganography)  
📌 **AES Encryption:** [How AES Works](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)  

---

## **🚀 Ready to Secure Your Messages?**  

💻 **Start encoding messages now!**  
```sh
streamlit run stego.py
```  
