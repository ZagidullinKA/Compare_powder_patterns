import os
import pandas as pd

# Импорт своего модуля для создания файлов дампа,
# датасета и справочника созданных CSV-файлов

import MakerDataFiles as mdf


class FilesReader:
    '''
    Производит чтение данных из файлов и компонует их в единый датафрейм.
    Для получения итогового датафрейма рекомендуется использовать метод
    get_data.
    Публичный метод Make_dataset вызывает методы чтения из файлов и создания
    датафреймов, после чего собирает их в единый датафрейм.
    Так же, с помощью модуля MakerDataFiles происходит создание бинарного дампа
    датафрейма, создание CSV файла и TXT справочника уже созданных CSV-файлов.
    '''
    def __init__(self, logger, processor):
        self.logger = logger
        self.processor = processor
        self.maker_data_files = mdf.MakerDataFiles(logger)
        self.__exp_data = pd.DataFrame()
        self.__exp_labels = []
        self.__sim_data = pd.DataFrame()
        self.__sim_labels = []
        self.__data = pd.DataFrame()
        self.__labels = []
        self.__input_directory = "INPUT"

    def __Read_data_from_file(self, file_path, col_names):
        '''
        Чтение данных из файла.
        IN:
        file_path - путь к файлу
        col_names - список заголовков столбцов
        OUT:
        dataframe с содержимым файла, озаглавленным col_names
        '''
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
        '''
        Получение пути к файлу.
        IN:
        file_name - имя файла в папке INPUT
        OUT:
        Путь к файлу file_name
        '''
        return os.path.join(self.processor.get_script_dir,
                            self.__input_directory,
                            file_name)

    def __Normalise_data(self, df_original, data_label):
        '''
        Нормализация интенсивностей, полученных из входных файлов.
        IN:
        df_original - датафрейм с 2theta и интенсивностями
        data_label - заголовок столбца интенсивностей
        OUT:
        df_normalized - нормированный датафрейм
        '''
        df_normalized = df_original.copy()
        df_normalized[data_label] = \
            (
                df_original[data_label]
                - df_original[data_label].min()
                )/(
                df_original[data_label].max()
                - df_original[data_label].min()
            )
        return df_normalized

    def __Make_exp_dataset(self):
        '''
        Заполнение датафрейма __exp_data
        нормализованными экспериментальными данными
        '''
        exp_files = self.processor.get_exp_files
        for name in exp_files:
            file_path = self.__File_path(name)
            name_without_extension = name.split(".")[0]
            theta_label = "2theta_" + name
            col_names = ["№", theta_label, name_without_extension,
                         "Theo_Int", "I_HZ", "PSO", "d", "Err"]

            exp_data = self.__Read_data_from_file(
                            file_path, col_names)[
                                [theta_label, name_without_extension]]
            exp_data_normalize = self.__Normalise_data(
                exp_data, name_without_extension)

            self.__exp_data = pd.concat([self.__exp_data, exp_data_normalize],
                                        axis=1)

            self.__exp_labels.append(name_without_extension)

    def __Make_sim_dataset(self):
        '''
        Заполнение датафрейма __sim_data расчетными данными
        '''
        exp_files = self.processor.get_sim_files
        for name in exp_files:
            file_path = self.__File_path(name)
            name_without_extension = name.split(".")[0]
            theta_label = "2theta_" + name
            col_names = [theta_label, name_without_extension, "Err"]

            sim_data = self.__Read_data_from_file(
                            file_path, col_names)[
                                [theta_label, name_without_extension]]
            sim_data_normalize = self.__Normalise_data(
                sim_data, name_without_extension)

            self.__sim_data = pd.concat([self.__sim_data, sim_data_normalize],
                                        axis=1)

            self.__sim_labels.append(name.split(".")[0])

    def Make_dataset(self):
        '''
        Вызов методов __Make_exp_dataset() и __Make_sim_dataset() и сборка
        полученных наборов данных в общий датафрейм.
        Создание дампа датафрейма, CSV-файла и заполнение TXT справочника
        созданных CSV-файлов с помощью модуля MakerDataFiles.
        '''
        self.__Make_exp_dataset()
        self.__Make_sim_dataset()
        self.__data = pd.concat([self.__sim_data, self.__exp_data],
                                axis=1)
        self.__labels = self.__sim_labels + self.__exp_labels
        self.logger.Log_info("Создан общий dataframe с данными порошкограмм")
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
