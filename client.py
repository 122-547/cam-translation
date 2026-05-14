import cv2
import socket
import time

def get_frame(cam: cv2.VideoCapture):
    ret, frame = cam.read()
    if not ret:
        print("Ошибка чтения кадра.")
        return None
    success, encoded_img = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 40])

    if success:
        bytes_data = encoded_img.tobytes()
        data_size = len(bytes_data)

        if data_size < 65507:
            return bytes_data
        else:
            print(f"Кадр слишком большой.")
            return None


client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_addr = ("147.45.79.209", 5823)
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

DESIRED_FPS = 15
frame_time = 1.0 / DESIRED_FPS

try:
    if not cam.isOpened():
        print("Error: Не удалось открыть камеру.")
        exit()

    print("Клиент запущен. Отправка кадров...")

    while True:
        start_time = time.time()
        frame = get_frame(cam)
        if frame:
            client.sendto(frame, server_addr)

        elapsed_time = time.time() - start_time
        sleep_time = frame_time - elapsed_time
        if sleep_time > 0:
            time.sleep(sleep_time)

finally:
    if cam:
        cam.release()
        client.close()
        print("Клиент остановлен")
        