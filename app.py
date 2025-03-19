from flask import Flask, render_template, request, send_from_directory, redirect
import os
from flask_cors import CORS
from flask_wtf import FlaskForm
from wtforms import FileField

app = Flask(__name__)
CORS(app)

class ImageForm(FlaskForm):
    image = FileField("image")

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config["SECRET_KEY"] = "secret_key"

if not os.path.exists("uploads"):
    os.makedirs("uploads")

@app.route("/", methods=["GET", "POST"])
def homepage():
    if request.method == "POST":
        if 'image' not in request.files:
            return "No file uploaded"
        file = request.files['image']
        file.save(f"uploads/{file.filename}")

    images = os.listdir("uploads")

    return render_template("index.html", images=images)

@app.route("/upload")
def upload():
    form = ImageForm()
    return render_template("upload.html", form=form)

@app.route("/uploads/<filename>/see")
def download_file(filename):
    code = "<a class='img' href='/uploads/" + filename + "/see/url'><img src='/uploads/" + filename + "/see/url' alt='video or other file here'></a>"
    other_code = "<a href='/uploads/" + filename + "/see/url' download>Download</a><br><a href='/upload/" + filename + "/delete'>delete the file</a>"
    return render_template("see.html", code=code, file_name=filename, other_code=other_code)

@app.route("/upload/<filename>/delete")
def delete_file(filename):
    os.remove(f"uploads/{filename}")
    return redirect("/", code=302)

@app.route("/uploads/<filename>/see/url")
def file_url(filename):
    return send_from_directory("uploads", filename)

app.run(debug=True, host="0.0.0.0", port=5500)
