import cv2
import os
import glob
import re
import pandas as pd


df = pd.read_csv(r"C:\空打ち検証データ\ラベル.csv")
# csvの情報から動画のパスを取得するようにそれぞれの情報をリストに格納
Season = list(df["Season"])
Sutation = list(df["Station"])
FileName = list(df["FileName"])
Species = list(df["Species"])

# フレーム数をカウントするための変数
frame_number = 0
# 画像の枚数をカウントするための変数
image_file = 'img_%s.jpg'
# 動画の保存先
output_folder_base = "D:/images/"
# 動画の絶対パスを作る
abs_path_list = []
# 動画のパス（ハードディスク）
movie_path = "C:/空打ち検証データ"

# csvファイルから動画の絶対パスを作成
for season, sutation, file in zip(Season, Sutation, FileName):
    abs_path_list.append(movie_path + "/" + season +
                         "/" + sutation + "/" + file)

# 動画のパスを元に動画を読み込む
for index, path in enumerate(abs_path_list):
    # ラベル名＝動物の種類
    labels = Species[index]
    # ラベル名からフォルダを作成
    output_folder = output_folder_base + labels + "/"
    # そのフォルダ内の画像名を取得。
    images = glob.glob(f"{output_folder}*.jpg")

    # ファイルが存在してなかったら作る
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    # フォルダ内の画像枚数を取得。len()だと画像名が被るかもしれないか最後の像の番号を取得するためこの方法
    try:
        # 最後の画像を取得
        image_last = images[-1]
        # 正規表現で番号を取得
        image_number = re.sub(r"\D", "", image_last)
        image_number = int(image_number) + 1
    except IndexError:
        image_number = 1

    cap = cv2.VideoCapture(path)
    cpf = int(cap.get(cv2.CAP_PROP_FPS))  # cut par frame
    while cap.isOpened():
        frame_number += 1
        ret, frame = cap.read()
        if ret == False:
            break

        # 一秒に一回画像を取得
        if frame_number % cpf == 0:
            img_name = output_folder + image_file % str(image_number).zfill(3)
            cv2.imwrite(img_name, frame)  # Save a frame
            print('Save', img_name)
            image_number += 1
            break
    cap.release()
