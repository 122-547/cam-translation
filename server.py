import socket

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
admin = None

try:
    server.bind(("0.0.0.0", 5823))
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
                admin = (addr[0], 5823)

finally:
    server.close()
    print("Сервер остановлен.")