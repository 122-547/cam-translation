import socket
import threading


# def get_admin_addr():
#     global admin, server_tcp
#     try:
#         server_tcp.bind(("localhost", 5824))
#         print("TCP сервер запущен и ожидает подключение админа...")
#         server_tcp.accept(1)
#         conn, addr = server_tcp.accept()
#         while True:
#             data = conn.recv(1024)
#             if data == b"<ADMIN>":
#                 print(f"Admin ({addr}) подключился к серверу.")
#                 admin = addr
#                 break
            
#     finally:
#         server_tcp.close()
    

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
admin = None
# waiting_admin = threading.Thread(target=get_admin_addr, daemon=True)
try:
    server.bind(("localhost", 5823))
    print("UDP Сервер запущен и ожидает кадры...")
    while True:
        data, addr = server.recvfrom(65536)
        if not data:
            break
        if admin:
            server.sendto(data, admin)
            print(f"Кадры пересланы админу ({admin}).")
        else:
            if data == b"<ADMIN>":
                admin = addr

finally:
    server.close()
    print("Сервер остановлен.")