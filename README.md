# Curriculum-design-of-VCM



该仓库为hust.aia视觉认知工程课设题目三的一个实现。该题目需要截取视频片段标注蒙版数据，并使用ICM与RVM两种预训练的模型预测蒙版，最后计算两种方法所得结果的5项指标并进行对比。关于具体的实验流程，可以参考help.md一文。

该工作在https://github.com/tiny-smart/in-context-matting的基础上进行，但具体实现细节与代码有所区别，具体信息见下文所述。

## 环境

- ICM需要在linux环境下运行，且GPU显存至少24G。

- ICM推荐使用cuda=11.7，python=3.10

- 具体的环境安装过程参考https://github.com/tiny-smart/in-context-matting一文。

- 在环境的配置过程中可能会遇到一些问题。部分问题的解决方案在help.md中给出。

## 数据

- 下载链接：

​	https://pan.baidu.com/s/1hunhxFD4Z_y4CSFwlo7l0g?pwd=yv06 
​	提取码：yv06 

- 数据构成：

​	mydata是用于ICM输入的数据，revl_data是用于计算评估指标的数据，.mkv文件是未经处理的原视频。

- 在ICM上的使用方法

​	下载完成后，将mydata解压数据目录下datasets/

​	将eval.yaml中dataset_name一项改为mydata，再执行运行以下代码。将占位符换为实际路径。

​	预训练模型的获取参考上文环境中给出的链接。

```
python eval.py --checkpoint PATH_TO_MODEL --save_path results/ --config config/eval.yaml
```

## 代码使用方法

该仓库的代码是对ICM中功能的一些补充，具体使用方法如下

- resize.py

  作用：将图像分辨率修改为768x768，以匹配ICM模型的输出结果

  使用方法：修改35，36行的路径为实际的输入与输出路径

- tri.py

​	作用：生成trimap数据

​	使用方法：将该文件与alpha，image文件夹置于同一目录下并运行

- evaluate.py

​	作用：计算5项评估指标

​	使用方法：见代码内部给出的指南

- ev.py

​	作用：计算评估指标的简易版本

​	使用方法：将81，82行路径修改为实际的预测结果与GT对应的路径

## 实验结果

实验结果如下表所示：

| Methods | Remark | MAD       | MSE      | Grad     | Conn   | dtSSD    |
| ------- | ------ | --------- | -------- | -------- | ------ | -------- |
| RVM     | Paper  | **14.48** | **8.93** | **4.35** | 3.83   | 1.01     |
| ICM     | real   | 30.56     | 19.03    | 1.05     | 12     | 0.4      |
| RVM     | real   | 45.20     | 41.32    | 0.56     | **80** | **0.02** |

如果有遗漏或者不解之处，请随时联系我202115204@hust.edu.cn



