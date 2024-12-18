# Compare_powder_patterns
Drawing program for comparison of experimental and theoretical powder patterns. 

Эта программа предназначена для создания иллюстраций с парными графиками дифрактограмм.
В первой версии предполагается работа с экспериментальной и теоретической дифрактограммами для их сравнения и анализа результатов химического синтеза.

Инструкция по использованию:

1) Создать в каталоге с программой три каталога: Experimental, Theoretical и Output.
2) В каталог Experimental поместить текстовый файл с результатами дифракционного эксперимента. Т.к. программа писалась под конкретный формат входных данных, то данные об углах должны располагаться во втором столбце, тогда как экспериментальные интенсивности - в третьем.
3) В каталог Theoretical поместить теоретическую дифрактограмму. Программа работает с файлами формата .xye, получаемыми при моделировании дифрактограмм в программном пакете Mercury. Теоретически, она будет понимать все текстовые файлы, в которых в первом столбце бцдцт расположены углы, а во втором - интенсивности.
4) Запустить программу.
5) Итоговое изображение будет находиться в каталоге Output.


This program is designed to create illustrations with paired graphs of diffraction patterns.
The first version is supposed to work with experimental and theoretical diffraction patterns for their comparison and analysis of the results of chemical synthesis.

Instructions for use:

1) Create three directories in the program directory: Experimental, Theoretical and Output.
2) Place a text file with the results of the diffraction experiment in the Experimental directory. Since the program was written for a specific format of input data, the data on the angles should be located in the second column, while the experimental intensities - in the third.
3) Place the theoretical diffraction pattern in the Theoretical directory. The program works with files of the .xye format, obtained when modeling diffraction patterns in the Mercury software package. Theoretically, it will understand all text files in which the angles are located in the first column bcdct, and the intensities in the second.
4) Run the program.
5) The final image will be located in the Output directory.
