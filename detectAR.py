import cv2
from cv2 import aruco
import numpy as np
import os
import time

# マーカーの保存先
dir_mark = "./marker"

# 生成するマーカーの種類
# サイズ：4x4~7x7,  枚数：50,100,250,1000
marker_type = aruco.DICT_4X4_50

# 生成するマーカー用のパラメータ
marker_num = 20      # 個数
marker_size = 1000   # マーカーのサイズ

# 余白[%]
margin_right = 0.1
margin_left = 0.1
margin_top = 0.1
margin_bottom = 0.1

# id のプリント
font_size = 1

# ディレクトリ作成
os.makedirs(dir_mark, exist_ok=True)

# マーカー種類を呼び出し
dict_aruco = aruco.getPredefinedDictionary(marker_type)

class ArucoDetector:
    def __init__(self):
        pass

    def detectMarkers(self, cap):
        # ret: bool型の変数, True: 成功, False: 失敗, frame: ndarray型の変数で、フレームのデータを格納
        ret, frame = cap.read()
        size = frame.shape

        focal_length = size[1]
        center = (size[1]/2, size[0]/2)

        fx, fy, cx, cy = focal_length, focal_length, center[0], center[1]
        cameraMatrix = np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]])
        k1, k2, p1, p2 = 0, 0, 0, 0
        distCoeff = np.array([[k1, k2, p1, p2]])
        distCoeff = np.zeros((4, 1))

        detector = aruco.ArucoDetector(dict_aruco)

        # 動画終了まで、1フレームずつ読み込んで表示する。
        while (cap.isOpened()):  # 1フレーム毎　読込み
            ret, frame = cap.read()

            corners, ids, rejectedCandidates = detector.detectMarkers(frame)

            if len(corners) > 0:
                for points, id in zip(corners, ids):

                    image_points_2D = np.array(points[0], dtype="double")   # 画像上の座標(マーカー認識の結果)
                    figure_points_3D = np.array([   # 画像上の点の３次元空間での座標
                                    (0.5, 0.5, 0.0),
                                    (0.5, -0.5, 0.0),
                                    (-0.5, -0.5, 0.0),
                                    (-0.5, 0.5, 0.0),
                                ])
                
                    objPoints = image_points_2D
                    # 上記を対応させて姿勢などを算出する
                    suc, rvec, tvec = cv2.solvePnP(figure_points_3D, image_points_2D, cameraMatrix, distCoeff)
                    distance = np.sqrt(tvec[0]**2 + tvec[1]**2 + tvec[2]**2)
                    print(f"{distance=}")
                    time.sleep(1)
                    cv2.polylines(frame, np.array(points).astype(int), isClosed=True, color=(0, 255, 0), thickness=1)
                    cv2.drawMarker(frame, np.array(points[0][0]).astype(int), color=(255, 0, 255), markerType=cv2.MARKER_SQUARE, thickness=1, markerSize=10)
                    cv2.putText(frame, str(id[0]), np.array(points[0][0]).astype(int), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.0, color=(255, 0, 0), thickness=2, lineType=cv2.LINE_AA)

                    # 高さにあたる辺の描画
                    for point2, point3 in zip(image_points_2D, figure_points_3D):

                        end_point3D = point3+np.array([[0, 0, 1]])
                        start_point2D = np.array([[point2]])

                        end_point2D, jacobian = cv2.projectPoints(end_point3D, rvec, tvec, cameraMatrix, distCoeff)

                        point1 = (int(start_point2D[0][0][0]), int(start_point2D[0][0][1]))
                        point2 = (int(end_point2D[0][0][0]), int(end_point2D[0][0][1]))

                        cv2.line(frame, point1, point2, (0, 255, 0), 1)

                    # 上面に対応する辺の描画
                    for i in range(4):
                        end_point3D = figure_points_3D[i]+np.array([[0, 0, 1]])     # [[-0.5  0.5  1. ]]
                        end_point2D, jacobian = cv2.projectPoints(end_point3D, rvec, tvec, cameraMatrix, distCoeff)
                        point1 = (int(end_point2D[0][0][0]), int(end_point2D[0][0][1]))
                        
                        start_point3D = figure_points_3D[(i+1) % 4]+np.array([[0, 0, 1]])
                        start_point2D, jacobian = cv2.projectPoints(start_point3D, rvec, tvec, cameraMatrix, distCoeff)
                        point2 = (int(start_point2D[0][0][0]), int(start_point2D[0][0][1]))

                        cv2.line(frame, point1, point2, (0, 255, 0), 1)

                        if i == 0:
                            cv2.drawMarker(frame, point1, color=(255, 255), markerType=cv2.MARKER_SQUARE, thickness=1, markerSize=10)

            # GUIに表示
            cv2.imshow("Camera", frame)
            # qキーが押されたら途中終了
            if cv2.waitKey(1) == ord('q'):
                break


if __name__ == "__main__":
    cap = cv2.VideoCapture(1)
    ad = ArucoDetector()
    ad.detectMarkers(cap)

    # 終了処理
    cap.release()
    cv2.destroyAllWindows() 
