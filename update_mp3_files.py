import pdb

import os
from mutagen.id3 import ID3, TIT2, TRCK, TALB, TYER, TPE1


#----- PARAMETERS -----#
folder_path = os.getcwd()
album_name = 'xxx'
artist_name = 'yyy'
year = 2023
order = 'update_time' # 連番を与える基準を更新日時順(update_time)または名前順(name)で指定
#----------------------#


# 指定されたフォルダ内の MP3 ファイルを取得
def get_files(folder_path, order):
    # 名前順で取得
    if order == 'name':
        files = sorted([f for f in os.listdir(folder_path) if f.endswith('.mp3')],
                        key=lambda f: f)
    # 更新日時順で取得
    elif order == 'update_time':
        files = sorted([f for f in os.listdir(folder_path) if f.endswith('.mp3')],
                        key=lambda f: os.path.getmtime(os.path.join(folder_path, f)))
    
    return files


# トラックナンバーのリストを作成
def get_track_number_list(files):
    return [i for i in range(1, len(files) + 1)]


# MP3 ファイルのアップデート
def update_mp3_file(folder_path, album_name, year, order):
    files = get_files(folder_path, order)
    track_number_l = get_track_number_list(files)

    for file_name, track_number in zip(files, track_number_l):
        file_path = os.path.join(folder_path, file_name)

        # ファイルのプロパティを変更
        audio = ID3(file_path)
        title = file_name.split('.')[0]
        audio['TIT2'] = TIT2(encoding=3, text=title)              # タイトルを設定
        audio['TRCK'] = TRCK(encoding=3, text=str(track_number))  # トラック番号を設定
        audio['TALB'] = TALB(encoding=3, text=album_name)         # アルバム名を設定
        audio['TPE1'] = TPE1(encoding=3, text=artist_name)        # アーティスト名を設定
        audio['TYER'] = TYER(encoding=3, text=str(year))          # 年を設定
        audio.save()                                              # 保存

        # ファイル名の前に2桁の連番を追加
        # 例えば「xxx.mp3」を「01 xxx.mp3」のように変更する
        new_file_name = f"{track_number:02d} {file_name}"
        new_file_path = os.path.join(folder_path, new_file_name)
        os.rename(file_path, new_file_path)


# 実行
if __name__ == '__main__':
    update_mp3_file(folder_path, album_name, year, order)