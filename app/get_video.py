import os.path
import time
from ultralytics import YOLO
import cv2
import math

from app import app


def get_video(url):
    # url = 'http://root:RmskBd9922@5.228.66.147:8000/live/media/DESKTOP-6KKNVN4/DeviceIpint.2/SourceEndpoint.video:0:0'
    camera = cv2.VideoCapture(url)

    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n'
                   b'\r\n' + frame + b'\r\n')
            time.sleep(0.04)


def detect_video(url):
    model_path = os.path.join(os.path.dirname(__file__), 'static\\best.pt')

    if not os.path.exists(model_path):
        return "Model not found"

    model = YOLO(model_path)

    cap = cv2.VideoCapture(url)
    classnames = ['fire']

    while True:
        success, frame = cap.read()

        if not success:
            break
        else:
            # frame = cv2.resize(frame, (640, 480))
            results = model(frame, stream=False, verbose=False)
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    # print(x1, y1, x2, y2)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)
                    conf = math.ceil((box.conf[0] * 100)) / 100
                    cls = int(box.cls[0])
                    class_name = classnames[cls]
                    label = f'{class_name}{conf}'
                    t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=2)[0]
                    # print(t_size)
                    c2 = x1 + t_size[0], y1 - t_size[1] - 3
                    cv2.rectangle(frame, (x1, y1), c2, [255, 0, 255], -1, cv2.LINE_AA)  # filled
                    cv2.putText(frame, label, (x1, y1 - 2), 0, 1, [255, 255, 255], thickness=1, lineType=cv2.LINE_AA)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n'
                   b'\r\n' + frame + b'\r\n')
            time.sleep(0.04)

            # yield (b'--frame\r\n'
            #       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
