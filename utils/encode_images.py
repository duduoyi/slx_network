import os
import base64


# 定义一个函数来批量读取和编码图片
def encode_images_from_assets(assets_folder="assets/school_logo"):
    encoded_images = {}
    for filename in os.listdir(assets_folder):
        # 只处理图片文件（根据文件扩展名）
        if filename.endswith((".png", ".jpg", ".jpeg")):
            file_path = os.path.join(assets_folder, filename)
            with open(file_path, "rb") as f:
                encoded_images[filename] = base64.b64encode(f.read()).decode('utf-8')
    return encoded_images