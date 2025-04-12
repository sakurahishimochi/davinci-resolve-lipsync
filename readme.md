# DaVinci Resolve Lipsync

DaVinci Resolve のプロジェクト上にメディアファイルを読み込み、歌メロディの MIDI データと、歌詞をローマ字表記のカナで書き起こしたデータを組み合わせて、リップシンクアニメーションのタイムラインを作成する Python スクリプトです。

メディアファイルの内容は、`res` ディレクトリ以下のサンプルデータを参考にしてください。

## 動作要件

- DaVinci Resolve 16 以降
- Python 3.12
  - DaVinci Resolve の Scripting ライブラリへのパスが通っていること
  - 依存パッケージ: mido 1.3 系
- 環境変数 `RESOLVE_SCRIPT_LIB`・`RESOLVE_SCRIPT_API` が適切に設定されていること

## 使い方

- DaVinci Resolve を起動し、プロジェクトを作成する
- プロジェクトのフレームレートなどを設定する
- プロジェクトを開いた状態で `python3 run.py [res/resoureces.json のキー名]` を実行する
- プロジェクト上にアニメーションのタイムラインが作成されたことを確認し、必要に応じて背景などのトラックを追加する

## サンプルデータについて

サンプルデータは私的な利用のみ許可します。二次配布は禁止です。
