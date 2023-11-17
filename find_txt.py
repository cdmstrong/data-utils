import os

def find(file_path):
    for item in os.listdir(file_path):
        val_path = os.path.join("train_slider/train/labels", item.replace("bmp", "txt"))
        if not os.path.exists(val_path):
            print(f"{val_path} txt is not exits")

if __name__ == "__main__":
    find("train_slider/train/images")
