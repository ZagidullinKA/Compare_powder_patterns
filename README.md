# Compare_powder_patterns
Drawing program for comparison of experimental and theoretical powder patterns. 

## Russian

Эта программа предназначена для создания иллюстраций с графиками дифрактограмм.
В данной версии предполагается работа с несколькими экспериментальными и теоретическими дифрактограммами для их сравнения и анализа результатов химического синтеза.
Количество загружаемых дифрактограмм может быть от 1 до 10.

Инструкция по использованию:

1) В каталог INPUT поместить .txt файлы с результатами дифракционного эксперимента или .xye файлы с данными смоделированной дифрактограммы. Файлов должно быть не более 10;
2) Запустить файл Compare_patterns.py;
3) В командной строке появится предложение просмотреть график. Если просто нажать Enter или ввести "N" или "n" - программа завершит работу. Если ввести "Y" или "y" - будет отображен график.
4) В каталоге Output появится .csv файл с обработанными данными, график в формате .png, вспомогательный справочный .txt файл со списком созданных .csv файлов и списком соответствующих исходных файлов, а так же дамп данных.

## English

This program is designed to create illustrations with diffraction pattern graphs.
This version assumes working with several experimental and theoretical diffraction patterns for their comparison and analysis of chemical synthesis results.
The number of diffraction patterns to be loaded can be from 1 to 10.

Instructions for use:

1) Place .txt files with the results of the diffraction experiment or .xye files with the simulated diffraction pattern data in the INPUT directory. There should be no more than 10 files;
2) Run the Compare_patterns.py file;
3) A prompt to view the graph will appear in the command line. If you simply press Enter or enter "N" or "n" - the program will exit. If you enter "Y" or "y" - the graph will be displayed.
4) The Output directory will contain a .csv file with the processed data, a graph in .png format, an auxiliary reference .txt file with a list of the created .csv files and a list of the corresponding source files, as well as a data dump.
