from pioneer_sdk import Pioneer, Camera
import cv2
import time

if __name__ == "__main__":
    print(
        """
    1 -- arm
    2 -- disarm
    3 -- takeoff
    4 -- land

    ↶q  w↑  e↷    i-↑
    ←a      d→     k-↓
        s↓"""
    )
    pioneer = Pioneer(ip="127.0.0.1", mavlink_port=8000)
    camera = Camera(ip="127.0.0.1", port=18000)
    min_v = 1200
    max_v = 1800
    try:
        while True:
            ch_1 = 1500
            ch_2 = 1500
            ch_3 = 1500
            ch_4 = 1500
            ch_5 = 2000
            frame = camera.get_cv_frame()
            if frame is not None:
                cv2.imshow("pioneer_camera_stream", frame)
            key = cv2.waitKey(1)
            if key == 27:  # esc
                print("esc pressed")
                cv2.destroyAllWindows()
                pioneer.land()
                break
            elif key == ord("1"):
                pioneer.arm()
            elif key == ord("2"):
                pioneer.disarm()
            elif key == ord("3"):
                time.sleep(2)
                pioneer.arm()
                time.sleep(1)
                pioneer.takeoff()
                time.sleep(2)
            elif key == ord("4"):
                time.sleep(2)
                pioneer.land()
                time.sleep(2)
            elif key == ord("w"):
                ch_3 = min_v
            elif key == ord("s"):
                ch_3 = max_v
            elif key == ord("a"):
                ch_4 = min_v
            elif key == ord("d"):
                ch_4 = max_v
            elif key == ord("q"):
                ch_2 = 2000
            elif key == ord("e"):
                ch_2 = 1000
            elif key == ord("i"):
                ch_1 = 2000
            elif key == ord("k"):
                ch_1 = 1000

            pioneer.send_rc_channels(
                channel_1=ch_1,
                channel_2=ch_2,
                channel_3=ch_3,
                channel_4=ch_4,
                channel_5=ch_5,
            )
            time.sleep(0.02)
    finally:
        time.sleep(1)
        pioneer.land()

        pioneer.close_connection()
        del pioneer