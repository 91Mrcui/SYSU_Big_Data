MapReduce算法实现文档数词

20337025 崔璨明

mapper.py文件实现map，reducer.py文件实现reduce，由main.py程序控制（Sorts和Shuffles也在其中）。

为了模拟并行处理，采用了三个线程，每个线程是一个mapper，提取不同的文章，经过Sorts和Shuffles后由一个reducer处理。

输入信息记录在input文件夹中：

input_1.txt、input2.txt、input_3.txt是三篇不同的文章。

输出的结果记录在output文件夹中：

map的结果记录在output_1.txt文件中。

Sorts and Shuffles的结果记录在output_2.txt文件中。

mapreduce最后的结果记录在output_3.txt文件中。

运行方法：在该文件夹中直接运行main.py即可。
