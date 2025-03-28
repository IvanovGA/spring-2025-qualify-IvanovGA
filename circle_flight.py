#!/usr/bin/env python3
from pioneer_sdk import Pioneer, Camera, VideoStream
import cv2
import math
import numpy as np

angle = 0.0
number_of_points = 10
increment = 360 / number_of_points
radius = 0.6
flight_height = 1.0

command_x = radius * math.cos(math.radians(angle))
command_y = radius * math.sin(math.radians(angle))
command_yaw = math.radians(angle)

first_point = True
last_point_reached = False

if __name__ == "__main__":
    print("start")
    pioneer_mini = Pioneer(
        name='Pioneer',
        ip='127.0.0.1',
        mavlink_port=8000,
        connection_method='udpout',
        logger=True, 
        log_connection=True
    )
    pioneer_mini.arm()
    pioneer_mini.takeoff()
    camera = Camera()
    stream = VideoStream()
    stream.start()

    # Создаём окно OpenCV для отображения видеопотока
    cv2.namedWindow("pioneer_camera_stream", cv2.WINDOW_NORMAL)

    while True:
        frame = camera.get_frame()
        if frame is not None:
            decoded_frame = cv2.imdecode(
                np.frombuffer(frame, dtype=np.uint8), cv2.IMREAD_COLOR
            )
            cv2.imshow("pioneer_camera_stream", decoded_frame)

        if pioneer_mini.point_reached() or first_point:
            first_point = False
            if angle >= 360:
                last_point_reached = True
            else:
                angle += increment
                command_x = radius * math.cos(math.radians(angle))
                command_y = radius * math.sin(math.radians(angle))
                command_yaw += math.radians(increment)
                pioneer_mini.go_to_local_point(
                    x=command_x, y=command_y, z=flight_height, yaw=command_yaw
                )

        key = cv2.waitKey(1)
        if (key == 27) or last_point_reached:  # esc или завершение миссии
            print("Esc нажата или миссия завершена")
            cv2.destroyAllWindows()
            pioneer_mini.land()
            pioneer_mini.close_connection()
            del pioneer_mini
            break

