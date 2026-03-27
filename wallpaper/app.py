from flask import Flask, request, redirect, url_for, send_from_directory, render_template_string
import os

UPLOAD_FOLDER = "uploads"
FILENAME = "current.jpg"  # always overwrite
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

HTML_PAGE = """
<!doctype html>
<title>Awww Uploader</title>
<h2>Upload Wallpaper</h2>
<form method=post enctype=multipart/form-data>
  <input type=file name=file required>
  <input type=submit value=Upload>
</form>
<p>Current image: <a href="{{ url_for('uploaded_file') }}" target="_blank">View</a></p>
"""

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part", 400
        file = request.files["file"]
        if file.filename == "":
            return "No selected file", 400
        if file and allowed_file(file.filename):
            path = os.path.join(app.config["UPLOAD_FOLDER"], FILENAME)
            file.save(path)
            return redirect(url_for("upload_file"))
    return render_template_string(HTML_PAGE)

@app.route("/uploads/current.jpg")
def uploaded_file():
    return send_from_directory(app.config["UPLOAD_FOLDER"], FILENAME)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
