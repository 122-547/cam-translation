import socket

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
accept_admin = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
admin = None

try:
    
    print("UDP Сервер запущен и ожидает кадры...")
    accept_admin.bind(("0.0.0.0", 5824))
    while admin is None:
        data, addr = accept_admin.recvfrom(1024)
        if b"<ADMIN>" in data:
            admin = (addr[0], 7575)
            for i in range(5):
                server.sendto(b"<OK>", admin)
    accept_admin.close()
    server.bind(("0.0.0.0", 5823))
    while True:
        
        data, addr = server.recvfrom(65536)
        if not data:
            break
        server.sendto(data, admin)
        print(f"Кадры пересланы админу ({admin}).", end="\r")


finally:
    server.close()
    if accept_admin:
        accept_admin.close()
    print("Сервер остановлен.")