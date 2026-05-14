import socket
import cv2
import numpy as np

udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
window_name = "Cam"
udp_client.bind(("0.0.0.0", 7575))

try:
    cv2.namedWindow(window_name)
    while True:
        udp_client.sendto(b"<ADMIN>", ("147.45.79.209", 5824))
        data, addr = udp_client.recvfrom(1024)
        if b"<OK>" in data:
            print("OK")
            break
    while True:
        data, addr = udp_client.recvfrom(65536)
        if b"<OK>" in data:
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