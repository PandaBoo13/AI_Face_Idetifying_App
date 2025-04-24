import cv2

# Khởi tạo camera và cascade detector
cam = cv2.VideoCapture(0)
detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Nhập ID và tên người dùng
face_id = input('\n Nhập ID người dùng (ví dụ 1): ')
name = input('\n Nhập tên người dùng: ')  # Nhập tên người dùng
count = 0

while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        count += 1
        # Lưu ảnh với tên người dùng và ID
        cv2.imwrite(f"dataset/{name}_User.{face_id}.{count}.jpg", gray[y:y+h, x:x+w])
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(img, f"{name}", (x + 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Hiển thị webcam
    cv2.imshow('image', img)

    # Dừng khi nhấn ESC hoặc đã thu thập đủ ảnh
    k = cv2.waitKey(100) & 0xff
    if k == 27 or count >= 50:
        break

cam.release()
cv2.destroyAllWindows()
