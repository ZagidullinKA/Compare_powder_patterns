import logging


class Logger:
    def __init__(self, Log_file="Log_file.log"):
        # Создание логгера
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # Определение формата сообщений
        formatter = logging.Formatter(
                                      "%(asctime)s-%(levelname)s-%(message)s",
                                      datefmt="%Y-%m-%d %H:%M:%S"
                                     )

        # Обработчик для записи в файл
        file_handler = logging.FileHandler(
                                           Log_file,
                                           mode="w",
                                           encoding="utf-8"
                                          )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Обработчик для вывода в терминал
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def Log_debug(self, message):
        self.logger.debug(message)

    def Log_info(self, message):
        self.logger.info(message)

    def Log_warning(self, message):
        self.logger.warning(message)

    def Log_error(self, message):
        self.logger.error(message)
