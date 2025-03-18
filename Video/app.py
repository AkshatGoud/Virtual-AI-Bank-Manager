from flask import Flask, render_template, request, send_from_directory
import os

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_video():
    if "video" not in request.files:
        return "No video file received", 400

    video = request.files["video"]
    video_path = os.path.join(UPLOAD_FOLDER, "user_recorded.webm")
    video.save(video_path)

    return "Video uploaded successfully", 200

if __name__ == "__main__":
    app.run(debug=True)
