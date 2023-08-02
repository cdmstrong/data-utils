import json
import os
import codecs
import shutil
def merge_json(up_dir, down_dir, dst_dir):
   if not os.path.exists(dst_dir):
      os.mkdir(dst_dir)
   for item in os.listdir(up_dir):
    if not item.endswith(".json"):
       continue
    up_path = os.path.join(up_dir, item)
    down_path = os.path.join(down_dir, item)
    if os.path.isdir(up_path):
        continue
    with open(up_path, "r", encoding= "utf-8") as f:
        up_data = json.load(f)
    with open(down_path, 'r', encoding= "utf-8") as f:
        down_data = json.load(f)
        # 解析为字典
    up_dict = dict(up_data)
    down_dict = dict(down_data)
    up_dict["shapes"] = up_dict["shapes"] + down_dict["shapes"]
    with codecs.open(os.path.join(dst_dir, item), "w") as f:
        json.dump(up_dict, f)
    shutil.copy(up_path.replace("json", "bmp"), os.path.join(dst_dir, item).replace("json", "bmp"))

if __name__ == "__main__":
   merge_json("型号_1516/2200/kong", "型号_1516/2200/kong/down", "型号_1516/2200/kong/merge")