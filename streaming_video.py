from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)
cap = cv2.VideoCapture(0)

def get_frames():
    while True:
        URL = "rtsp://YOUR_TAPO_ID:YOUR_TAPO_PW@YOUR_TAPO_IPCAM_LOCAL_IP:554/stream2"
        cap = cv2.VideoCapture(URL)
        ret, frame = cap.read()
        if not ret:
            break
        else:
            _, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()
            yield (b"--frame\r\n"
                   b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

@app.route("/video_feed")
def video_feed():
    return Response(get_frames(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/")
def index():
    return render_template("video.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8088, debug=True)