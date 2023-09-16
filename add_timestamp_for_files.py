import pdb

import os
import glob
from PIL import Image
from datetime import datetime


#----- PARAMETERS -----#
# フォルダのパスとファイル名のパターン指定
folder_path = os.getcwd()
file_pattern = "DSC*.*"

# 画像ファイルと動画ファイルの拡張子リスト
image_extensions = [".jpg", ".jpeg", ".png", ".gif", '.JPG']
video_extensions = [".mp4", ".wmv", ".3gp"]
#----------------------#


def get_capture_date(file_path):
    try:
        with Image.open(file_path) as image:
            if hasattr(image, "_getexif"):
                exif = image._getexif()
                if exif is not None and 36867 in exif:
                    capture_date = exif[36867]
                    capture_datetime = datetime.strptime(capture_date, "%Y:%m:%d %H:%M:%S")
                    return capture_datetime.strftime("%Y-%m-%d")
                
    except (IOError, AttributeError, KeyError, ValueError):
        print('IO Error!')
        print(file_path)
        pdb.set_trace()

    return None


def add_timestamp_for_files():
    # フォルダ内のファイルを取得
    file_list = glob.glob(os.path.join(folder_path, file_pattern))

    for file_path in file_list:
        # 拡張子を取得
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()

        # 画像ファイルの場合, 撮影日時を取得
        if ext in image_extensions:
            date_str = get_capture_date(file_path)
        # 動画ファイルの場合, 撮影日時の取得は ffprobe 周りが面倒そうなので更新日時の取得で妥協
        elif ext in video_extensions:
            mtime = os.path.getmtime(file_path)
            date_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")
        else:
            continue
        
        if date_str is None:
            continue

        # 新しいファイル名を生成
        file_name = os.path.basename(file_path)
        new_file_name = f"{date_str}_{file_name}"
        
        # 新しいファイル名に変更
        try:
            new_file_path = os.path.join(folder_path, new_file_name)
            os.rename(file_path, new_file_path)
        except:
            new_file_path = os.path.join(folder_path, file_name)
            os.rename(file_path, new_file_path)


# 実行
if __name__ == '__main__':
    add_timestamp_for_files()