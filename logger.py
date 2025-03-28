import logging
import warnings
import inspect
import sys

class Logger:
    def __init__(self, logfile_name='log.txt', mode='w'):
        # Удаляем существующие обработчики у корневого логгера, чтобы basicConfig не игнорировался
        root_logger = logging.getLogger()
        if root_logger.hasHandlers():
            root_logger.handlers.clear()

        # Устанавливаем уровень логирования
        root_logger.setLevel(logging.INFO)

        # Создаем форматтер    format="%(asctime)s [%(levelname)s]: %(message)s"
        formatter = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s")

        # Настраиваем обработчик для файла
        file_handler = logging.FileHandler(logfile_name, mode=mode)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

        # Если требуется вывод логов и в консоль, можно добавить StreamHandler:
        # stream_handler = logging.StreamHandler(sys.stdout)
        # stream_handler.setFormatter(formatter)
        # root_logger.addHandler(stream_handler)

        self.logger = root_logger

    def my_showwarning(self, message, category, filename, lineno, file=None, line=None):
        log_message = f"{filename}:{lineno}: {category.__name__}: {message}"
        self.logger.warning(log_message)

    def __lshift__(self, other):
        frame = inspect.currentframe().f_back
        filename = frame.f_code.co_filename
        lineno = frame.f_lineno
        log_message = f"{filename}:{lineno}: INFO: {other}"
        self.logger.info(log_message)
        return self

def exception_handler(exc_type, exc_value, exc_traceback):
    logger = logging.getLogger()
    logger.exception("Необработанное исключение:",
                     exc_info=(exc_type, exc_value, exc_traceback))
    sys.__excepthook__(exc_type, exc_value, exc_traceback)

sys.excepthook = exception_handler

