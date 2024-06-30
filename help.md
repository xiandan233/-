# 视觉认知工程考察作业报告

## 一、数据标注过程

视频截取自《让子弹飞》中的一个片段。

<img src="C:\Users\26697\Videos\1234\1234_000014.jpg" alt="1234_000014" style="zoom: 25%;" />

​							图1：视频数据截取自电影《让子弹飞》

数据集由以下四部分组成：

### 1.image

使用工具Free Video to JPG Converter.lnk对帧进行分割，将原始视频分割为145帧，存放于mydata\image文件夹中。

### 2.alpha

数据使用PhotoShop 2024进行标注，具体标注过程如下：

1. 智能选区->选择主体。
2. 手动修改不准确的区域。
3. 将主体部分填充为白色，背景填充为黑色，生成二值图像。

生成图像结果如下：

<img src="C:\Users\26697\Desktop\3\066.png" alt="066" style="zoom: 25%;" />

​							图2：数据标注生成的alpha蒙版图片

经过上述操作，生成了主体的alpha蒙版，存放于mydata\alpha文件夹中。

### 3.trimap

通过“tri.py”生成trimap数据，存放于mydata\trimap文件夹中。

### 4.json文件

格式根据ICM57数据集，存放于mydata中。

## 二、实验过程

### 1.使用基于预训练的 In-Context Matting 模型生成预测蒙版

In-Context Matting有关的代码可从以下链接获取：

https://github.com/tiny-smart/in-context-matting

在配置ICM所需的环境中，遇到了许多问题，部分问题可参考“三、遇到的问题与解决方案”解决。

### 2.通过字节跳动提供的Colab demo调用预训练的Robust Video Matting模型预测蒙版

Colab链接如下：

[Google Colab](https://colab.research.google.com/drive/10z-pNKRnVNsp0Lq9tH1J_XPZ7CBC_uHm?usp=sharing)

### 3.计算对比两种方法得到的结果的五项指标

在计算之前，由于ICM输出数据尺寸与输入不同，需要先对标注的数据进行resize，实验中使用“resize.py”实现该功能。

RVM的github仓库中给出了一个现有的计算五种指标的程序"evaluate.py"，可以直接根据数据计算，并将结果存储为.xlsx文件，但是该方法对路径的设置要求比较复杂。因此，仓库中给出的“ev.py”计算的五项指标更加方便，两种方法所得的五项指标结果大致相同。

## 三、遇到的问题与解决方案

实验中遇到了许多问题，这里挑选部分记录：

#### 1.autodl服务器可选cuda版本与所需环境不一致

autodl服务器创建镜像时能选的版本有限，在创建镜像后，需要重新手动下载对应版本的cuda与cudnn。

#### 2.In-Context Matting环境缺少包

例如：

![image-20240630220639006](C:\Users\26697\AppData\Roaming\Typora\typora-user-images\image-20240630220639006.png)

​								图3：部分报错信息截图

解决方案：使用pip install 或者conda install下载缺失的包

### 3.hugging face

实验中遇到了sd21模型无法加载的问题，解决方案参考以下文章。

[Huggingface镜像站使用及常见报错_usage: huggingface-cli  [\] huggingf-CSDN博客](https://blog.csdn.net/weixin_42592151/article/details/136480973)

可以通过token将模型下载到本地，也可以修改evnl.ymal中的参数，使程序支持从镜像站加载模型。

### 4.In-Context Matting输出结果失真

模型对于并非正方形的输入数据会输出变形的结果，这点可以通过修改相关代码解决。

## 五、实验结果

### 1.定性结果

ICM模型生成的预测结果如下图所示：

<img src="C:\Users\26697\Desktop\1\068.png" alt="068" style="zoom:25%;" />

​								图4：ICM模型生成的预测结果

RVM模型生成的预测结果如下图所示：

<img src="C:\Users\26697\Desktop\4\068.png" alt="068" style="zoom:25%;" />

​								图5：RVM模型生成的预测结果

ground truth如下图所示：

<img src="C:\Users\26697\Desktop\3\068.png" alt="068" style="zoom:25%;" />

​								图6：对比标注的图片数据

可以看出，对于字幕和人物的手部，模型预测的效果较差。

### 2.定量结果

视频抠图主要由以下五个指标衡量：

**MAD（Mean Absolute Deviation）**：平均绝对偏差，表示抠图结果与真实值之间的平均绝对差异。数值越小，抠图结果越准确。

**MSE（Mean Squared Error）**：均方误差，表示抠图结果与真实值之间的平均平方差异。数值越小，抠图结果越准确。

**Grad（Gradient）**：梯度，可能表示图像边缘的锐利程度或边缘保留的效果。数值越大，说明边缘信息保留得越好。

**Conn（Connectivity）**：连通性，表示抠图后前景物体的完整性。数值越大，说明前景物体越连贯、完整。

**dtSSD（Dynamic Time Sequence Sum of Squared Differences）**：动态时间序列平方差和，可能用于衡量在时间序列中的变化情况。数值越小，说明随时间变化的平滑度越好。

实验结果如下表所示

| Methods | Remark | MAD       | MSE      | Grad     | Conn   | dtSSD    |
| ------- | ------ | --------- | -------- | -------- | ------ | -------- |
| RVM     | Paper  | **14.48** | **8.93** | **4.35** | 3.83   | 1.01     |
| ICM     | real   | 30.56     | 19.03    | 1.05     | 12     | 0.4      |
| RVM     | real   | 45.20     | 41.32    | 0.56     | **80** | **0.02** |

​							表1：5种视频抠图指标的对比

与论文结果对比发现，总体来说MAD，MSE，Conn偏大，而Grad，dtSSD偏小，而其中RVM方法的误差明显偏大。

## 五、讨论

### 1.定性分析

从直观感受，两个模型对于手部和字幕的预测效果相比于身体更差。

### 2.定量分析

与论文结果对比发现，总体来说MAD，MSE，Conn偏大，而Grad，dtSSD偏小，而其中RVM方法的误差明显偏大。

针对第一点，我认为主要是数据的原因，本次实验所选择的数据有两个特点：

1. 所选视频中有字幕，播放按键等干扰因素，影响了模型预测的结果。
2. 所选视频的运动幅度比较小，导致dsSSD等数据异常。

而针对第二点，主要原因也来自数据，但我推测原因应该与我截取视频帧序列时的操作有误有关：

RVM使用mp4格式视频作为输入，而原视频格式为(.mkv)，为了解决这个问题，我采用了以下的方法：

1. 将原视频转化为mp4格式。
2. 将转化后的视频输入RVM(Colab Demo)中生成蒙版视频。
3. 将蒙版视频分割为帧序列。

由于在第一步中数据产生了一定程度的变形，导致最终生成的帧序列和标注数据并不能很好对应，产生了一定程度的错位，导致误差较大。

此外，ICM预测的结果中对图像进行了裁剪，将较难预测的手部裁剪掉了部分，也可能是表现更加优良的部分原因。

### 3.对比

从定性角度：

1.可能由于运用了sd21模型的关系，ICM倾向于补全人物被边框所遮挡的部分。

<img src="C:\Users\26697\Desktop\1\028.png" alt="028" style="zoom:25%;" />

​								图7：ICM预测存在补全的问题

2.对于深度不同的部分，如手部，前倾的面部，模型明显预测结果更差，而且ICM对此方面更不擅长。

<img src="C:\Users\26697\AppData\Roaming\Typora\typora-user-images\image-20240701001349946.png" style="zoom:50%;" />

​								图8：左：RVM预测的结果；右：ICM预测的结果

从定量角度：

根据表1，ICM在这项任务上预测的结果更准确，但平滑性和完整性不够好。原因分析见上一部分。

## 六、代码以及数据

本次实验所有代码以及所用的数据集可以在以下github仓库中获取：

[xiandan233/Curriculum-design-of-VCE: hust.aia (github.com)](https://github.com/xiandan233/Curriculum-design-of-VCE)

使用方法参考仓库中的readme.md