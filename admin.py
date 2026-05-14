import socket
import threading
import cv2
import numpy as np

def send_admin_message():
    global tcp_client
    try:
        tcp_client.conenct(("147.45.79.209", 5824))
        tcp_client.send(b"<ADMIN>")
        tcp_client.close()
    finally:
        if tcp_client:
            tcp_client.close()

udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
window_name = "Cam"

try:
    cv2.namedWindow(window_name)
    while True:
        data, addr = udp_client.recvfrom(65536)
        if not data:
            continue

        np_arr = np.frombuffer(data, dtype=np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if frame is not None:
            cv2.imshow(window_name, frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
            break

finally:
    cv2.destroyAllWindows()
    udp_client.close()
    print("Админ отключился.")