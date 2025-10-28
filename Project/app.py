from flask import Flask, render_template, request, url_for
from ultralytics import YOLO
from PIL import Image
import os
import shutil
import time
import uuid

app = Flask(__name__)

# Model YOLO
model = YOLO("yolov8x.pt")

# Folder untuk upload dan hasil
UPLOAD_FOLDER = "static/uploads"
RESULT_FOLDER = "static/results"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["RESULT_FOLDER"] = RESULT_FOLDER


@app.route("/", methods=["GET", "POST"])
def index():
    result_img = None
    upload_img = None
    error_msg = None  # Variabel untuk pesan error

    if request.method == "POST":
        file = request.files.get("file")

        if not file or file.filename == "":
            error_msg = "No file uploaded. Please select a file."
            return render_template("index.html", error_msg=error_msg)

        try:
            # 1. Buat nama file unik
            filename = f"{uuid.uuid4()}_{file.filename}"
            
            # 2. Simpan file yang diupload
            upload_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(upload_path)
            upload_img = url_for("static", filename=f"uploads/{filename}")
            print(f"✅ [DEBUG] File saved to: {upload_path}")
            print(f"✅ [DEBUG] Upload Img URL: {upload_img}")

            # 3. Jalankan Prediksi
            print(f"⏳ [DEBUG] Running prediction on: {upload_path}")
            results = model.predict(
                source=upload_path, 
                save=True, 
                project="runs", 
                name="detect", 
                exist_ok=True,
                classes=0  # INGAT: Ini HANYA mendeteksi 'person'
            )
            
            # 4. Tentukan path hasil
            # results[0].save_dir akan menjadi sesuatu seperti 'runs/detect'
            detected_img_path = os.path.join(results[0].save_dir, filename)
            print(f"ℹ️ [DEBUG] Predicted save_dir: {results[0].save_dir}")
            print(f"ℹ️ [DEBUG] Expecting result file at: {detected_img_path}")

            # 5. Cek apakah file hasil benar-benar ada
            if os.path.exists(detected_img_path):
                print(f"👍 [DEBUG] SUCCESS! Result file found.")
                
                # 6. Salin ke folder static/results
                output_path = os.path.join(app.config["RESULT_FOLDER"], filename)
                shutil.copy(detected_img_path, output_path)
                print(f"✅ [DEBUG] File copied to: {output_path}")

                # 7. Buat URL untuk HTML (dengan cache-buster)
                timestamp = int(time.time())
                result_img = url_for("static", filename=f"results/{filename}", t=timestamp)
                print(f"✅ [DEBUG] Result Img URL: {result_img}")

            else:
                print(f"❌ [DEBUG] ERROR: Result file NOT found at: {detected_img_path}")
                print(f"ℹ️ [DEBUG] Alasan: Model tidak menemukan 'person' (classes=0), jadi tidak ada gambar yang disimpan.")
                error_msg = "Image processed, but no 'person' was detected."
                # result_img tetap None

        except Exception as e:
            print(f"🔥🔥🔥 [DEBUG] An exception occurred: {e}")
            error_msg = f"An error occurred: {e}"

    # Render template dengan semua variabel
    return render_template(
        "index.html", 
        result_img=result_img, 
        upload_img=upload_img,
        error_msg=error_msg
    )


if __name__ == "__main__":
    app.run(debug=True)