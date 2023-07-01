from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

URLS = [
    "rtsp://YOUR_TAPO_ID:YOUR_TAPO_PW@YOUR_TAPO_IPCAM_LOCAL_IP1:554/stream2",  # 第一支攝影機 URL
    "rtsp://YOUR_TAPO_ID:YOUR_TAPO_PW@YOUR_TAPO_IPCAM_LOCAL_IP2:554/stream2",  # 第二支攝影機 URL
    "rtsp://YOUR_TAPO_ID:YOUR_TAPO_PW@YOUR_TAPO_IPCAM_LOCAL_IP3:554/stream2",  # 第三支攝影機 URL    
    "rtsp://YOUR_TAPO_ID:YOUR_TAPO_PW@YOUR_TAPO_IPCAM_LOCAL_IP4:554/stream2"  # 第四支攝影機 URL
]

def get_frames(urls):
    caps = [cv2.VideoCapture(url) for url in urls]

    while True:
        frames = []
        for cap in caps:
            ret, frame = cap.read()
            if not ret:
                break
            _, buffer = cv2.imencode(".jpg", frame)
            frames.append(buffer.tobytes())

        if len(frames) != len(urls):
            break

        frame_data = b""
        for frame in frames:
            frame_data += (b"--frame\r\n"
                           b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

        yield frame_data

@app.route("/video_feed/<int:camera_index>")  # 修改路由，加入攝影機索引
def video_feed(camera_index):
    if camera_index < len(URLS):
        return Response(get_frames([URLS[camera_index]]), mimetype="multipart/x-mixed-replace; boundary=frame")
    else:
        return "Invalid camera index."

@app.route("/")
def index():
    camera_urls = range(len(URLS))  # 修改為攝影機索引的範圍
    return render_template("video2to2refresh.html", camera_urls=camera_urls)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8088, debug=True)

