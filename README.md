# Project Football Player Detection With YOLOv8 Flask

Repositori ini berisi kode sumber untuk aplikasi web deteksi pemain sepak bola.

## ⚠️ PENTING: Prasyarat Model

File model (`yolov8.pt`, 133MB) **tidak** disimpan di repositori ini karena ukurannya yang besar.

1.  Unduh file model secara manual dari grup WA atau link gdrive berikut: **[https://drive.google.com/file/d/1EwtND3MKokHkPo-zhE6Y8cFnGpJC0GCN/view?usp=sharing]**
2.  Tempatkan file `yolov8.pt` yang sudah diunduh ke dalam folder `Model/`.

## Instruksi Setup

1.  Clone repositori ini.
2.  Buat virtual environment: `python -m venv venv`
3.  Aktifkan environment: `.\venv\Scripts\activate`
4.  Install semua library: `pip install -r requirements.txt`
5.  Jalankan aplikasi (pastikan Anda berada di folder `Project`):
    ```bash
    cd Project
    python app.py
    ```