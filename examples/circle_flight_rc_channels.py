from pioneer_sdk import Pioneer
import math
import time

flight_duration = 100  # Продолжительность полёта в секундах

first_point = True
last_point_reached = False

if __name__ == "__main__":
    pioneer = Pioneer(ip="127.0.0.1", mavlink_port=8000)
    pioneer.arm()
    pioneer.takeoff()

    start_time = time.time()
    now_time = time.time()

    while now_time - start_time < flight_duration:
        now_time = time.time()

        radius_coefficient = 3
        time_delta = (now_time - start_time) / radius_coefficient

        delta_x = int(math.sin(time_delta) * 100)
        delta_y = int(math.cos(time_delta) * 100)

        pioneer.send_rc_channels(1500, 1500, 1500 + delta_x, 1500 + delta_y, 2000)
