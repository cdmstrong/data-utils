# -*-coding:utf-8 -*-
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import json
import codecs
import base64
def perspective_transform(points, matrix):
    # 创建透视变换矩阵
    
    # 将坐标转换为齐次坐标
    points_homogeneous = np.concatenate([points, np.ones((points.shape[0], 1))], axis=1)
    # 进行透视变换
    transformed_points = np.dot(matrix, points_homogeneous.T).T
    # 将齐次坐标转换为二维坐标
    transformed_points = transformed_points[:, :2] / transformed_points[:, 2:]
    return transformed_points
def get_encoding(file_path):
    import chardet

    # 读取JSON文件并检测编码格式
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        print(encoding)

# 获取四个点的位置
def get_points(data):
    pts2 = []
    temp = []
    for i, point in enumerate(data):
        point = point["points"]
        item = [(point[0][0] + (point[1][0] - point[0][0])/2), (point[0][1] + (point[1][1] - point[0][1])/2)]
        if i%2 == 1:
            temp.append(item)
            continue
        pts2.append(item)
    pts2 = pts2 + temp
    return pts2
def parse(ori_name, dst_name):
    # ori_json = json.load("112830曝光640.json")
    # 读取JSON文件
    print('----------------')
    print(dst_name) 
    with open(ori_name, "r", encoding= "utf-8") as f:
        ori_data = json.load(f)
    with open(dst_name, 'r', encoding= "utf-8") as f:
        data = json.load(f)
    # 解析为字典
    ori_dict = dict(ori_data)
    dst_dict = dict(data)

    # 变换前的4个点
    # pts1 = np.float32([[1420, 930],[3844, 962], [1462, 2548],[3843, 2720]])#7428
    # pts1 = np.float32([[1169, 778],[3746, 1159], [1025, 2391],[3525, 2791]])#1495
    # pts1 = np.float32([[1490, 1403],[3837, 1028], [1622, 2779],[3947, 2566]])# 1516 new
    # pts1 = np.float32([[1552, 1301],[3916, 1026], [1543, 2647],[3877, 2555]])# 1516 temp
    # pts1 = np.float32([[1100, 1349],[4062, 723], [1147, 2643],[4113, 2168]])# 1516
    # pts1 = np.float32([[786, 1186],[3826, 508], [955, 2993],[3969, 2626]])# 1529

    # 变换后的4个点
    pts2 = []
    if len(dst_dict["shapes"]) > 4:
        return
    pts1 = get_points(ori_dict["shapes"][:4])
    pts2 = get_points(dst_dict["shapes"])
    print(pts2)

    # pts2 = np.float32([[1532, 849], [3974, 840], [1593, 2468], [3999, 2616]]) #
    matrix = cv2.getPerspectiveTransform(np.float32(pts1), np.float32(pts2))
    # print(ori_dict["shapes"][0]["points"])
    for i, point in enumerate(ori_dict["shapes"]):
        point = point["points"]
        item = np.float32([
            [
                point[0][0],
                point[0][1]
            ],
            [
                point[1][0],
                point[1][1]
            ]
        ])
        ori_dict["shapes"][i]["points"] = perspective_transform(item, matrix).tolist()
    # print(ori_dict["shapes"][0]["points"])
    image = cv2.imread(dst_name.replace("json", "bmp"))
    _, buffer = cv2.imencode('.jpg', image)
    ori_dict['imageData'] = base64.b64encode(buffer).decode('utf-8')

    with codecs.open(dst_name, "w") as f:
        json.dump(ori_dict, f)
    
def run(ori_path, first_filename):
    arr = os.listdir(ori_path)
    index = 0
    for item in arr:
        if item.endswith(".json") and first_filename + ".json" != item:
            parse(os.path.join(ori_path, first_filename + ".json"), os.path.join(ori_path, item))
            # index += 1

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
        if item == "112830720.bmp" or item.endswith(".py") or item.endswith(".bmp") or os.path.isdir(os.path.join(ori_path, item)):
            continue
        print(item)
        with open(os.path.join(ori_path, item), 'r', encoding= "utf-8") as f:
            data = json.load(f)
        old_item = item
        item = item.replace(old_id, new_id)
        
        data["imagePath"] = item.replace("json", "bmp")
        # 读取图像文件
        image_path = os.path.join(ori_path, data["imagePath"])
        if not os.path.exists(image_path):
            print(image_path + "is not exits")
            continue
        image = cv2.imread(image_path)

        # 将图像转换为Base64编码
        retval, buffer = cv2.imencode('.jpg', image)
        data["imageData"] = base64.b64encode(buffer).decode('utf-8')
        os.remove(os.path.join(ori_path, old_item))
        with codecs.open(os.path.join(ori_path, item), "w") as f:
            json.dump(data, f)

def replace_label(ori_path, old_id, new_id):

    arr = os.listdir(ori_path)
    for item in arr:
        if item.endswith(".py") or item.endswith(".bmp"):
            continue
        print(item)
        with open(os.path.join(ori_path, item), 'r', encoding= "utf-8") as f:
            data = json.load(f)
        shapes = data["shapes"]
        for labels in shapes:
            if labels["label"] == old_id:
                labels["label"] = labels["label"].replace(old_id, new_id)
        # 读取图像文件
        with codecs.open(os.path.join(ori_path, item), "w") as f:
            json.dump(data, f)

def rename(ori_path, word):
    for root, dirs, files in os.walk(ori_path):
        for file in files:
            # 检查文件名是否包含"曝光二"字样
            if word in file:
                # 构建新的文件名
                new_file = file.replace(word, "")
                # 构建文件的完整路径
                old_path = os.path.join(root, file)
                print(old_path)
                new_path = os.path.join(root, new_file)
                # 重命名文件
                os.rename(old_path, new_path)

if __name__ == "__main__":
    # replace_id("型号_1516/2800/7.25", "2200", "2800")
    # run("型号_1516/2600/7.25", "1008062800")
    # replace_label("型号_7428", "M3-P", "M4-P")
    # 重命名
    rename("型号_1516/2600/7.25", "ÆØ¹â")

    # for i in os.listdir("20230714曝光800"):
    #     if i.endswith('112830800.json') or i.endswith("112830800 copy.json") or i.endswith(".bmp"):
    #         continue
    #     os.remove(os.path.join("20230714曝光800", i))
