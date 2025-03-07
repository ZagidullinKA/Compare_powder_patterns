import os
import sys
import pandas as pd

# Импорт своих модулей

import Logger as lg
import FilesProcessor as fp
import MakerDataFiles as mdf


class ValidationError(Exception):
    pass


class FilesReader:
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


def main():
    logger = lg.Logger()
    logger.Log_info("Старт")

    processor = fp.FilesProcessor(logger)
    processor.Files_processor()

    reader = FilesReader(logger, processor)
    reader.Make_dataset()

    logger.Log_info("Успешно завершено!")

    sys.exit()


if __name__ == "__main__":
    main()
