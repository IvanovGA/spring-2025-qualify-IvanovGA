

class Rover:
    def __init__(self, config=None, logger=None):
        self.config = config or {}
        self.logger = logger
        if self.logger:
            self.logger << f"Создается экземпляр Rover с параметрами {self.config}"
        # Если для Rover требуется инициировать подключение к устройству, добавьте здесь нужный код.
        # Например:
        # self.device = SomeDevice(ip=self.config.get('ip', '127.0.0.1'), port=self.config.get('port', 8001))
        # if self.logger:
        #    self.logger << f"Создан экземпляр Rover: {self.device}"


