# -*-coding: utf-8 -*-
import os
import random
import shutil

def split_file(parent_folder):
    # 定义各个文件夹的路径
    dirs = os.listdir(parent_folder)
    dirs = [os.path.join(parent_folder, item) for item in dirs]
    MAX_SIZE = 30000
    # 计算每个文件夹中要划分为验证集的图片数量
    val_ratio = 0.1
    file_sizes = [ int(val_ratio * (len(os.listdir(item)) if len(os.listdir(item)) < 10000 else MAX_SIZE)) for item in dirs]
    # c_val_size = int(val_ratio * (len(os.listdir(c_folder)) if len(os.listdir(c_folder)) < 10000 else MAX_SIZE)) 

    # size_arr.append(a_val_size)
    random.seed(20)
    # 分别对每个文件夹进行处理，将图片移动到 train/ 和 val/ 目录中
    train_folder = os.path.join(parent_folder, "train")
    val_folder = os.path.join(parent_folder, "val")
    os.makedirs(train_folder, exist_ok=True)
    os.makedirs(val_folder, exist_ok=True)
    for index, folder in enumerate(dirs):
        filenames = os.listdir(folder)
        random.shuffle(filenames)  # 打乱文件顺序
        val_filenames = set(filenames[:file_sizes[index]])
        train_filenames = set(filenames[file_sizes[index]:MAX_SIZE])

        # 移动文件到 train/ 或 val/ 目录中的子文件夹中
        os.makedirs(os.path.join(val_folder, os.path.basename(folder)), exist_ok = True)
        # os.makedirs(os.path.join(val_folder, os.path.basename("labels")), exist_ok = True)
        # os.makedirs(os.path.join(val_folder, "M3-L"), exist_ok = True)
        os.makedirs(os.path.join(train_folder, os.path.basename(folder)), exist_ok = True)
        # os.makedirs(os.path.join(train_folder, os.path.basename("labels")), exist_ok = True)
        # os.makedirs(os.path.join(train_folder, "M3-L"), exist_ok = True)

        for filename in val_filenames:
            src_path = os.path.join(folder, filename)
            # txt_path = os.path.join(parent_folder,"labels", filename.replace("bmp", "txt"))
            # dst_path = os.path.join(val_folder, "M3-L", filename)
            dst_path = os.path.join(val_folder, os.path.basename(folder), filename)
            # dst_txt = os.path.join(val_folder, "labels", filename.replace("bmp", "txt"))
            print(dst_path)

            shutil.copy(src_path, dst_path)
            # shutil.copy(txt_path, dst_txt)

        for filename in train_filenames:
            src_path = os.path.join(folder, filename)
            # txt_path = os.path.join(parent_folder, "labels", filename.replace("bmp", "txt"))
            # dst_path = os.path.join(train_folder, "M3-L", filename)
            dst_path = os.path.join(train_folder, os.path.basename(folder), filename)
            # dst_txt = os.path.join(train_folder, "labels", filename.replace("bmp", "txt"))
            print(dst_path)
            shutil.copy(src_path, dst_path)
            # shutil.copy(txt_path, dst_txt)
    
def random_del(folder):
    filenames = os.listdir(folder)
    max_size = 16000
    del_size = len(filenames) - max_size
    random.seed(20)
    random.shuffle(filenames)  # 打乱文件顺序
    del_filenames = set(filenames[:del_size])
    for item in del_filenames:
        print(os.path.join(folder, item))
        os.remove(os.path.join(folder, item))
if __name__ == "__main__":
    parent_folder = "/home/cdm/code/ncnn-plate/cut_dir/clspatch1"
    split_file(parent_folder)
    # random_del(parent_folder)