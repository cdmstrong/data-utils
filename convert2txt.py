import os
import json
from enum import Enum, unique
@unique
class ScrewType(Enum):
    N = 0
    C = 1
    P = 2
    K = 3

def convertLabel(label):
    ori = label.split("-")[1]
    return str(ScrewType[ori].value)


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
            f.write("\n" + str(i) + " " + str(x) + " " + str(y) + " " + convertLabel(item["label"]))

if __name__ == "__main__":
    convert("型号_1459/2200/1302562200.json")