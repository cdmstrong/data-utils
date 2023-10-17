# -*-coding:utf-8 -*-
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import json
import codecs
import base64
import random
import string

item_type = {
    "M3-C": 48,
    "M3-P": 48,
    "M3-K": 48,
    "M4-P": 64,
    "M4-C": 64,
    "M4-K": 64,
}
def parse(ori_path, dst_path, filter_dir):
    # ori_json = json.load("112830曝光640.json")
    # 读取JSON文件
    print('----------------')
    print(ori_path) 
    if not os.path.exists(dst_path):
        os.mkdir(dst_path)
    find = 0
    for root, dirs, files in os.walk(ori_path):
        if root.split("/")[-1] in filter_dir:
            continue
        for i in filter_dir:
            if root.find(i) >= 0:
                find = 1
                break
        if find:
            continue
        print(root)
        for file in files:
            if file.endswith(".json"):
                with open(os.path.join(root, file), "r", encoding= "utf-8") as f:
                    ori_data = json.load(f)
                ori_dict = dict(ori_data)
                im = cv2.imread(os.path.join(root, file.replace("json", "bmp")))

                # 解析为字典
                for item in ori_dict["shapes"]:
                    point = item["points"]
                    label = item["label"]
                    x, y = (point[1][0] + point[0][0])/2, (point[1][1] + point[0][1])/2
                    filename = file.split('.')[0]
                    rand_string = ''.join(random.choices(string.ascii_lowercase, k=9))
                    item_size = item_type[label] + 4
                    if label == "M4-P":
                        label = "M3-P"
                    elif label == "M4-C":
                        label = "M3-C"
                    elif label == "M4-K":
                        label = "M3-K"
                    if not os.path.exists(dst_path + "/" + label):
                        os.mkdir(dst_path + "/" + label)
                    save_path = dst_path + "/" + label + "/" + filename + rand_string + ".jpg"
                    cropped_image = im[int(y - item_size/2):int(y + item_size/2),int(x - item_size/2):int(x + item_size/2)]
                # 将裁剪后的NumPy数组转换为图像并保存到输出文件
                    cv2.imwrite(save_path, cropped_image)
                # pts2 = np.float32([[1532, 849], [3974, 840], [1593, 2468], [3999, 2616]]) #
    
    
def run(ori_path, first_filename):
    arr = os.listdir(ori_path)
    for item in arr:
        if item == first_filename + ".bmp" or item.endswith(".py") or item.endswith(".bmp"):
            continue
        parse(os.path.join(ori_path, first_filename + ".json"), os.path.join(ori_path, item))

# 替换文件夹内，型号不同的信息
'''
ori_path: 文件夹路径
old_id: 旧的id 如720曝光
new_id :新的曝光id
ex: 20230714曝光800 换成 900 ori_path：20230714曝光800， old_id: 800, new_id = 
'''
def replace_id(ori_path, old_id, new_id):
    

    arr = os.listdir(ori_path)
    for item in arr:
        if item == "112830720.bmp" or item.endswith(".py") or item.endswith(".bmp"):
            continue
        print(item)
        with open(os.path.join(ori_path, item), 'r', encoding= "utf-8") as f:
            data = json.load(f)
        old_item = item
        item = item.replace(old_id, new_id)
        data["imagePath"] = item.replace("json", "bmp")
        # 读取图像文件
        image_path = os.path.join(ori_path, data["imagePath"])
        image = cv2.imread(image_path)

        # 将图像转换为Base64编码
        retval, buffer = cv2.imencode('.jpg', image)
        data["imageData"] = base64.b64encode(buffer).decode('utf-8')
        os.remove(os.path.join(ori_path, old_item))
        with codecs.open(os.path.join(ori_path, item), "w") as f:
            json.dump(data, f)

if __name__ == "__main__":
    parse("源数据/20230912", "classify2", [])
    # 型号_1459
    # 型号_1495 and new
    # 型号_1516 反面
    # 型号_1529
    # 型号_1561
    # 型号_7428 彩色
