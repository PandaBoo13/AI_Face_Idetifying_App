import cv2
import numpy as np
from PIL import Image
import os

recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

def get_images_and_labels(path):
    image_paths = [os.path.join(path, f) for f in os.listdir(path)]
    face_samples = []
    ids = []

    for image_path in image_paths:
        gray_img = Image.open(image_path).convert('L')
        img_numpy = np.array(gray_img, 'uint8')
        id = int(os.path.split(image_path)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_numpy)

        for (x, y, w, h) in faces:
            face_samples.append(img_numpy[y:y+h, x:x+w])
            ids.append(id)

    return face_samples, ids

print("\n [INFO] Đang train, vui lòng chờ...")
faces, ids = get_images_and_labels('dataset')
recognizer.train(faces, np.array(ids))
recognizer.save('trainer/trainer.yml')
print(f"\n [INFO] Train xong {len(np.unique(ids))} khuôn mặt.")
