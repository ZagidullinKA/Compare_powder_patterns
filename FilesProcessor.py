import os
import sys


class ValidationError(Exception):
    pass


class FilesProcessor:
    def __init__(self, logger):
        self.__exp_files = []
        self.__sim_files = []
        self.__struct_files = []
        self.__exp_extension = ("txt", )
        self.__sim_extension = ("xye", "xy", )
        self.__struct_extension = ("cif", "res", )
        self.logger = logger
        self.__script_dir = self.__Script_directory()

    def __Script_directory(self):
        '''
        Определение директории, в которой находится скрипт
        '''
        return os.path.dirname(os.path.abspath(__file__))

    def __List_of_files(self):
        '''
        Получение списка файлов в директории Input
        '''
        file_names = os.listdir(os.path.join(self.__script_dir, "Input"))
        return file_names

    def __Categorize_files_by_extension(self, file_names: list):
        '''
        Разделение списка файлов на экспериментальные,
        теоретические и структурные
        '''
        for name in file_names:
            match name.split(".")[-1]:
                case ext if ext in self.__exp_extension:
                    self.__exp_files.append(name)
                case ext if ext in self.__sim_extension:
                    self.__sim_files.append(name)
                case ext if ext in self.__struct_extension:
                    self.__struct_files.append(name)
                case "png":
                    self.logger.Log_info(f"Обнаружен файл изображения {name}")
                case _:
                    self.logger.Log_warning(f"Расширение файла {name} "
                                            "не поддерживается")

    def __Validation_number(self, file_names: list):
        if len(file_names) == 0:
            raise ValidationError("Поместите файлы в директорию Input")
        elif len(file_names) > 10:
            raise ValidationError("В директории Input должно быть "
                                  "не более 10 файлов")
        return True

    def __Checking_number_of_files(self, file_names: list):
        try:
            self.__Validation_number(file_names)
        except ValidationError as e:
            sys.exit(e)

    @property
    def get_exp_files(self):
        return self.__exp_files

    @property
    def get_sim_files(self):
        return self.__sim_files

    @property
    def get_struct_files(self):
        return self.__struct_files

    @property
    def get_script_dir(self):
        return self.__script_dir

    def Files_processor(self):
        file_names = self.__List_of_files()
        self.__Checking_number_of_files(file_names)
        self.__Categorize_files_by_extension(file_names)
        self.logger.Log_debug(f"Experimental files {self.__exp_files}")
        self.logger.Log_debug(f"Simulated files {self.__sim_files}")
        self.logger.Log_debug(f"Structure files {self.__struct_files}")
