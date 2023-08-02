import os
import shutil
# 参考文件夹 search——path
# dst_path 源文件的文件夹
# 目标文件夹 
# 参考文件夹原名
# 目标文件夹 的文件名
def move_file(search_path, ori_path, dst_path, old_name, replace_name):
    if os.path.exists(dst_path):
        os.mkdir(dst_path)
    for item in os.listdir(search_path):
        dst_file = item.replace(old_name, replace_name)
        ori_file = os.path.join(ori_path, dst_file)
        if os.path.exists(ori_file):
            shutil.move(ori_file, os.path.join(dst_path, dst_file))


if __name__ == "__main__":
    move_file("型号_1516/2000/kong", "型号_1516/2800", "型号_1516/2800/kong", str(2000), str(2800))