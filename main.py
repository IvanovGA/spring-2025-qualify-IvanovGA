#!/usr/bin/env python3


from flyer import Flyer
from rover import Rover
from logger import Logger
from navigator import Navigator

import time
import cv2
import threading
import sys


class App:
    def __init__(self, rover_config=None, flyer_config=None, navigator=None, logger=None):
        self.logger = logger
        self.navigator=navigator
        if self.logger:
            self.logger << f"Создан экземпляр App с параметрами: rover_config={rover_config}, flyer_config={flyer_config}"
        self.flyer = Flyer(config=flyer_config, logger=logger)
        self.rover = Rover(config=rover_config, logger=logger)
        # Остальной код, например, запуска потоков или основной цикл приложения.
        
    def run(self):
        if self.logger:
            self.logger << f"Запуск основной логики"
        points =  self.navigator.generate_random_route(points=50)
        #{   "Точка1": {"lat": 0, "lon": 0, "alt": 1},    "Точка2": {"lat": 1, "lon": -1, "alt": 2}}
  
        if self.flyer:
         self.flyer.fly_by_points(points)
        

    def close(self):
        """Явное завершение работы: закрытие Flyer и Rover."""
        if self.logger:
            self.logger << "Завершение работы приложения: закрытие устройств."
        try:
            if hasattr(self.flyer, "close"):
                self.flyer.close()
        except Exception as e:
            if self.logger:
                self.logger << f"Ошибка при закрытии Flyer: {e}"
        try:
            if hasattr(self.rover, "close"):
                self.rover.close()
        except Exception as e:
            if self.logger:
                self.logger << f"Ошибка при закрытии Rover: {e}"
        
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Не переданы необходимые аргументы: порт Пионера, порт камеры Пионера, порт Геобота. Пример: python main.py 8000 18000 8001")
        sys.exit(1)
    else:
        print("Старт приложения")

    # Разбираем параметры командной строки
    pioneer_mavlink_port = int(sys.argv[1])
    camera_port = int(sys.argv[2])
    rover_port = int(sys.argv[3])

    # Формируем конфигурационные словари для Flyer и Rover. 
    # Здесь для примера указан один и тот же ip, если требуется изменить – обновите данные.
    flyer_config = {'ip': '127.0.0.1', 'm_port': pioneer_mavlink_port, 'c_port': camera_port}
    rover_config = {'ip': '127.0.0.1', 'port': rover_port}  # для Rover ключ называем 'port', можно переименовать

    # Создаем экземпляр логгера
    logger = Logger()
    navigator=Navigator(logger=logger)
    
    # Запускаем приложение
    app = App(rover_config=rover_config, flyer_config=flyer_config,navigator=navigator, logger=logger)
    app.run()
    app.close()
    
    
    
