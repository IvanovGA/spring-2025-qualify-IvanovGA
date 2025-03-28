import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from geobot_sdk import Geobot
import cv2
import time

if __name__ == "__main__":
    print(
        """
        w↑ 
    ←a      d→
        s↓"""
    )
    geobot = Geobot(ip="127.0.0.1", mavlink_port=8001)
    min_v = 1300
    max_v = 1700
    try:
        while True:
            ch_1 = 1500
            ch_2 = 1500
            ch_3 = 1500
            ch_4 = 1500
            ch_5 = 2000
            frame = cv2.imread("wasd.jpg")
            if frame is not None:
                cv2.imshow("pioneer_camera_stream", frame)
            key = cv2.waitKey(1)
            if key == 27:  # esc
                print("esc pressed")
                cv2.destroyAllWindows()
                break

            elif key == ord("w"):
                ch_3 = max_v
            elif key == ord("s"):
                ch_3 = min_v
            elif key == ord("a"):
                ch_4 = min_v
            elif key == ord("d"):
                ch_4 = max_v

            geobot._rc_channels_send(
                channel_1=ch_1,
                channel_2=ch_2,
                channel_3=ch_3,
                channel_4=ch_4,
                channel_5=ch_5,
            )
            time.sleep(0.02)
    finally:
        time.sleep(1)
        del geobot
