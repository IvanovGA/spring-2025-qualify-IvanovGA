from pioneer_sdk import Camera, Pioneer
import math
import time

class Flyer(Pioneer):
    def __init__(self, config=None, logger=None):
        self.config = config or {}
        self.logger = logger
        self.start_coords=None
        if self.logger:
            self.logger << f"__________________FLYER____________________________________"
            self.logger << f"Создается экземпляр Flyer с конфигурацией: {self.config}"
        
        # Инициализация базового класса Pioneer с использованием ip и mavlink-порта из config.
        try:
            super().__init__(ip=self.config['ip'], mavlink_port=self.config['m_port'])
            if self.logger:
                preflight_state = self.get_preflight_state() if hasattr(self, 'get_preflight_state') else 'нет данных'
                self.logger << f"Базовый класс Pioneer инициализирован: {self} с параметрами: {preflight_state}"
        except Exception as e:
            if self.logger:
                self.logger << f"Ошибка инициализации Pioneer: {e}"
            raise

        
        # Инициализация камеры с использованием ip и порта камеры из config.
        try:
            self.camera = Camera(ip=self.config['ip'], port=self.config['c_port'])
            if self.logger:
                self.logger << f"Создан экземпляр камеры (Camera): {self.camera}"
        except Exception as e:
            if self.logger:
                self.logger << f"Ошибка инициализации камеры: {e}"
            raise

    def fly_to_point(self,target_x=None, target_y=None, target_z=None):
            if self.logger:
                self.logger << f"Целевые координаты {target_x, target_y, target_z} "

            coords=self.get_local_position_lps()

            if self.logger:
                self.logger << f"Текущие координаты {coords}"

            if not target_x and coords:
              target_x=coords[0]
            if not target_y and coords:
              target_y=coords[1]
            if not target_z and coords:
              target_z=coords[2]


            # Вычисляем угол, под которым находится целевая точка относительно текущей точки
            if  coords:
                yaw = math.atan2(target_y - coords[1], target_x - coords[0])
            else:
               yaw=0
               
            if self.logger:
                self.logger << f"Вычисленный тангаж {yaw} последние координаты {coords}"

      
            # Если требуется перевод в градусы: math.degrees(yaw)
            # Отправляем команду перемещения, включая рассчитанный yaw
            rez= self.go_to_local_point(x=target_x, y=target_y, z=target_z, yaw=yaw)
            t=0
            while (not self.point_reached()) and (t<5):
                time.sleep(0.1)
                t+=0.1
            if self.logger:
                self.logger << f"Продолжительность полета {t} в точку {target_x,target_y,target_z}"

   
            return rez

    def fly_by_points(self, points_dict):
        """
        Реализует полет по точкам, координаты которых передаются в виде словаря.
        
        Ожидаемый формат points_dict:
            {
                "Точка1": {"lat": значение, "lon": значение, "alt": значение},
                "Точка2": {"lat": значение, "lon": значение, "alt": значение},
                ...
            }
        
        Для перемещения используется метод goto(), который должен быть реализован в базовом классе Pioneer.
        """

        if self.logger:
            self.logger << f"<<<<<<<<<________ПОЛЕТ_____>>>>>>>>>>>"
            self.logger << "Начало полета по заданным точкам."

        

        if not self.start_coords:
           self.start_coords=self.get_local_position_lps()
        
        if self.logger:
            self.logger << f" {self} начальные координаты: {self.start_coords}"
        rez = False
        
        for point_name, coords in points_dict.items():
            try:
                if not rez:
                   armed=self.arm()
                   flying=self.takeoff()           
                if self.logger:
                    self.logger << f" Лежим? '{armed}' Летим? {flying}"
                
                # Проверка наличия всех необходимых координат.
                lat = coords["lat"]
                lon = coords["lon"]
                alt = coords["alt"]
                if lat is None or lon is None or alt is None:
                    raise ValueError(f"Неполные координаты для точки {point_name}: {coords}")
                
                if self.logger:
                    self.logger << f"Перелет к точке '{point_name}' с координатами: lat={lat},lon={lon},alt={alt}"
                
                
                rez = self.fly_to_point(
                    target_x=lat, target_y=lon, target_z=alt
                )
                
                if self.logger:
                    self.logger << f"Успешно достигнута точка '{point_name}' с результатом  {rez}."
            except Exception as e:
                if self.logger:
                    self.logger << f"Ошибка при перелете в точку '{point_name}': {e} полетная рограмма {points_dict}"
        
        if self.logger:
            self.logger << "___________Полёт по точкам завершен.__________________"

    def close(self):
        if self.logger:
            self.logger << f"______________________ДЕСТРУКТОР-FLYER______________________"
            self.logger << "Начинается завершение работы Flyer: посадка и закрытие соединений."
        
        # Попытка выполнить посадку с помощью метода land() из Pioneer.
        try:
            self.land()
            if self.logger:
                self.logger << "Посадка выполнена успешно."
        except Exception as e:
            if self.logger:
                self.logger << f"Ошибка при выполнении посадки: {e}"
        
        # Закрытие соединения с Pioneer с помощью метода close_connection().
        try:
            self.close_connection()
            if self.logger:
                self.logger << "Соединение с Pioneer успешно закрыто."
        except Exception as e:
            if self.logger:
                self.logger << f"Ошибка при закрытии соединения Pioneer: {e}"
        
        # Если у камеры присутствует метод для закрытия соединения, вызываем его.
        if hasattr(self, 'camera'):
            try:
                if hasattr(self.camera, "close") and callable(self.camera.close):
                    self.camera.close()
                    if self.logger:
                        self.logger << "Соединение с камерой успешно закрыто через метод close()."
                elif hasattr(self.camera, "close_connection") and callable(self.camera.close_connection):
                    self.camera.close_connection()
                    if self.logger:
                        self.logger << "Соединение с камерой успешно закрыто через метод close_connection()."
                else:
                    if self.logger:
                        self.logger << "Метод закрытия соединения для камеры не найден."
            except Exception as e:
                if self.logger:
                    self.logger << f"Ошибка при закрытии соединения камеры: {e}"
