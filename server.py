# import socket

# server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# accept_admin = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# admin = None

# try:
    
#     print("UDP Сервер запущен и ожидает кадры...")
#     accept_admin.bind(("0.0.0.0", 5824))
#     while admin is None:
#         data, addr = accept_admin.recvfrom(1024)
#         if b"<ADMIN>" in data:
#             admin = (addr[0], 7575)
#             for i in range(5):
#                 server.sendto(b"<OK>", admin)
#     accept_admin.close()
#     server.bind(("0.0.0.0", 5823))
#     while True:
        
#         data, addr = server.recvfrom(65536)
#         if not data:
#             break
#         server.sendto(data, admin)
#         print(f"Кадры пересланы админу ({admin}).", end="\r")


# finally:
#     server.close()
#     if accept_admin:
#         accept_admin.close()
#     print("Сервер остановлен.")


import socket
import threading
import time

# Создаем два разных сокета для разных портов
admin_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Для приема админов
video_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Для видео

admin_addr = None

try:
    # Привязываем сокеты к разным портам
    admin_socket.bind(("0.0.0.0", 5824))
    video_socket.bind(("0.0.0.0", 5823))
    
    print("UDP Сервер запущен")
    print(f"Порт для админов: 5824")
    print(f"Порт для видео: 5823")
    
    # Ожидаем подключение админа
    print("Ожидание подключения админа...")
    while admin_addr is None:
        admin_socket.settimeout(1.0)
        try:
            data, addr = admin_socket.recvfrom(1024)
            if b"<ADMIN>" in data:
                admin_addr = (addr[0], 7575)  # Порт админа для видео
                print(f"Админ подключен: {admin_addr}")
                # Отправляем подтверждение
                for _ in range(3):
                    admin_socket.sendto(b"<OK>", addr)
                    time.sleep(0.1)
                break
        except socket.timeout:
            continue
    
    print("Начинаем ретрансляцию видео...")
    
    # Основной цикл пересылки видео
    while True:
        video_socket.settimeout(0.5)
        try:
            data, addr = video_socket.recvfrom(65536)
            if data and admin_addr:
                # Отправляем видео админу
                video_socket.sendto(data, admin_addr)
                print(f"Кадр переслан админу", end='\r')
        except socket.timeout:
            continue
        except Exception as e:
            print(f"\nОшибка при пересылке: {e}")
            break

except KeyboardInterrupt:
    print("\nПрерывание работы сервера")
except Exception as e:
    print(f"\nОшибка: {e}")
finally:
    admin_socket.close()
    video_socket.close()
    print("Сервер остановлен.")