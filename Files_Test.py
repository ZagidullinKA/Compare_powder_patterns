import os
import sys
import logging
import pandas as pd
import pickle
from datetime import datetime


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
        file_handler = logging.FileHandler(
                                           log_file,
                                           mode="w",
                                           encoding="utf-8"
                                          )
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
                    self.logger.log_info(f"Обнаружен файл изображения {name}")
                case _:
                    self.logger.log_warning(f"Расширение файла {name} "
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
        self.logger.log_debug(f"Experimental files {self.__exp_files}")
        self.logger.log_debug(f"Simulated files {self.__sim_files}")
        self.logger.log_debug(f"Structure files {self.__struct_files}")


class FilesReader:
    def __init__(self, logger, processor):
        self.logger = logger
        self.processor = processor
        self.maker_data_files = MakerDataFiles(logger)
        self.__exp_data = pd.DataFrame()
        self.__exp_labels = []
        self.__sim_data = pd.DataFrame()
        self.__sim_labels = []
        self.__data = pd.DataFrame()
        self.__labels = []

    def __Read_data_from_file(self, file_path, col_names):
        df = pd.read_csv(
                            f"{file_path}",
                            sep=r'\s+|\t',
                            encoding="utf-8",
                            engine="python",
                            header=0,
                            names=col_names
                        )
        return df

    def __File_path(self, file_name):
        return os.path.join(self.processor.get_script_dir, "Input", file_name)

    def __Make_exp_dataset(self):
        exp_files = self.processor.get_exp_files
        for name in exp_files:
            file_path = self.__File_path(name)
            name_without_extension = name.split(".")[0]
            col_names = ["№", "2theta", f"{name_without_extension}",
                         "Theo_Int", "I_HZ", "PSO", "d", "Err"]

            exp_data = self.__Read_data_from_file(
                            file_path, col_names)[
                                ["2theta", f"{name_without_extension}"]]
            self.__exp_data = pd.concat([self.__exp_data, exp_data],
                                        axis=1)

            self.__exp_labels.append(name_without_extension)

    def __Make_sim_dataset(self):
        exp_files = self.processor.get_sim_files
        for name in exp_files:
            file_path = self.__File_path(name)
            name_without_extension = name.split(".")[0]
            col_names = ["2theta", f"{name_without_extension}", "Err"]

            sim_data = self.__Read_data_from_file(
                            file_path, col_names)[
                                ["2theta", f"{name_without_extension}"]]
            self.__sim_data = pd.concat([self.__sim_data, sim_data],
                                        axis=1)

            self.__sim_labels.append(name.split(".")[0])

    def Make_dataset(self):
        self.__Make_exp_dataset()
        self.__Make_sim_dataset()
        self.__data = pd.concat([self.__sim_data, self.__exp_data],
                                axis=1)
        self.__labels = self.__sim_labels + self.__exp_labels
        self.logger.log_info("Создан общий dataframe с данными порошкограмм")
        self.maker_data_files.Make_dump(self.__data)
        self.maker_data_files.Make_csv(self.__data)
        self.maker_data_files.Make_dictionary_of_csv(self.__labels)

    @property
    def get_exp_data(self):
        return self.__exp_data

    @property
    def get_exp_labels(self):
        return self.__exp_labels

    @property
    def get_sim_data(self):
        return self.__sim_data

    @property
    def get_sim_labels(self):
        return self.__sim_labels

    @property
    def get_data(self):
        return self.__data


class MakerDataFiles():
    def __init__(self, logger):
        self.logger = logger
        self.__current_time = ""

    def Make_dump(self, data: list):
        '''
        Выгрузка дампа полученного датасета порошкограмм
        '''
        with open('dump of powders.pickle', 'wb') as f:
            pickle.dump(data, f)
        self.logger.log_info("Выгружен дамп с датасетом порошкограмм")

    def Make_csv(self, data):
        self.__current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        data.to_csv(f"Difract_dataset_{self.__current_time}.csv", index=False)
        self.logger.log_info("Создан CSV файл 'Difract_dataset "
                             f"{self.__current_time}.csv'"
                             "с данными порошкограмм")

    def Make_dictionary_of_csv(self, labels):
        if os.path.exists("CSV files.txt"):
            with open("CSV files.txt", "a") as file:
                file.write(f"{self.__current_time} 'Difract_dataset_"
                           f"{self.__current_time}.csv' is \n\t\t\t {labels}\n")
        else:
            with open("CSV files.txt", "w") as file:
                file.write(f"{datetime.now()} 'Difract_dataset_"
                           f"{self.__current_time}.csv' is \n\t\t\t {labels}\n")


def main():
    logger = Logger()
    logger.log_info("Старт")

    processor = FilesProcessor(logger)
    processor.Files_processor()

    reader = FilesReader(logger, processor)
    reader.Make_dataset()

    logger.log_info("Успешно завершено!")

    sys.exit()


if __name__ == "__main__":
    main()
