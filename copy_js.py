import os
import shutil
import json
import codecs
def copy(file_path, dst_path):
    ori_path = "源数据/20231007/new/1/正面/20230927142722892.json"
    shutil.copy(ori_path, dst_path)
    with open(dst_path, 'r', encoding= "utf-8") as f:
        data = json.load(f)
    data["imagePath"] = file_path
    with codecs.open(dst_path, "w") as f:
        json.dump(data, f)
def run(dir_path):
    for item in os.listdir(dir_path):
        dst_path = os.path.join(dir_path, item).replace("bmp", "json")
        if item.endswith("json"):
            continue
        elif os.path.exists(dst_path):
            continue
        copy(item, dst_path)


if __name__ == "__main__":
    run("源数据/20231007/new/1/正面")