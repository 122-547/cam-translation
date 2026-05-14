# import cv2
# import socket
# import time

# def get_frame(cam: cv2.VideoCapture):
#     ret, frame = cam.read()
#     if not ret:
#         print("Ошибка чтения кадра.")
#         return None
#     success, encoded_img = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 40])

#     if success:
#         bytes_data = encoded_img.tobytes()
#         data_size = len(bytes_data)

#         if data_size < 65507:
#             return bytes_data
#         else:
#             print(f"Кадр слишком большой.")
#             return None


# client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server_addr = ("147.45.79.209", 5823)
# cam = cv2.VideoCapture(0)
# cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# DESIRED_FPS = 15
# frame_time = 1.0 / DESIRED_FPS

# try:
#     if not cam.isOpened():
#         print("Error: Не удалось открыть камеру.")
#         exit()

#     print("Клиент запущен. Отправка кадров...")

#     while True:
#         start_time = time.time()
#         frame = get_frame(cam)
#         if frame:
#             client.sendto(frame, server_addr)

#         elapsed_time = time.time() - start_time
#         sleep_time = frame_time - elapsed_time
#         if sleep_time > 0:
#             time.sleep(sleep_time)

# finally:
#     if cam:
#         cam.release()
#         client.close()
#         print("Клиент остановлен")

import cv2
import socket
import time

def get_frame(cam: cv2.VideoCapture):
    ret, frame = cam.read()
    if not ret:
        return None
    
    # Уменьшаем размер для UDP
    height, width = frame.shape[:2]
    if width > 640:
        scale = 640 / width
        new_width = 640
        new_height = int(height * scale)
        frame = cv2.resize(frame, (new_width, new_height))
    
    # Сжимаем с хорошим качеством
    success, encoded_img = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
    
    if success:
        bytes_data = encoded_img.tobytes()
        if len(bytes_data) < 65000:  # Оставляем запас
            return bytes_data
        else:
            # Если всё ещё большой, сжимаем сильнее
            success, encoded_img = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
            if success:
                return encoded_img.tobytes()
    return None

# Создаем сокет
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_addr = ("147.45.79.209", 5823)  # Порт видео сервера

# Инициализируем камеру
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cam.set(cv2.CAP_PROP_FPS, 15)

# Даем камере время на инициализацию
time.sleep(2)

DESIRED_FPS = 10
frame_time = 1.0 / DESIRED_FPS

try:
    if not cam.isOpened():
        print("Error: Не удалось открыть камеру.")
        exit()

    print("Клиент запущен. Отправка кадров на сервер...")
    print(f"Сервер: {server_addr}")
    
    frame_count = 0
    last_print = time.time()
    
    while True:
        start_time = time.time()
        frame_data = get_frame(cam)
        
        if frame_data:
            client.sendto(frame_data, server_addr)
            frame_count += 1
            
            # Статистика каждые 2 секунды
            if time.time() - last_print > 2:
                print(f"Отправлено кадров: {frame_count}")
                frame_count = 0
                last_print = time.time()
        else:
            print("Ошибка получения кадра", end='\r')
        
        # Контроль FPS
        elapsed_time = time.time() - start_time
        sleep_time = frame_time - elapsed_time
        if sleep_time > 0:
            time.sleep(sleep_time)

except KeyboardInterrupt:
    print("\nПрерывание пользователя")
finally:
    if cam:
        cam.release()
        client.close()
        print("Клиент остановлен")