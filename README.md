# 利用Python-Flask結合RTSP協定實現IPCam觀看的多平台化(TP-Link,Tapo)

By combining the RTSP protocol and Python programming, we can overcome the limitation of only being able to view surveillance footage through a mobile app. This allows users to access and control IPCams on their computers, providing a richer visual experience and more convenient operation.

Furthermore, integrating the RTSP protocol and Python programming enables the fusion of IPCams with artificial intelligence technologies, bringing more potential to applications. For example, utilizing computer vision techniques to analyze and recognize the images from IPCams can enable functions such as intelligent monitoring, object detection, or facial recognition. These applications expand the capabilities of IPCams, making them a more powerful and intelligent security surveillance solution.

# 動機

透過結合RTSP通訊協定和Python程式，我們能夠解決目前僅能透過手機APP觀看監視畫面的限制。這使得使用者可以在電腦上實現對IPCam的觀看和控制，提供更豐富的視覺體驗和更方便的操作。

此外，結合RTSP通訊協定和Python程式還可以實現IPCam與人工智能相關技術的結合，為應用帶來更多潛力。例如，利用電腦視覺技術對IPCam的影像進行分析和辨識，可以實現智能監控、物體檢測或人臉辨識等功能。這樣的應用擴展了IPCam的功能，使其成為一個更強大和智能的安全監控解決方案。

# Step 1 :

目前小弟是使用TP-Link廠牌中的Tapo系列做相關應用，Tapo有提供RTSP服務，如果您是使用其它廠牌是可以透過本文去做連接，當然在非Tapo系列下當然設定細節會有不同就要去查廠牌提供的規範去做設定，因此本文會以TP-Link廠牌做示範。

首先要做設定之前請先了解整個系統架構與流程，1. IP Camera會主動相連於WiFi Router，2. IP Camera的內部IP會分享串流媒體(影像)給開發者的電腦(你的python開發電腦)。3. 開發者的電腦會透過WiFi Router方式獲得相關資訊

> *規範說明:
1. 攝影機的配對就不再這裡介紹，不論是小米品牌或TP-Link其實設定都非常人性了，可以參考廠商說明文件
2. 本範例採用Local網路做範例來降低複雜度*
> 

![structure.png](image/structure.png)

# Step 2 :

首先您先設定您的Tapo帳號，可以透過兩個步驟去做設定，第一開啟Tapo APP後先到關於我(下圖報子步驟一)再來再點選您的Tapo登入帳號(下圖報步子驟二)，再來進入到設定畫面中可以看到您的帳號與密碼，您可以在裡面做密碼設定，設定完後做儲存

![698943.jpg](image/698943.jpg)

![698944.jpg](image/698944.jpg)

> *Note : 這裡設定完後做RTSP連結，有些網友分享Tapo系統有時候需要兩到三天工作天後才可以完成密碼設定或更換，但是我這邊當下就可以直接連結了*
> 

# Step 3:

查詢您的IP Camera，點選您要觀看的攝影機名稱，下圖”後面室外”為這次示範監視器

![698912.jpg](image/698912.jpg)

點選右上角的設定

![698911.jpg](image/698911.jpg)

點選監視器型號名稱

![698910.jpg](image/698910.jpg)

可以看到紅色框為Local的IP名稱，此範例為192.168.55.222，請把它紀錄起來

![698909.jpg](image/698909.jpg)

# Step 4 :

最後也是最重要的一部分就是Tapo設定規範，可參考如下RTSP即時串流的URL(網址)規範，這裡為了串流平順先以stream2做示範，ex: rtsp://ID123:key123@192.168.55.222:554/stream2，然後請參考下列程式碼範例

RTSP即時串流的URL(網址)規範：
對於1080P（1920 * 1080）串流：rtsp：//使用者名稱：密碼@IP位址：554 / stream1
對於360P（640 * 360）串流：rtsp：//使用者名稱：密碼@IP位址：554 / stream2

```python
from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)
cap = cv2.VideoCapture(0)

def get_frames():
    while True:
        URL = "rtsp://ID:Key@192.168.55.222:554/stream2"
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
```

> 參考 : [https://www.tp-link.com/tw/support/faq/2680/](https://www.tp-link.com/tw/support/faq/2680/)
> 

# Step 5 :

完成步驟4程式撰寫後，小弟是利用terminal方式進行程式運行，或您也可以依據個人習慣做起啟動程式

Step A: 切換磁碟槽

Step B: 進入您儲存的程式碼路徑

Step C:  運行您的程式碼

Step D:  此IP為您可以觀看網址

![code_terminal.jpg](image/code_terminal.jpg)

驗證成功畫面(如下)

![view.jpeg](image/view.jpeg)
