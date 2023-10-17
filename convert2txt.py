import os
import json
from enum import Enum, unique
import codecs
import cv2
import shutil
@unique
class ScrewType(Enum):
    N = 0
    C3 = 1
    P3 = 2
    K3 = 3
    F = 6
    L3 = 9
    C4 = 11
    P4 = 12
    K4 = 13
    L4 = 14
    L5 = 15
    L8 = 16
    K5 = 17
    K8 = 18
    FK = 19

def convertLabel(label):
    if label == "F":
        return str(ScrewType[label].value)
    elif label == "F-K":
        return str(ScrewType[label.split("-")[0] + label.split("-")[1]].value)
    print(label)
    ori = label.split("-")[1]
    ori_size = any(c.isdigit() for c in label.split('-')[0])
    return str(ScrewType[ori + (str(label.split('-')[0][-1]) if ori_size else "")].value)

def parse(ori_path, filter_dir):
    print('----------------')
    print(ori_path) 
    if not os.path.exists(ori_path):
        os.mkdir(ori_path)
    for root, dirs, files in os.walk(ori_path):
        find = 0
        if root.split("/")[-1] in filter_dir:
            continue
        for i in filter_dir:
            print(i)
            if root.find(i) >= 0:
                find = 1
                break
        if find:
            continue
        # print(files)
        for file in files:
            if file.endswith("json"):
                print(f"转换file{file}")
                # convert(os.path.join(root, file))
                # move_dir(os.path.join(root, file), "源数据/20230927/WT-H1582Y-3/正面/")
                # remove_imgData(os.path.join(root, file))
                json2txt(os.path.join(root, file))
            # if file.endswith("bmp"):
                # move_slider(os.path.join(root, file),file)

def convert(file_path): 
    with open(file_path, "r", encoding = "utf-8") as f:
        data = json.load(f)
    data = dict(data)
    res_path = file_path.replace("json", "txt")
    print(res_path)
    with open(res_path, "w+", encoding= "utf-8") as f:
        f.write(str(len(data["shapes"])))
        shapes = data["shapes"]
        for i, item in enumerate(shapes):
            x = int((item["points"][1][0] + item["points"][0][0])/2)
            y = int((item["points"][1][1] + item["points"][0][1])/2)
            f.write("\n" + str(i) + " " + str(x) + " " + str(y) + " " + item["label"]) #convertLabel(item["label"]))
def json2txt(file_path):
    with open(file_path, "r", encoding = "utf-8") as f:
        data = json.load(f)
    data = dict(data)
    res_path = file_path.replace("json", "txt")
    print(res_path)
    img = cv2.imread(file_path.replace("json", "bmp"))
    img_w = img.shape[1]
    img_h = img.shape[0]
    with open(res_path, "w", encoding= "utf-8") as f:
        # f.write(str(len(data["shapes"])))
        shapes = data["shapes"]
        for i, item in enumerate(shapes):
            x = ((item["points"][1][0] + item["points"][0][0])/2)/img_w
            y = ((item["points"][1][1] + item["points"][0][1])/2)/img_h
            w = (item["points"][1][0] - item["points"][0][0])/img_w
            h = ((item["points"][1][1] + item["points"][0][1])/2)/img_h
            f.write(str(0) + " " + str(x) + " " + str(y) + " " + str(w) + " " + str(h) + "\n")
def move_dir(file_path, move_dir):
    res_path = file_path.replace("json", "txt")
    if res_path.find("20230908101037113") < 0:
            shutil.move(file_path.replace("json", "bmp"), os.path.join(move_dir, res_path.split("/")[-1].replace("txt", "bmp")))
            shutil.move(res_path, os.path.join(move_dir, res_path.split("/")[-1]))
            shutil.move(file_path, os.path.join(move_dir, file_path.split("/")[-1]))

def move_slider(file_path, move_dir):
    if os.path.getsize(file_path) < 1 * 1024 * 1024:
        shutil.move(file_path, os.path.join("源数据/20231007/new/1/侧面2/", move_dir))
    elif os.path.getsize(file_path) > 50 * 1024 * 1024:
        shutil.move(file_path, os.path.join("源数据/20231007/new/1/正面/", move_dir))
    else:
        shutil.move(file_path, os.path.join("源数据/20231007/new/1/侧面1/", move_dir))

def remove_imgData(file_path):
    with open(file_path, "r", encoding = "utf-8") as f:
        data = json.load(f)
    data = dict(data)
    data["imageData"] = None
    with codecs.open(file_path, "w") as f:
        json.dump(data, f)

if __name__ == "__main__":
    # convert("源数据/20230912/WT-H7451Y-正面/20230909135613774.json")
    parse("train_slider", [])
    # print(convertLabel("M3-K"))

    