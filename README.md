# 📷✨ EXIF Metadata Editor ✨📷

A modern and intuitive web application designed to help you view, edit, and save EXIF (Exchangeable Image File Format) metadata for your images. Easily modify details like date, time, GPS coordinates, and camera information, then save the updated data directly back to the image file.

---

## 🌟 Features

*   🖼️ **Image Upload:** Simple drag-and-drop or file selection for image uploads.
*   📊 **EXIF Viewing:** Clearly displays existing EXIF metadata.
*   ✏️ **Metadata Editing:** Modify various EXIF tags including:
    *   📅 Date & Time (DateTimeOriginal, DateTime, DateTimeDigitized)
    *   📍 GPS Location (Latitude, Longitude)
    *   📸 Camera Information (Make, Model)
*   🗺️ **Interactive Map:** Visual map interface (using Leaflet.js) for viewing and setting GPS coordinates.
*   🎨 **Modern UI:** Sleek interface built with Tailwind CSS.
*   🌗 **Dark/Light Mode:** Toggle between themes for comfortable viewing.
*   📱 **Responsive Design:** Adapts seamlessly to desktop and mobile devices.

---

## ⚙️ Technology Stack

*   **Backend:** 🐍 Python (Flask)
*   **Image Processing:** 🖼️ Pillow (PIL Fork)
*   **Frontend:** 🎨 Tailwind CSS, Alpine.js
*   **Maps:** 🗺️ Leaflet.js

---

## 🚀 Getting Started

Follow these instructions to get the project up and running on your local machine.

### Prerequisites

*   Python 3.7+ installed
*   `pip` (Python package installer)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/justpeder1/Exif-Metadata-Editor
    cd exif-metadata-editor
    ```

2.  **Create and activate a virtual environment** (Recommended):

    *   On Windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    *   On macOS/Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Create a `.env` file in the project root and add your secret key:
    ```
    SECRET_KEY='your-super-secret-key-here'
    FLASK_DEBUG=True # Optional: for development mode
    ```
    *Replace `'your-super-secret-key-here'` with a strong, unique secret key.* 

### Running the Application

1.  **Start the Flask development server:**
    ```bash
    flask run
    ```
    *(If `flask run` doesn't work, you might need to use `python app.py` depending on your setup).* 

2.  **Access the application:**
    Open your web browser and navigate to:
    [`http://127.0.0.1:5000/`](http://127.0.0.1:5000/)

---

## 🖱️ How to Use

1.  **Upload:** Drag & drop an image onto the designated area or click "Dosya Seç" (Select File).
2.  **View:** EXIF data will be automatically extracted and displayed across different tabs (Basic Info, Date & Time, Location, Camera).
3.  **Edit:** Click "Metadata Düzenle" (Edit Metadata).
4.  **Modify:** Make changes in the input fields or click on the map to set a location.
5.  **Save:** Click "Değişiklikleri Kaydet" (Save Changes) to apply the modifications to the image file's metadata.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues to improve the application.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details (if one exists, otherwise specify license type). 
