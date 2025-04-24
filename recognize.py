import cv2
import os
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

cam = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX
def load_names_from_dataset():
    names = {}
    for filename in os.listdir("dataset"):
        if filename.endswith(".jpg"):
            parts = filename.split(".")
            name_part = parts[0]  # Ví dụ: 'Nam_User'
            user_id = int(parts[1])  # Ví dụ: '1'
            name = name_part.split("_")[0]  # Lấy 'Nam'
            names[user_id] = name
    return names

names = load_names_from_dataset()

while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, 1.2, 5)

    for (x, y, w, h) in faces:
        id, confidence = recognizer.predict(gray[y:y+h, x:x+w])  # đúng vùng mặt
    if confidence < 100:
        name = names.get(id, "Unknown")
        text = f"{name} ({round(100 - confidence)}%)"
    else:
        text = "Unknown"
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.putText(img, text, (x+5, y-5), font, 1, (255, 255, 255), 2)


    cv2.imshow('camera', img)

    # Thoát nếu bấm ESC hoặc đóng cửa sổ
    if cv2.getWindowProperty('camera', cv2.WND_PROP_VISIBLE) < 1:
        break
    if cv2.waitKey(10) & 0xff == 27:
        break


cam.release()
cv2.destroyAllWindows()
