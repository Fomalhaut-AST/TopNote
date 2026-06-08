# TopNote

[简体中文](README.md) | [繁體中文](README.zh-TW.md) | [English](README.en.md) | [日本語](README.ja.md)

一个简单的 Windows 顶部下拉便签程序。鼠标移动到屏幕顶端中间的小热区时，便签会立即开始下拉动画，支持多便签浏览、保存、删除、黑白主题和系统托盘常驻。

## 功能

- 鼠标移到屏幕顶端中间立即开始下拉
- mac 风格圆角、轻阴影、半透明界面
- 无边框置顶窗口
- 支持拖动调整顶部停靠位置
- 触发条会跟随便签停靠位置和下拉动画移动
- 支持左侧列表浏览多条便签
- 支持新建、保存、删除和自动保存
- 支持浅色/深色主题切换
- 工具按钮全部使用小图标显示
- 系统托盘菜单支持显示、隐藏、退出
- 图钉按钮可切换固定/自动收起

## 环境要求

- Windows 10/11
- Python 3.10 或更新版本

## 安装

```powershell
conda activate topnote
pip install -r requirements.txt
```

## 运行

```powershell
python main.py
```

启动后，屏幕顶端中间会有一个非常细的小触发条。把鼠标移到那里，便签会立即开始下拉动画。

## 使用说明

- 左侧列表：浏览和切换已保存的便签
- 加号：创建一条空白便签
- 软盘：立即保存当前内容
- 垃圾桶：删除当前便签
- 太阳/月亮：切换浅色/深色主题
- 图钉：切换固定模式
- 拖动标题栏区域：调整便签在屏幕顶部的停靠位置
- 托盘图标右键：显示、隐藏或退出

便签内容、当前选中便签和主题会保存到：

```text
%APPDATA%\TopNote\notes.json
```

## 打包为 exe

可以使用项目自带的打包脚本：

```powershell
conda activate topnote
.\build.ps1
```

生成文件位于：

```text
dist\TopNote.exe
```

也可以手动使用 PyInstaller：

```powershell
pip install pyinstaller
pyinstaller --noconsole --onefile --name TopNote main.py
```

生成文件位于：

```text
dist\TopNote.exe
```

打包后的 `TopNote.exe` 已经包含 Python 运行环境和依赖，普通 Windows 电脑不需要再配置 conda 环境，双击即可运行。

## 调整样式

常用参数在 `main.py` 顶部：

- `NOTE_WIDTH`
- `NOTE_HEIGHT`
- `HOT_ZONE_HEIGHT`
- `AUTO_HIDE_DELAY_MS`

如果想要更接近 macOS 的深色或毛玻璃风格，可以继续调整样式表中的背景色、边框、阴影和字体。
