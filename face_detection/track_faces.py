from datetime import datetime, timedelta

import cv2
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

from geekcon2022_becoming_zaphod.face_detection.attributes import load_attribute_model, find_attributes_of_face


# from facenet_pytorch import MTCNN


def detection_as_ascii(new_h, frame_shape, face):
    scale = new_h / frame_shape[0]
    new_w = int(round(float(frame_shape[1]) * scale))
    face_int = (face * scale).astype(int)
    face_int = np.minimum(face_int, [new_w-1, new_h-1, new_w-1, new_h-1])
    face_int = np.maximum(face_int, 0)
    ##
    asc = [["+"] + ["-"] * (new_w - 2) + ["+"]]
    for r in range(new_h - 2):
        asc.append(["|"] + [" "] * (new_w - 2) + ["|"])
    asc.append([["+"] + ["-"] * (new_w - 2) + ["+"]])
    asc = np.vstack(asc)
    ##
    if not np.all(face_int == 0):
        asc[face_int[1], face_int[0]] = 'x'
        asc[face_int[3], face_int[0]] = 'x'
        asc[face_int[1], face_int[2]] = 'x'
        asc[face_int[3], face_int[2]] = 'x'
        for y in range(face_int[1] + 1, face_int[3]):
            asc[y, face_int[0]] = '|'
            asc[y, face_int[2]] = '|'
        for x in range(face_int[0] + 1, face_int[2]):
            asc[face_int[1], x] = '-'
            asc[face_int[3], x] = '-'
    res_str = "".join(["".join(row) + "\n" for row in asc])
    return res_str

def crop_face_from_frame(face, frame):
    w, h = face[2] - face[0], face[3] - face[1]
    ext_face = np.array([face[0] - 0.5 * w, face[1] - 0.5 * h, face[2] + 0.5 * w, face[3] + 0.5 * h]).astype(int)
    ext_face = np.minimum(ext_face, [frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
    ext_face = np.maximum(ext_face, 0)
    face_crop = frame[ext_face[1]:ext_face[3], ext_face[0]:ext_face[2]]
    return face_crop


def detect_faces_in_frame(frame, model):
    scale = 320. / frame.shape[1]
    frame = cv2.resize(frame, None, fx=scale, fy=scale)
    # boxes, _ = mtcnn.detect(frame)
    # boxes = face_recognition.face_locations(frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detects faces of different sizes in the input image
    boxes = model.detectMultiScale(gray, 1.3, 5)

    if len(boxes) == 0:
        return None, 0.5, frame

    boxes = np.vstack(boxes)

    if model is None:  # face detector
        boxes = boxes[:, [3, 0, 1, 2]]  # convert from y1, x2, y2, x1
    elif isinstance(model, cv2.CascadeClassifier):
        boxes = np.hstack([boxes[:, :2], boxes[:, :2] + boxes[:, 2:]])  # x y w h
    max_dim = (boxes[:, 2:] - boxes[:, :2]).max(axis=1)
    biggest_loc = np.argmax(max_dim)
    face = boxes[biggest_loc, :]
    x_center = (face[2] + face[0]) / 2
    relative_x_center = x_center / frame.shape[1] - 0.5
    return face, relative_x_center, frame


def main():
    cam = cv2.VideoCapture(0)
    # device = "cpu"  # torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    # model = MTCNN(keep_all=True, device=device)
    model = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    # model = None
    attr_model = load_attribute_model("cpu")

    if not cam.isOpened():
        print("camera was not opened")
        return

    frame_id = 0
    attributes_dict = {}
    while True:
        # time.sleep(0.1)
        start = datetime.now()
        ret, frame = cam.read()
        elapsed_capture = datetime.now() - start

        if not ret:
            print("no image")
            continue

        save_elapsed = timedelta(0)
        # if frame_id % 100 == 0:
        #     start = datetime.now()
        #     cv2.imwrite(os.path.join(os.path.dirname(__file__), f"{frame_id:05d}.jpg"), frame)
        #     save_elapsed = datetime.now() - start
        frame_id += 1

        start = datetime.now()
        face, relative_x_center, frame = detect_faces_in_frame(frame, model)
        detect_elpsed = datetime.now() - start
        if face is None:
            face = np.zeros((4, 1))

        fps = np.floor(1e6 / (elapsed_capture + detect_elpsed + save_elapsed).microseconds)
        print(detection_as_ascii(10, frame.shape, face) +
              f'{frame_id:04d} {datetime.now()} location: {relative_x_center:.02f}, fps: {fps}')

        if not np.all(face == 0) and frame_id % 5 == 0:
            face_crop = crop_face_from_frame(face, frame)
            result, attributes_dict = find_attributes_of_face(face_crop, attr_model)
            print([k for k,v in attributes_dict.items() if v])

        vis = False
        if vis:
            plt.clf()
            scale = 320. / frame.shape[1]
            frame_sm = cv2.resize(frame, None, fx=scale, fy=scale)
            plt.imshow(frame_sm[:, :, ::-1])
            plt.gca().add_patch(Rectangle((face[0], face[1]), face[2] - face[0], face[3] - face[1], alpha=0.5))
            plt.show()


if __name__ == '__main__':
    main()
