import os

# 指定源文件夹路径
source_folder = './test'

# 指定目标文件夹路径
target_folder = './dest'

# 遍历源文件夹中的文件
for filename in os.listdir(source_folder):
    # 获取文件扩展名
    extension = os.path.splitext(filename)[1]
    
    # 如果该文件是图片文件，则重命名并移动到目标文件夹
    if extension in ['.bmp', '.png', '.jpeg']:
        # 获取不带扩展名的文件名
        file_name = os.path.splitext(filename)[0]
        
        # 生成新的文件名，例如“new_filename.jpg”
        new_filename = f'new_{file_name}{222}{extension}'
        
        # 重命名文件
        os.rename(os.path.join(source_folder, filename), os.path.join(source_folder, new_filename))
        
        # 将文件移动到目标文件夹
        os.rename(os.path.join(source_folder, new_filename), os.path.join(target_folder, new_filename))