# реализовать альтернативное именование введенными строками

import os
import sys

import matplotlib.pyplot as plt
import pandas as pd


class ValidationError(Exception):
    pass


def Script_directory():
    return os.path.dirname(os.path.abspath(__file__))


def Checking_for_file(script_dir, directory, file_names):
    if len(file_names) > 1:
        raise ValidationError("Должен быть один файл в "
                              f"директории {directory}")
    elif len(file_names) < 1:
        raise ValidationError("Отсутствует исходный файл в "
                              f"директории {directory}")
    return True


def Validation_of_files(script_dir, file_names_experimental,
                        file_names_theoretical):
    try:
        Checking_for_file(script_dir, "Experimental", file_names_experimental)
    except ValidationError as e:
        sys.exit(e)

    try:
        Checking_for_file(script_dir, "Theoretical", file_names_theoretical)
    except ValidationError as e:
        sys.exit(e)


def Get_dataframe(col_names, file_path):
    df_powder = pd.read_csv(
                            f"{file_path}",
                            sep=r'\s+|\t',
                            encoding="utf-8",
                            engine="python",
                            header=0,
                            names=col_names
                           )
    return df_powder


def Normalisation_one_df(df_powder, col_names, shift):
    df_int = df_powder[col_names].copy()
    df_normalized_int = df_int.copy()
    df_normalized_int[col_names[1]] = shift + \
        (
         df_int[col_names[1]]
         - df_int[col_names[1]].min()
        )/(
         df_int[col_names[1]].max()
         - df_int[col_names[1]].min()
        )
    return df_normalized_int


def Normalization_all_concat(
                             df_exp_powder,
                             df_theo_powder,
                             shift_exp,
                             shift_theo,
                             name_experimental,
                             name_theoretical
                            ):
    col_exp_norm_names = ["Position", f"{name_experimental}"]
    df_normalized_exp_int = Normalisation_one_df(
                                          df_exp_powder,
                                          col_exp_norm_names,
                                          shift_exp
                                         )

    col_theo_norm_names = ["Position", f"{name_theoretical}"]
    df_normalized_theo_int = Normalisation_one_df(
                                           df_theo_powder,
                                           col_theo_norm_names,
                                           shift_theo
                                          )

    df_exp_theo_int = pd.concat([df_normalized_exp_int,
                                df_normalized_theo_int])

    return df_exp_theo_int


def Plot_diagrams(df_exp_theo_int,
                  name_experimental,
                  name_theoretical,
                  script_dir,
                  plot_name):
    df_exp_theo_int.plot(
                         y=[f"{name_experimental}",
                            f"{name_theoretical}"],
                         x="Position",
                         xlim=[10, 50],
                         xlabel="2\u03b8",
                         ylabel="Rel.Int",
                         yticks=([]),
                         linewidth=0.5,
                        )

    plt.savefig(os.path.join(script_dir, "Output", plot_name), dpi=600)


def main():
    # Определяем расположение скрипта для построения дальнейших абсолютных
    # путей
    script_dir = Script_directory()

    # Прописываем пути к исходным файлам
    file_names_experimental = os.listdir(
        (os.path.join(script_dir, "Experimental"))
        )
    file_names_theoretical = os.listdir(
        os.path.join(script_dir, "Theoretical")
        )

    # проверяем наличие и единственность файлов в
    # папках ./Experimental и ./Theoretical
    Validation_of_files(script_dir, file_names_experimental,
                        file_names_theoretical)

    # Выделяем имена файлов без расширений
    name_experimental = (
        os.path.split(file_names_experimental[0])[1]
        ).split(sep='.', maxsplit=2)[0]
    name_theoretical = (
        os.path.split(file_names_theoretical[0])[1]
        ).split(sep='.', maxsplit=2)[0]

    # берем из файла экспериментальную дифрактограмму
    col_names_exp = ["№", "Position", f"{name_experimental}",
                     "Theo_Int", "I_HZ", "PSO", "d", "Err"]
    file_exp_path = f"{script_dir}./Experimental/{file_names_experimental[0]}"
    df_exp_powder = Get_dataframe(col_names_exp, file_exp_path)

    # берем из файла теоретическую дифрактограмму
    col_names_theo = ["Position", f"{name_theoretical}", "Err"]
    file_theo_path = f"{script_dir}./Theoretical/{file_names_theoretical[0]}"
    df_theo_powder = Get_dataframe(col_names_theo, file_theo_path)

    # определяем вертикальный сдвиг графиков
    shift_exp = 1.1
    shift_theo = 0

    # Нормализуем данные и объединяем в один датафрейм
    df_exp_theo_int = Normalization_all_concat(
                                               df_exp_powder,
                                               df_theo_powder,
                                               shift_exp,
                                               shift_theo,
                                               name_experimental,
                                               name_theoretical
                                              )

    # Строим диаграмму
    plot_name = "1.png"
    Plot_diagrams(df_exp_theo_int,
                  name_experimental,
                  name_theoretical,
                  script_dir,
                  plot_name)

    sys.exit("Успешно!")


if __name__ == "__main__":
    main()
