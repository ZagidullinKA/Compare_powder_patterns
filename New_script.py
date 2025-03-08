import sys

# Импорт своих модулей

import Logger as lg
import FilesProcessor as fp
import FilesReader as fr
import PlotDF as pldf


class ValidationError(Exception):
    pass


def main():
    logger = lg.Logger()
    logger.Log_info("Старт")

    processor = fp.FilesProcessor(logger)
    processor.Files_processor()

    reader = fr.FilesReader(logger, processor)
    reader.Make_dataset()

    plotter = pldf.PlotDF(logger)
    xlim = (10, 50)
    plotter.plotting(reader.get_data, xlim)

    logger.Log_info("Успешно завершено!")

    sys.exit()


if __name__ == "__main__":
    main()
