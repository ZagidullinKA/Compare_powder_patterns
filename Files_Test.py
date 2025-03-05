import os
import sys
import logging


class ValidationError(Exception):
    pass


class Logger:
    def __init__(self, log_file="log_file.log"):
        # Создание логгера
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # Определение формата сообщений
        formatter = logging.Formatter(
                                      "%(asctime)s-%(levelname)s-%(message)s",
                                      datefmt="%Y-%m-%d %H:%M:%S"
                                     )
        
        # Обработчик для записи в файл
        file_handler = logging.FileHandler(log_file, mode="w")
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Обработчик для вывода в терминал
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def log_debug(self, message):
        self.logger.debug(message)

    def log_info(self, message):
        self.logger.info(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_error(self, message):
        self.logger.error(message)


class FilesProcessor:
    def __init__(self):
        self.__exp_files = []
        self.__sim_files = []
        self.__struct_files = []
        self.__exp_extension = ("txt", )
        self.__sim_extension = ("xye", "xy", )
        self.__struct_extension = ("cif", "res", )
        self.logger = Logger()
        self.__script_dir = self.Script_directory()

    def Script_directory(self):
        # Определение директории, в которой находится скрипт
        return os.path.dirname(os.path.abspath(__file__))

    def List_of_files(self):
        # Получение списка файлов в директории Input
        file_names = os.listdir(os.path.join(self.__script_dir, "Input"))
        return file_names

    def Categorize_files_by_extension(self, file_names: list):
        # Разделение списка файлов на экспериментальные,
        # теоретические и структурные
        for name in file_names:
            match name.split(".")[-1]:
                case ext if ext in self.__exp_extension:
                    self.__exp_files.append(name)
                case ext if ext in self.__sim_extension:
                    self.__sim_files.append(name)
                case ext if ext in self.__struct_extension:
                    self.__struct_files.append(name)
                case "png":
                    self.logger.log_info(f"Обнаружен файл изображения {name}")
                case _:
                    self.logger.log_warning(f"Расширение файла {name} "
                                            "не поддерживается")

    def Validation_number(self, file_names: list):
        if len(file_names) == 0:
            raise ValidationError("Поместите файлы в директорию Input")
        elif len(file_names) > 10:
            raise ValidationError("В директории Input должно быть "
                                  "не более 10 файлов")
        return True

    def Checking_number_of_files(self, file_names: list):
        try:
            self.Validation_number(file_names)
        except ValidationError as e:
            sys.exit(e)

    def Files_processor(self):
        file_names = self.List_of_files()
        self.Checking_number_of_files(file_names)
        self.Categorize_files_by_extension(file_names)
        self.logger.log_debug(f"Experimental files {self.__exp_files}")
        self.logger.log_debug(f"Simulated files {self.__sim_files}")
        self.logger.log_debug(f"Structure files {self.__struct_files}")


def main():
    processor = FilesProcessor()
    processor.Files_processor()


if __name__ == "__main__":
    main()
