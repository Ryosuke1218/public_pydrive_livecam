# pydrive_livecam

一定時間ごとにUSBカメラから画像を取得し，Google Driveにアップロードするプログラム．

## Required libraries

- [PyDrive2](https://github.com/iterative/PyDrive2)
- opencv-python
- schedule

## Setup

1. Google Drive APIを有効化し，認証情報を取得する．
2. configディレクトリを作成し，認証情報のJSONファイルを`config/client_secrets.json`として保存する．
3. authentication.pyを実行し，認証を行う．
