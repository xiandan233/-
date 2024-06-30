import numpy as np
from skimage import measure
from skimage.filters import sobel
from PIL import Image
import os




def load_images(directory, is_ground_truth=False):
    """
    从指定目录加载图像文件
    """
    images = []
    for i in range(120):
        filename = f"{i:03d}.png"  # 生成类似 000.png, 001.png, ..., 119.png 的文件名
        img_path = os.path.join(directory, filename)
        if os.path.exists(img_path):
            img = Image.open(img_path)
           
            img = img.convert('L')  # 转换为灰度图像
            img_array = np.array(img) / 255.0  # 归一化到 0-1 范围
            images.append(img_array)
        else:
            raise FileNotFoundError(f"找不到文件: {img_path}")
    return images


def calculate_metrics(predicted_frames, ground_truth_frames):
    num_frames = len(predicted_frames)
        
    # 初始化指标
    mad = 0
    mse = 0
    grad = 0
    conn = 0
    dt_ssd = 0
    
    for i in range(num_frames):
        pred = predicted_frames[i]
        gt = ground_truth_frames[i]
        
        # 计算 MAD
        mad += np.mean(np.abs(pred - gt))
        
        # 计算 MSE
        mse += np.mean((pred - gt) ** 2)
        
        # 计算 Grad (空间梯度)
        grad += np.mean(np.abs(sobel(pred) - sobel(gt)))
        
        # 计算 Conn (连通性)
        pred_labeled = measure.label(pred)
        gt_labeled = measure.label(gt)
        conn = np.sum(np.abs(pred_labeled.max() - gt_labeled.max()))
        
        # 计算 dtSSD (时间一致性)
        if i > 0:
            dt_ssd = np.mean((pred - predicted_frames[i-1]) ** 2)
    
    # 计算平均值
    mad /= num_frames
    mse /= num_frames
    # grad /= num_frames
    # conn /= num_frames
    dt_ssd /= (num_frames - 1)

    mad *= 1000
    mse *= 1000
    dt_ssd *= 100
    
    return {
        'MAD': mad,
        'MSE': mse,
        'Grad': grad,
        'Conn': conn,
        'dtSSD': dt_ssd
    }

# 设置数据路径
predicted_dir = "1/"
ground_truth_dir = "2/"

# 加载图像
try:
    predicted_frames = load_images(predicted_dir)
    ground_truth_frames = load_images(ground_truth_dir, is_ground_truth=True)
except FileNotFoundError as e:
    print(f"错误: {e}")
    exit(1)

# 确保加载了正确数量的帧
if len(predicted_frames) != 120 or len(ground_truth_frames) != 120:
    print(f"警告: 预期120帧，但加载了 {len(predicted_frames)} 个预测帧和 {len(ground_truth_frames)} 个真实帧")

# 计算指标
metrics = calculate_metrics(predicted_frames, ground_truth_frames)
print(metrics)