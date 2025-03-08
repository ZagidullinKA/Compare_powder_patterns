import os
import pickle

from datetime import datetime


class MakerDataFiles():
    def __init__(self, logger):
        self.logger = logger
        self.__current_time = ""
        self.__output_dir = "OUTPUT"

    def Make_dump(self, data: list):
        '''
        Выгрузка дампа полученного датасета порошкограмм
        '''
        file_name = os.path.join(self.__output_dir, "dump_of_powders.pickle")
        with open(file_name, 'wb') as f:
            pickle.dump(data, f)
        self.logger.Log_info("Выгружен дамп с датасетом порошкограмм")

    def Make_csv(self, data):
        self.__current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file_name = os.path.join(self.__output_dir,
                                 f"Difract_dataset_{self.__current_time}.csv")
        data.to_csv(file_name, index=False)
        self.logger.Log_info("Создан CSV файл 'Difract_dataset "
                             f"{self.__current_time}.csv'"
                             "с данными порошкограмм")

    def Make_dictionary_of_csv(self, labels):
        file_name = os.path.join(self.__output_dir, "CSV files.txt")
        if os.path.exists(file_name):
            with open(file_name, "a") as file:
                file.write(f"{self.__current_time} 'Difract_dataset"
                           f"{self.__current_time}.csv' is "
                           f"\n\t\t\t {labels}\n")
        else:
            with open(file_name, "w") as file:
                file.write(f"{datetime.now()} 'Difract_dataset"
                           f"{self.__current_time}.csv' is "
                           f"\n\t\t\t {labels}\n")
