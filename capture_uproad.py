# cv2のインポート前にカメラに関する設定を行う
# https://github.com/opencv/opencv/issues/17687
import os

if os.name == 'nt':
    os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"

import cv2
import time
import datetime
import schedule
import threading
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

FILE_ID = '***'

# 文字背景の透過処理
def add_text_to_image(img, text):
    copy_img = img.copy()
    mat_color = (200, 200, 200)
    cv2.rectangle(copy_img, (0, 0), (380, 50), mat_color, -1)
    weighted_img = cv2.addWeighted(copy_img, 0.4, img, 0.6, 0)
    cv2.putText(weighted_img, text=text, org=(10, 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 0, 0), thickness=2, lineType=cv2.LINE_AA)
    return weighted_img

def capture_uproad(drive_instance, cap_instance):
    # 時間計測
    time_start = time.perf_counter()
    diff_time = 0

    # オートフォーカスやホワイトバランスの調整時間を考慮して、5秒間キャプチャを続ける
    while diff_time < 5:
        _, source = cap_instance.read()

        time_now = time.perf_counter()
        diff_time = time_now - time_start

    # 画像に日付と時間を追加
    dt_now = datetime.datetime.now()
    dt_str = dt_now.strftime('%Y/%m/%d %H:%M:%S')
    weighted_image = add_text_to_image(source, dt_str)

    # 画像を保存
    cv2.imwrite('source.png', weighted_image)

    # Google Driveにアップロード
    file_1 = drive_instance.CreateFile({'id': FILE_ID})
    file_1.SetContentFile('./source.png')
    file_1.Upload()
    print('{} Upload file to Google Drive' .format(dt_str))

def run_threaded(drive_instance, cap_instance):
    job_thread = threading.Thread(target=capture_uproad, args=(drive_instance, cap_instance))
    job_thread.start()

def main():
    # Google Driveへの接続
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    # カメラの起動
    cap = cv2.VideoCapture(1)

    # カメラの設定
    print(cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280))
    print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # 現在の画像をアップロード
    capture_uproad(drive_instance=drive, cap_instance=cap)

    # スケジュールの設定
    schedule.every(30).seconds.do(run_threaded, drive_instance=drive, cap_instance=cap)
    
    # スケジュールの実行
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()