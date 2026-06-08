# TopNote

[简体中文](README.md) | [繁體中文](README.zh-TW.md) | [English](README.en.md) | [日本語](README.ja.md)

TopNote は、Windows 向けのシンプルなトップドロップダウン型メモアプリです。画面上部中央の小さなハンドルにマウスを移動すると、メモがすぐに下へスライドし始めます。複数メモ、保存、削除、ライト/ダークテーマ、システムトレイ常駐に対応しています。

## 機能

- 画面上部中央のハンドルにマウスを移動するとすぐに下へスライド
- mac 風の角丸で軽量なインターフェース
- フレームレスの常に手前に表示されるウィンドウ
- ドラッグで画面上端のドッキング位置を調整
- ハンドルがメモの位置とスライドアニメーションに追従
- 左側リストで複数の保存済みメモを閲覧
- 新規作成、保存、削除、自動保存に対応
- ライト/ダークテーマ切り替え
- ツールボタンはすべて小さなアイコン表示
- システムトレイメニューで表示、非表示、終了
- ピンボタンで固定/自動収納を切り替え

## 必要環境

- Windows 10/11
- Python 3.10 以降

## インストール

```powershell
conda activate topnote
pip install -r requirements.txt
```

## 実行

```powershell
python main.py
```

起動後、画面上部中央に細いハンドルが表示されます。そこへマウスを移動すると、メモがすぐに下へスライドし始めます。

## 使い方

- 左側リスト：保存済みメモの閲覧と切り替え
- プラス：空のメモを作成
- フロッピーディスク：現在の内容をすぐに保存
- ゴミ箱：現在のメモを削除
- 太陽/月：ライト/ダークテーマを切り替え
- ピン：固定モードを切り替え
- タイトルバー領域をドラッグ：画面上部でのドッキング位置を調整
- トレイアイコンを右クリック：表示、非表示、終了

メモ内容、現在選択中のメモ、テーマは以下に保存されます：

```text
%APPDATA%\TopNote\notes.json
```

## exe のビルド

同梱のビルドスクリプトを使用できます：

```powershell
conda activate topnote
.\build.ps1
```

生成されるファイル：

```text
dist\TopNote.exe
```

PyInstaller を手動で実行することもできます：

```powershell
pip install pyinstaller
pyinstaller --noconsole --onefile --name TopNote main.py
```

パッケージ化された `TopNote.exe` には Python 実行環境と必要な依存関係が含まれます。他の Windows PC では conda や pip の設定は不要で、exe をダブルクリックすれば実行できます。

## カスタマイズ

よく調整する設定は `main.py` の上部にあります：

- `NOTE_WIDTH`
- `NOTE_HEIGHT`
- `HOT_ZONE_HEIGHT`
- `AUTO_HIDE_DELAY_MS`

macOS のダークテーマやガラス風の見た目に近づけたい場合は、`main.py` 内のスタイルシートの背景色、境界線、影、フォントを調整してください。
