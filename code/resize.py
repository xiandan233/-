import os
from PIL import Image

def crop_to_square(image):
    width, height = image.size
    size = min(width, height)
    left = (width - size) // 2
    top = (height - size) // 2
    right = left + size
    bottom = top + size
    return image.crop((left, top, right, bottom))

def process_directory(input_dir, output_dir):
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 遍历输入目录中的所有文件
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            # 打开图片
            input_path = os.path.join(input_dir, filename)
            with Image.open(input_path) as img:
                # 裁剪图片
                cropped_img = crop_to_square(img)
                
                # 保存裁剪后的图片
                output_path = os.path.join(output_dir, filename)
                resized_img = cropped_img.resize((768, 768), Image.LANCZOS)
                resized_img.save(output_path)
                print(f"Processed: {filename}")

# 设置输入和输出目录
input_directory = "mydata/alpha"
output_directory = "mydata/alpha_square"

# 处理目录
process_directory(input_directory, output_directory)

print("All images have been processed and saved to", output_directory)