# -*-coding: utf-8 -*-
import os
import random
import shutil

# 定义各个文件夹的路径
parent_folder = "./classify"
a_folder = os.path.join(parent_folder, "M3-C")
c_folder = os.path.join(parent_folder, "M3-K")
b_folder = os.path.join(parent_folder, "M3-P")
MAX_SIZE = 10000
size_arr = []
# 计算每个文件夹中要划分为验证集的图片数量
val_ratio = 0.1
a_val_size = int(val_ratio * (len(os.listdir(a_folder)) if len(os.listdir(a_folder)) < 10000 else MAX_SIZE))
b_val_size = int(val_ratio * (len(os.listdir(b_folder)) if len(os.listdir(b_folder)) < 10000 else MAX_SIZE))
c_val_size = int(val_ratio * (len(os.listdir(c_folder)) if len(os.listdir(c_folder)) < 10000 else MAX_SIZE)) 

size_arr.append(a_val_size)
size_arr.append(b_val_size)
size_arr.append(c_val_size)

print(size_arr)
# 分别对每个文件夹进行处理，将图片移动到 train/ 和 val/ 目录中
train_folder = os.path.join(parent_folder, "train")
val_folder = os.path.join(parent_folder, "val")
os.makedirs(train_folder, exist_ok=True)
os.makedirs(val_folder, exist_ok=True)
for index, folder in enumerate([a_folder, b_folder, c_folder]):
    filenames = os.listdir(folder)
    random.shuffle(filenames)  # 打乱文件顺序
    val_filenames = set(filenames[:size_arr[index]])
    train_filenames = set(filenames[size_arr[index]:MAX_SIZE])

    # 移动文件到 train/ 或 val/ 目录中的子文件夹中
    for filename in val_filenames:
        src_path = os.path.join(folder, filename)
        os.makedirs(os.path.join(val_folder, os.path.basename(folder)), exist_ok = True)
        dst_path = os.path.join(val_folder, os.path.basename(folder), filename)
        print(filename)
        shutil.copy(src_path, dst_path)

    for filename in train_filenames:
        src_path = os.path.join(folder, filename)
        print(filename)
        os.makedirs(os.path.join(train_folder, os.path.basename(folder)), exist_ok = True)
        dst_path = os.path.join(train_folder, os.path.basename(folder), filename)
        shutil.copy(src_path, dst_path)
    

