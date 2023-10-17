import os
import matplotlib.pyplot as plt
import enum 
import json
import cv2
import numpy as np
import base64
import codecs
types = {
    "M3盘头钉": "M3-P",
    "M3沉头钉": "M3-C",
    "M4盘头钉": "M4-P",
    "M3": "M3-L",
    "M4": "M4-L",
    "M5": "M5-L",
    "M8":  "M8-L",
    "M3圆柱钉": "M3-Y",
    "F":  "F"
}
colors = {
    "M3-P": "Navy",
    "M3-C": "green",
    "M4-P": "Navy",
    "M3-L": "blue",
    "M4-L": "purple",
    "M8-L": "black",
    "M5-L": "black",
    "F": "grey",
    "M3-Y": "blue"
}

sizes = {
    "M3-P": 26,
    "M3-Y": 25,
    "M3-C": 25,
    "M4-P": 31,
    "M3-L": 32,
    "M4-L": 34,
    "M8-L": 62,
    "M5-L": 55,
    "F": 35
}
# template
# sizes = {
#     "M3-P": 40,
#     "M3-Y": 40,
#     "M3-C": 40,
#     "M4-P": 55,
#     "M3-L": 45,
#     "M4-L": 55,
#     "M8-L": 85,
#     "M5-L": 65,
#     "F": 45
# }

def txt2img(file_path):
    print("start")
    with open(file_path) as f:
        lines = f.readlines()
        fig=plt.figure(figsize=(16,12)) #新建画布
        ax=plt.subplot(1,1,1) #子图初始化
        for i,line in enumerate(lines[1:-1]):
            arr = line.split("\t")
            ax.plot(float(arr[1]), float(arr[2]), 'o', color = "red")

            # plt.text(arr[1], arr[2], "hhh", size= 10, color = "green")
            ax.text(float(arr[1]), float(arr[2]), str(i) + "-" + types[arr[3].strip()], fontsize=8, color = colors[types[arr[3].strip()]], style = "italic", weight = "light", verticalalignment='top', horizontalalignment='left')

            # print(line)
    # plt.show()
    plt.savefig(file_path.split(".")[0] + ".png")
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

def perspective_transform(points, matrix):
    # 创建透视变换矩阵
    
    # 将坐标转换为齐次坐标
    points_homogeneous = np.concatenate([points, np.ones((points.shape[0], 1))], axis=1)
    # 进行透视变换
    transformed_points = np.dot(matrix, points_homogeneous.T).T
    # 将齐次坐标转换为二维坐标
    transformed_points = transformed_points[:, :2] / transformed_points[:, 2:]
    return transformed_points
# 将型号文件转成json
def txt2json(file_path, dst_name):    
    # WT-H1582Y 384 356 298 317
    # arr = [384, 298, 356, 317]
    # WT-1475
    arr = [64, 224, 118, 165]
    # 7451
    # arr = [284, 304, 183, 154]
    # 7480
    # arr = [433, 403, 475, 501]
    # 7524
    # arr = [218, 281, 510, 474]
    # for item in sizes:
    #     sizes[item] += 10
    print(dst_name)
    img = cv2.imread(dst_name.replace("json", "bmp"))
    h, w = img.shape[0]/2, img.shape[1]/2
    with open(file_path) as f:
        lines = f.readlines()[1:-1]
        ori_points = [[float(lines[i].split("\t")[1]), float(lines[i].split("\t")[2])] for i in arr]
    with open(dst_name, 'r', encoding= "utf-8") as f:
        dst_data = json.load(f)
    dst_dict = dict(dst_data)
    pts1 = get_points(dst_dict["shapes"][:4])
    pts1 = [[item[0] - w, item[1] - h] for item in pts1]
    matrix = cv2.getPerspectiveTransform(np.float32(ori_points),np.float32(pts1))
    # print(ori_dict["shapes"][0]["points"])
    # four_dict = dst_dict["shapes"][0:4]
    dst_dict["shapes"] = []
    
    for i, point in enumerate(lines):
        # if i in arr:
        #     continue
        item_ori = point.split("\t")
        x = float(item_ori[1])
        y = float(item_ori[2])
        size = sizes[types[item_ori[3].strip()]]
        res = perspective_transform(np.float32([[x, y]]), matrix)
        # print(res[0][0])
        # print(matrix)
        
        item = np.float32([
            [
                res[0][0] - size/2 + w,
                res[0][1] - size/2 + h
            ],
            [
                res[0][0] + size/2 + w,
                res[0][1] + size/2 + h
            ]
        ])
        
        dst_dict["shapes"].append({
            "points": item.tolist(),
            "label" : types[item_ori[3].strip()].split("-")[0] + "-K",
            "description": "",
            "shape_type": "rectangle",
            "flags": {}
            }
        )
    dst_dict["imageData"] = None
    # dst_dict["shapes"] = four_dict + dst_dict["shapes"]
    # print(ori_dict["shapes"][0]["points"])
    # image = cv2.imread(dst_name.replace("json", "bmp"))
    # _, buffer = cv2.imencode('.jpg', image)
    # dst_dict['imageData'] = base64.b64encode(buffer).decode('utf-8')
    # print(dst_dict)
    with codecs.open(dst_name, "w") as f:
        json.dump(dst_dict, f)
def replace_txt(file_path):
    res = ""
    with open(file_path) as f:
        lines = f.readlines()[1:-1]
        res += lines[0]
        for line in lines:
            arr = line.split("\t")
            if line.split("\t")[-1].strip() == "M3盘头钉":
                arr[3] = arr[3].replace("盘", "沉")
            res += "\t".join(arr)
            print(res)

    with open(file_path, "w+") as f1:
        f1.write(str(res))
    print(res)

def run(dir):
    for item in os.listdir(dir):
        print(item)
        if item.endswith("txt"): #and (item.split('.')[1] + ".png") not in os.listdir(dir):
            txt2img(os.path.join(dir, item))
if __name__ == "__main__":
    txt2json("腔体型号/1475.txt", "源数据/20230912/Image20230911/WT-H1475114/exp_800/temp/001.json")
    # txt2img("腔体型号/1475.txt")
    # replace_txt("腔体型号/WT-H7524Y.txt")