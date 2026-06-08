# TopNote

[简体中文](README.md) | [繁體中文](README.zh-TW.md) | [English](README.en.md) | [日本語](README.ja.md)

一個簡單的 Windows 頂部下拉便條程式。滑鼠移到螢幕頂端中間的小觸發區時，便條會立即開始下拉動畫，支援多便條瀏覽、儲存、刪除、淺色/深色主題和系統匣常駐。

## 功能

- 滑鼠移到螢幕頂端中間立即開始下拉
- mac 風格圓角、輕量視覺介面
- 無邊框置頂視窗
- 支援拖曳調整頂部停靠位置
- 觸發把手會跟隨便條停靠位置和下拉動畫移動
- 支援左側列表瀏覽多條便條
- 支援新增、儲存、刪除和自動儲存
- 支援淺色/深色主題切換
- 工具按鈕全部使用小圖示顯示
- 系統匣選單支援顯示、隱藏、退出
- 圖釘按鈕可切換固定/自動收起

## 環境需求

- Windows 10/11
- Python 3.10 或更新版本

## 安裝

```powershell
conda activate topnote
pip install -r requirements.txt
```

## 執行

```powershell
python main.py
```

啟動後，螢幕頂端中間會有一個很細的小把手。把滑鼠移到那裡，便條會立即開始下拉動畫。

## 使用方式

- 左側列表：瀏覽和切換已儲存的便條
- 加號：建立一條空白便條
- 軟碟：立即儲存目前內容
- 垃圾桶：刪除目前便條
- 太陽/月亮：切換淺色/深色主題
- 圖釘：切換固定模式
- 拖曳標題列區域：調整便條在螢幕頂部的停靠位置
- 系統匣圖示右鍵：顯示、隱藏或退出

便條內容、目前選中的便條和主題會儲存到：

```text
%APPDATA%\TopNote\notes.json
```

## 打包為 exe

可以使用專案自帶的打包腳本：

```powershell
conda activate topnote
.\build.ps1
```

生成檔案位於：

```text
dist\TopNote.exe
```

也可以手動使用 PyInstaller：

```powershell
pip install pyinstaller
pyinstaller --noconsole --onefile --name TopNote main.py
```

打包後的 `TopNote.exe` 已包含 Python 執行環境和依賴，一般 Windows 電腦不需要再配置 conda，雙擊即可執行。

## 調整樣式

常用參數在 `main.py` 頂部：

- `NOTE_WIDTH`
- `NOTE_HEIGHT`
- `HOT_ZONE_HEIGHT`
- `AUTO_HIDE_DELAY_MS`

如果想讓介面更接近 macOS 的深色或毛玻璃風格，可以繼續調整樣式表中的背景色、邊框、陰影和字體。
