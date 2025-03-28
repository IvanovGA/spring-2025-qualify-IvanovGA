import cv2
from pioneer_sdk import Camera

# Подключение к камере дрона
camera = Camera()

if __name__ == "__main__":
    while True:
        frame = camera.get_cv_frame()
        cv2.imshow("video", frame)  # Выводит изображение на экран

        if cv2.waitKey(1) == 27:  # Выход по нажатии ESC
            break

    cv2.destroyAllWindows()  # Закрывает все окна openCV 