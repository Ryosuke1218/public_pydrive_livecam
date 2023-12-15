import os

if os.name == 'nt':
    os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"

import cv2
import time
from cv2 import aruco

dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters()
input_file = "source.png"


def capture_uproad(cap_instance):
    # 時間計測
    time_start = time.perf_counter()
    diff_time = 0

    # オートフォーカスやホワイトバランスの調整時間を考慮して、5秒間キャプチャを続ける
    while diff_time < 5:
        _, source = cap_instance.read()

        time_now = time.perf_counter()
        diff_time = time_now - time_start

    # 画像を保存
    cv2.imwrite('source.png', source)
    input_img = cv2.imread(input_file)
    # ノイズの除去
    blurred = cv2.GaussianBlur(input_img, (5, 5), 0)

    # 明るさやコントラストの調整
    adjusted = cv2.convertScaleAbs(blurred, alpha=1.2, beta=50)

    # エッジ検出
    edges = cv2.Canny(adjusted, threshold1=30, threshold2=100)
    cv2.imwrite('edges.png', edges)

    corners, ids, rejectedCandidates = aruco.detectMarkers(edges, dictionary, parameters=parameters)
    print(ids)
    if ids is not None:
        print("AR markar is detected.")
        for id in ids:
            if id[0] == 0:
                print("Marker 0 detected. This is a special marker.")
            else:
                print(f"Marker {id[0]} detected.")
    else:
        print("AR markar is not detected.")

# def run_threaded(cap_instance):
#     job_thread = threading.Thread(target=capture_uproad, args=(cap_instance))
#     job_thread.start()


def main():

    # カメラの起動
    cap = cv2.VideoCapture(1)

    # カメラの設定
    print(cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280))
    print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # 現在の画像をアップロード
    while True:
        capture_uproad(cap_instance=cap)
        time.sleep(10)
    # スケジュールの設定
    # schedule.every(10).seconds.do(run_threaded, cap_instance=cap)
    
    # スケジュールの実行
    # while True:
        # schedule.run_pending()
        # time.sleep(1)


if __name__ == '__main__':
    main()