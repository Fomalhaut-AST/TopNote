# TopNote

[简体中文](README.md) | [繁體中文](README.zh-TW.md) | [English](README.en.md) | [日本語](README.ja.md)

TopNote is a small Windows sticky note app that drops down from the top of the screen. Move your mouse to the small handle at the top center of the screen, and the note starts sliding down immediately. It supports multiple notes, save/delete actions, light/dark themes, and a system tray menu.

## Features

- Immediate drop-down animation when the mouse reaches the top-center handle
- mac-inspired rounded, lightweight interface
- Frameless always-on-top window
- Drag to adjust the docked position along the top edge
- The handle follows the note position and the slide animation
- Browse multiple saved notes from the left sidebar
- Create, save, delete, and auto-save notes
- Light/dark theme switch
- Icon-only tool buttons
- System tray menu for show, hide, and quit
- Pin button to keep the note open or allow auto-hide

## Requirements

- Windows 10/11
- Python 3.10 or newer

## Install

```powershell
conda activate topnote
pip install -r requirements.txt
```

## Run

```powershell
python main.py
```

After launch, a slim handle appears at the top center of the screen. Move your mouse there to start the drop-down animation.

## Usage

- Left sidebar: browse and switch saved notes
- Plus: create a blank note
- Floppy disk: save the current note immediately
- Trash: delete the current note
- Sun/moon: switch between light and dark themes
- Pin: toggle pinned mode
- Drag the title bar area: adjust the note's docked position along the top of the screen
- Right-click the tray icon: show, hide, or quit

Notes, current selection, and theme are saved to:

```text
%APPDATA%\TopNote\notes.json
```

## Build an exe

Use the included build script:

```powershell
conda activate topnote
.\build.ps1
```

The output file will be:

```text
dist\TopNote.exe
```

You can also run PyInstaller manually:

```powershell
pip install pyinstaller
pyinstaller --noconsole --onefile --name TopNote main.py
```

The packaged `TopNote.exe` includes Python and the required dependencies. Other Windows PCs do not need conda or pip; double-click the exe to run it.

## Customize

Common settings live near the top of `main.py`:

- `NOTE_WIDTH`
- `NOTE_HEIGHT`
- `HOT_ZONE_HEIGHT`
- `AUTO_HIDE_DELAY_MS`

To make the interface closer to a macOS dark or glass-like style, adjust the stylesheet colors, borders, shadows, and fonts in `main.py`.
