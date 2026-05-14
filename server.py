import socket

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
admin = None

try:
    server.bind(("0.0.0.0", 5823))
    print("UDP Сервер запущен и ожидает кадры...")
    while admin is None:
        data, addr = server.recvfrom(1024)
        if b"<ADMIN>" in data:
            admin = (addr[0], 7575)
            for i in range(5):
                server.sendto(b"<OK>", admin)
    while True:
        data, addr = server.recvfrom(65536)
        if not data:
            break
        server.sendto(data, admin)
        print(f"Кадры пересланы админу ({admin}).", end="\r")


finally:
    server.close()
    print("Сервер остановлен.")