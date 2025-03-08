import os
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime


class PlotDF():
    def __init__(self, logger):
        self.logger = logger
        self.__output_dir = "OUTPUT"

    def plotting(
                 self,
                 df: pd.DataFrame,
                 xlim: tuple = None,
                 linewidth: float = 1.0,
                 colors: list = None
                ):
        num_data_pairs = len(df.columns) // 2

        fig, axes = plt.subplots(num_data_pairs, 1,
                                 figsize=(8, 3 * num_data_pairs))

        if num_data_pairs == 1:
            axes = [axes]

        if colors is None:
            colors = plt.cm.tab10.colors

        for pair in range(num_data_pairs):
            x_col = df.columns[2 * pair]
            y_col = df.columns[2 * pair + 1]

            axes[pair].plot(df[x_col], df[y_col], label=y_col,
                            linewidth=linewidth,
                            color=colors[pair])
            axes[pair].set_xlabel("2theta")
            axes[pair].set_ylabel("Relative intensity")
            axes[pair].legend()
            axes[pair].set_title(y_col)

            if xlim is not None:
                axes[pair].set_xlim(xlim)
                self.logger.Log_debug(f"Выбранный диапазон значений для {y_col}: {xlim}")

        self.logger.Log_info("График построен!")

        plt.tight_layout()

        self.__current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        plot_name = os.path.join(self.__output_dir,
                                 f"Plot_{self.__current_time}.png")

        plt.savefig(plot_name, dpi=600)

        if self.Show_choice():
            plt.show()

    def Show_choice(self):
        print("Отобразить график?\ny - Да, N - нет")
        show_plot = input()
        if show_plot in ["Y", "y"]:
            return True
        elif show_plot in ["N", "n", ""]:
            return False
        else:
            self.Show_choice()
