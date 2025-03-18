from flask import Flask, render_template, request, send_from_directory
import os

app = Flask(__name__)
UPLOAD_FOLDER = "/Users/akshat/Developer/Python/CODE/Virtual AI Bank Manager/HTML/static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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


@app.route("/upload-page")
def upload_page():
    return render_template("upload.html")


@app.route('/upload-page', methods=['POST'])
def upload_file():
    messages = []
    for doc_type in ["aadhar", "pan", "income_proof"]:
        if doc_type in request.files and request.files[doc_type].filename != "":
            document = request.files[doc_type]
            document_path = os.path.join(app.config['UPLOAD_FOLDER'], document.filename)
            document.save(document_path)
            messages.append(f"{doc_type.capitalize()} {document.filename} uploaded successfully!")
        else:
            messages.append(f"No {doc_type} uploaded.")
    
    return "<br>".join(messages)

if __name__ == "__main__":
    app.run(debug=True)