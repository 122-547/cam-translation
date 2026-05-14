# import socket
# import cv2
# import numpy as np

# udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# window_name = "Cam"
# udp_client.bind(("0.0.0.0", 7575))

# try:
#     cv2.namedWindow(window_name)
#     while True:
#         udp_client.sendto(b"<ADMIN>", ("147.45.79.209", 5824))
#         data, addr = udp_client.recvfrom(1024)
#         if b"<OK>" in data:
#             print("OK")
#             break
#     while True:
#         data, addr = udp_client.recvfrom(65536)
#         if b"<OK>" in data:
#             continue
#         np_arr = np.frombuffer(data, dtype=np.uint8)
#         frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

#         if frame is not None:
#             cv2.imshow(window_name, frame)

#         if cv2.waitKey(1) & 0xFF == ord("q"):
#             break
#         if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
#             break

# finally:
#     cv2.destroyAllWindows()
#     udp_client.close()
#     print("Админ отключился.")

import socket
import cv2
import numpy as np
import time

# Создаем два сокета для разных портов
admin_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Для регистрации
video_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Для приема видео

window_name = "Cam Stream"

try:
    # Привязываем сокеты
    video_socket.bind(("0.0.0.0", 7575))  # Порт для приема видео
    admin_socket.bind(("0.0.0.0", 0))  # Любой свободный порт
    
    print("Админ запущен")
    print("Подключение к серверу...")
    
    # Регистрируемся на сервере
    server_admin_port = ("147.45.79.209", 5824)  # Порт админов на сервере
    
    for attempt in range(5):
        admin_socket.sendto(b"<ADMIN>", server_admin_port)
        print(f"Попытка регистрации {attempt + 1}/5")
        
        # Ждем подтверждение
        admin_socket.settimeout(2.0)
        try:
            data, addr = admin_socket.recvfrom(1024)
            if b"<OK>" in data:
                print("Регистрация успешна!")
                break
        except socket.timeout:
            if attempt == 4:
                print("Не удалось зарегистрироваться")
                exit()
            continue
    
    # Настраиваем окно
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 800, 600)
    
    print("Ожидание видео... Нажмите 'q' для выхода")
    
    video_socket.settimeout(0.5)
    frame_count = 0
    last_print = time.time()
    
    while True:
        try:
            # Получаем видео
            data, addr = video_socket.recvfrom(65536)
            
            # Пропускаем служебные сообщения
            if b"<OK>" in data:
                continue
            
            # Декодируем кадр
            np_arr = np.frombuffer(data, dtype=np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            
            if frame is not None:
                frame_count += 1
                cv2.imshow(window_name, frame)
                
                # Статистика
                if time.time() - last_print > 2:
                    print(f"Получено кадров: {frame_count}")
                    frame_count = 0
                    last_print = time.time()
            
            # Проверяем нажатие клавиш
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
                
            # Проверяем, что окно не закрыто
            if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                break
                
        except socket.timeout:
            # Нет данных, но продолжаем
            print(".", end='', flush=True)
            continue

except KeyboardInterrupt:
    print("\nПрерывание пользователя")
except Exception as e:
    print(f"\nОшибка: {e}")
finally:
    cv2.destroyAllWindows()
    admin_socket.close()
    video_socket.close()
    print("Админ отключился.")