import os
import pickle
from datetime import datetime


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
        self.logger.Log_info("Выгружен дамп с датасетом порошкограмм")

    def Make_csv(self, data):
        self.__current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        data.to_csv(f"Difract_dataset_{self.__current_time}.csv", index=False)
        self.logger.Log_info("Создан CSV файл 'Difract_dataset "
                             f"{self.__current_time}.csv'"
                             "с данными порошкограмм")

    def Make_dictionary_of_csv(self, labels):
        if os.path.exists("CSV files.txt"):
            with open("CSV files.txt", "a") as file:
                file.write(f"{self.__current_time} 'Difract_dataset"
                           f"{self.__current_time}.csv' is "
                           f"\n\t\t\t {labels}\n")
        else:
            with open("CSV files.txt", "w") as file:
                file.write(f"{datetime.now()} 'Difract_dataset"
                           f"{self.__current_time}.csv' is "
                           f"\n\t\t\t {labels}\n")
