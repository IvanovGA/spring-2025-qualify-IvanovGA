from pioneer_sdk import Pioneer
import math

angle = 0
number_of_points = 10
increment = float(360 / number_of_points)
radius = 2
flight_height = 1

last_point_reached = False

if __name__ == "__main__":
    pioneer = Pioneer(ip="127.0.0.1", mavlink_port=8000)

    pioneer.arm()
    pioneer.takeoff()
    
    while not last_point_reached:
            if angle >= 360:
                last_point_reached = True

            angle += increment
            command_x = radius * math.cos(math.radians(angle))
            command_y = radius * math.sin(math.radians(angle))

            pioneer.go_to_local_point(command_x, command_y, flight_height, 0)

            while not pioneer.point_reached():
                pass
