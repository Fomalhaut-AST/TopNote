import json
import sys
import time
import ctypes
from pathlib import Path

from PySide6.QtCore import QEasingCurve, QPoint, QPropertyAnimation, QRect, QSize, QTimer, Qt, Signal
from PySide6.QtGui import QAction, QColor, QCursor, QFont, QIcon, QPainter, QPainterPath, QPixmap, QPolygon
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMenu,
    QPlainTextEdit,
    QPushButton,
    QSystemTrayIcon,
    QVBoxLayout,
    QWidget,
)


APP_NAME = "TopNote"
NOTE_WIDTH = 680
NOTE_HEIGHT = 440
HOT_ZONE_WIDTH = NOTE_WIDTH
HOT_ZONE_HEIGHT = 24
AUTO_HIDE_DELAY_MS = 120
SAVE_DEBOUNCE_MS = 500
SHOW_ANIMATION_MS = 190
HIDE_ANIMATION_MS = 180
DEFAULT_NOTE_ID = "inbox"
DWMWA_BORDER_COLOR = 34
DWMWA_COLOR_NONE = 0xFFFFFFFE


THEMES = {
    "light": {
        "card": "rgba(246, 246, 247, 255)",
        "sidebar": "rgba(235, 235, 237, 205)",
        "editor": "rgba(255, 255, 255, 210)",
        "editor_focus": "rgba(255, 255, 255, 235)",
        "text": "#202124",
        "muted": "rgba(60, 60, 67, 150)",
        "border": "rgba(0, 0, 0, 18)",
        "button": "rgba(255, 255, 255, 150)",
        "button_hover": "rgba(255, 255, 255, 220)",
        "active_item": "rgba(0, 122, 255, 35)",
        "hover_item": "rgba(0, 0, 0, 14)",
        "accent": "#007aff",
    },
    "dark": {
        "card": "rgba(31, 31, 34, 255)",
        "sidebar": "rgba(22, 22, 24, 210)",
        "editor": "rgba(43, 43, 47, 220)",
        "editor_focus": "rgba(49, 49, 54, 235)",
        "text": "#f3f3f4",
        "muted": "rgba(235, 235, 245, 135)",
        "border": "rgba(255, 255, 255, 18)",
        "button": "rgba(255, 255, 255, 8)",
        "button_hover": "rgba(255, 255, 255, 18)",
        "active_item": "rgba(10, 132, 255, 55)",
        "hover_item": "rgba(255, 255, 255, 10)",
        "accent": "#0a84ff",
    },
}


def app_data_file() -> Path:
    app_data = Path.home() / "AppData" / "Roaming"
    note_dir = app_data / APP_NAME
    note_dir.mkdir(parents=True, exist_ok=True)
    return note_dir / "notes.json"


def remove_native_border(widget: QWidget):
    if not sys.platform.startswith("win"):
        return
    try:
        hwnd = int(widget.winId())
        color = ctypes.c_uint(DWMWA_COLOR_NONE)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            ctypes.c_void_p(hwnd),
            ctypes.c_uint(DWMWA_BORDER_COLOR),
            ctypes.byref(color),
            ctypes.sizeof(color),
        )
    except Exception:
        pass


def make_tray_icon() -> QIcon:
    pixmap = QPixmap(64, 64)
    pixmap.fill(Qt.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setPen(Qt.NoPen)
    painter.setBrush(QColor("#f8d66d"))
    painter.drawRoundedRect(10, 8, 44, 48, 10, 10)
    painter.setBrush(QColor("#fff4bf"))
    painter.drawRoundedRect(16, 15, 32, 7, 3, 3)
    painter.drawRoundedRect(16, 28, 26, 6, 3, 3)
    painter.end()

    return QIcon(pixmap)


def make_action_icon(name: str, color: QColor) -> QIcon:
    pixmap = QPixmap(48, 48)
    pixmap.fill(Qt.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setPen(color)
    painter.setBrush(Qt.NoBrush)

    if name == "pin":
        painter.setPen(Qt.NoPen)
        painter.setBrush(color)
        painter.drawRoundedRect(18, 8, 14, 18, 4, 4)
        painter.drawPolygon(QPolygon([QPoint(15, 24), QPoint(35, 24), QPoint(24, 35)]))
        painter.setPen(color)
        painter.drawLine(24, 32, 24, 42)
    elif name == "save":
        painter.setPen(color)
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(11, 9, 26, 30, 4, 4)
        painter.drawLine(17, 9, 17, 20)
        painter.drawLine(30, 9, 30, 19)
        painter.drawRoundedRect(17, 27, 14, 8, 2, 2)
    elif name == "sun":
        painter.drawEllipse(18, 18, 12, 12)
        for x1, y1, x2, y2 in [
            (24, 5, 24, 12),
            (24, 36, 24, 43),
            (5, 24, 12, 24),
            (36, 24, 43, 24),
            (10, 10, 15, 15),
            (33, 33, 38, 38),
            (38, 10, 33, 15),
            (15, 33, 10, 38),
        ]:
            painter.drawLine(x1, y1, x2, y2)
    elif name == "moon":
        painter.setPen(Qt.NoPen)
        painter.setBrush(color)
        painter.drawEllipse(13, 9, 25, 30)
        painter.setBrush(QColor(0, 0, 0, 0))
        painter.setCompositionMode(QPainter.CompositionMode_Clear)
        painter.drawEllipse(23, 6, 23, 30)
        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
    elif name == "trash":
        painter.drawLine(15, 16, 33, 16)
        painter.drawLine(20, 11, 28, 11)
        painter.drawRoundedRect(17, 18, 14, 20, 3, 3)
        painter.drawLine(21, 22, 21, 34)
        painter.drawLine(27, 22, 27, 34)
    elif name == "plus":
        painter.drawLine(24, 13, 24, 35)
        painter.drawLine(13, 24, 35, 24)

    painter.end()
    return QIcon(pixmap)


class IconButton(QPushButton):
    def __init__(self, tooltip: str):
        super().__init__()
        self.setToolTip(tooltip)
        self.setFixedSize(32, 30)
        self.setIconSize(QSize(18, 18))
        self.setCursor(Qt.PointingHandCursor)


class HotZone(QWidget):
    activated = Signal()

    def __init__(self):
        super().__init__()
        self.handle_color = QColor(31, 31, 34, 255)
        self.grip_color = QColor(170, 170, 178, 120)
        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.Tool
            | Qt.WindowStaysOnTopHint
            | Qt.WindowDoesNotAcceptFocus
            | Qt.NoDropShadowWindowHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(HOT_ZONE_WIDTH, HOT_ZONE_HEIGHT)
        remove_native_border(self)
        self.place_at_top_center()
        self.poll_timer = QTimer(self)
        self.poll_timer.timeout.connect(self.check_cursor)
        self.poll_timer.start(35)

    def place_at_top_center(self):
        screen = QApplication.primaryScreen().availableGeometry()
        x = screen.x() + (screen.width() - HOT_ZONE_WIDTH) // 2
        self.setGeometry(x, screen.y(), HOT_ZONE_WIDTH, HOT_ZONE_HEIGHT)

    def follow_note(self, note_geometry: QRect):
        screen = QApplication.screenAt(note_geometry.center()) or QApplication.primaryScreen()
        screen_top = screen.geometry().y()
        x = note_geometry.x()
        y = max(note_geometry.y() + note_geometry.height(), screen_top)
        self.setGeometry(x, y, HOT_ZONE_WIDTH, HOT_ZONE_HEIGHT)
        self.raise_()

    def set_theme(self, theme_name: str):
        if theme_name == "light":
            self.handle_color = QColor(246, 246, 247, 255)
            self.grip_color = QColor(95, 95, 105, 115)
        else:
            self.handle_color = QColor(31, 31, 34, 255)
            self.grip_color = QColor(170, 170, 178, 120)
        self.update()

    def enterEvent(self, event):
        self.raise_()
        self.activated.emit()
        super().enterEvent(event)

    def check_cursor(self):
        screen = QApplication.screenAt(self.geometry().center()) or QApplication.primaryScreen()
        if self.y() <= screen.geometry().y() + 2 and self.geometry().contains(QCursor.pos()):
            self.activated.emit()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        tab_width = 96
        tab_height = 22
        radius = 8
        tab_x = (HOT_ZONE_WIDTH - tab_width) // 2
        tab_y = 0

        path = QPainterPath()
        path.moveTo(tab_x, tab_y)
        path.lineTo(tab_x + tab_width, tab_y)
        path.lineTo(tab_x + tab_width, tab_y + tab_height - radius)
        path.quadTo(
            tab_x + tab_width,
            tab_y + tab_height,
            tab_x + tab_width - radius,
            tab_y + tab_height,
        )
        path.lineTo(tab_x + radius, tab_y + tab_height)
        path.quadTo(tab_x, tab_y + tab_height, tab_x, tab_y + tab_height - radius)
        path.lineTo(tab_x, tab_y)

        painter.fillPath(path, self.handle_color)
        painter.setBrush(self.grip_color)
        painter.drawRoundedRect(tab_x + 31, tab_y + 12, tab_width - 62, 4, 2, 2)
        painter.end()
        super().paintEvent(event)


class NoteWindow(QWidget):
    hidden_finished = Signal()
    handle_geometry_changed = Signal(QRect)
    theme_changed = Signal(str)

    def __init__(self):
        super().__init__()
        self.note_file = app_data_file()
        self.pinned = False
        self.drag_offset = None
        self.shown_geometry = QRect()
        self.hidden_geometry = QRect()
        self.notes = []
        self.current_note_id = DEFAULT_NOTE_ID
        self.theme_name = "light"
        self.loading_note = False

        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.Tool
            | Qt.WindowStaysOnTopHint
            | Qt.NoDropShadowWindowHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(NOTE_WIDTH, NOTE_HEIGHT)
        remove_native_border(self)

        self.hide_timer = QTimer(self)
        self.hide_timer.setSingleShot(True)
        self.hide_timer.timeout.connect(self.hide_note)

        self.save_timer = QTimer(self)
        self.save_timer.setSingleShot(True)
        self.save_timer.timeout.connect(self.save_note)

        self.animation = QPropertyAnimation(self, b"geometry", self)
        self.animation.setDuration(SHOW_ANIMATION_MS)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.valueChanged.connect(self.on_geometry_value_changed)
        self.animation.finished.connect(self.on_animation_finished)

        self.build_ui()
        self.load_note()
        self.apply_theme()
        self.refresh_note_list()
        self.select_note(self.current_note_id, update_editor=True)
        self.reset_default_geometry()
        self.setGeometry(self.hidden_geometry)
        self.handle_geometry_changed.emit(self.hidden_geometry)

    def build_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        self.card = QFrame()
        self.card.setObjectName("card")

        outer.addWidget(self.card)

        layout = QVBoxLayout(self.card)
        layout.setContentsMargins(14, 12, 14, 14)
        layout.setSpacing(10)

        self.titlebar = QFrame()
        self.titlebar.setObjectName("titlebar")
        self.titlebar.setCursor(Qt.OpenHandCursor)
        self.titlebar.mousePressEvent = self.start_drag
        self.titlebar.mouseMoveEvent = self.drag_window
        self.titlebar.mouseReleaseEvent = self.end_drag

        title_layout = QHBoxLayout(self.titlebar)
        title_layout.setContentsMargins(2, 0, 2, 0)
        title_layout.setSpacing(6)

        self.pin_btn = IconButton("固定/自动收起")
        self.theme_btn = IconButton("切换黑白主题")
        self.save_btn = IconButton("保存")
        self.save_btn.setObjectName("saveButton")
        self.delete_btn = IconButton("删除当前便签")
        self.delete_btn.setObjectName("deleteButton")

        self.theme_btn.clicked.connect(lambda: self.toggle_theme())
        self.save_btn.clicked.connect(lambda: self.save_note())
        self.delete_btn.clicked.connect(lambda: self.delete_current_note())
        self.pin_btn.clicked.connect(lambda: self.toggle_pin())

        title_layout.addWidget(self.pin_btn)
        title_layout.addStretch()
        title_layout.addWidget(self.theme_btn)
        title_layout.addWidget(self.save_btn)
        title_layout.addWidget(self.delete_btn)

        content = QFrame()
        content.setObjectName("content")
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(10)

        self.note_list = QListWidget()
        self.note_list.setObjectName("noteList")
        self.note_list.setFixedWidth(138)
        self.note_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.note_list.setSpacing(4)
        self.note_list.currentItemChanged.connect(self.on_note_selected)

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(8, 8, 8, 8)
        sidebar_layout.setSpacing(8)
        sidebar_layout.addWidget(self.note_list, 1)

        self.new_note_btn = IconButton("新建便签")
        self.new_note_btn.setObjectName("sideButton")
        self.new_note_btn.clicked.connect(lambda: self.create_note())
        sidebar_layout.addWidget(self.new_note_btn)

        self.editor = QPlainTextEdit()
        self.editor.textChanged.connect(self.on_text_changed)

        content_layout.addWidget(sidebar)
        content_layout.addWidget(self.editor, 1)

        layout.addWidget(self.titlebar)
        layout.addWidget(content, 1)

        font = QFont("Segoe UI", 10)
        font.setStyleStrategy(QFont.PreferAntialias)
        self.setFont(font)

    def reset_default_geometry(self):
        screen = QApplication.primaryScreen().availableGeometry()
        x = screen.x() + (screen.width() - NOTE_WIDTH) // 2
        shown_y = screen.y()
        hidden_y = screen.y() - NOTE_HEIGHT
        self.shown_geometry = QRect(x, shown_y, NOTE_WIDTH, NOTE_HEIGHT)
        self.hidden_geometry = QRect(x, hidden_y, NOTE_WIDTH, NOTE_HEIGHT)

    def show_note(self):
        self.hide_timer.stop()
        if self.isVisible() and self.geometry().y() >= self.shown_geometry.y() - 2:
            return
        if not self.isVisible():
            self.setGeometry(self.hidden_geometry)
            self.show()
        self.raise_()
        self.animate_to(self.shown_geometry, SHOW_ANIMATION_MS)

    def hide_note(self, force: bool = False):
        if self.pinned and not force:
            return
        if not self.isVisible():
            return
        self.editor.clearFocus()
        self.animate_to(self.hidden_geometry, HIDE_ANIMATION_MS)

    def animate_to(self, geometry: QRect, duration_ms: int):
        self.animation.stop()
        self.animation.setDuration(duration_ms)
        self.animation.setStartValue(self.geometry())
        self.animation.setEndValue(geometry)
        self.animation.start()

    def on_geometry_value_changed(self, value):
        self.handle_geometry_changed.emit(value)

    def on_animation_finished(self):
        self.handle_geometry_changed.emit(self.geometry())
        if self.geometry().y() <= self.hidden_geometry.y() + 2:
            self.hide()
            self.hidden_finished.emit()

    def enterEvent(self, event):
        self.hide_timer.stop()
        super().enterEvent(event)

    def leaveEvent(self, event):
        super().leaveEvent(event)

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        if not self.pinned and not self.underMouse():
            self.hide_timer.start(AUTO_HIDE_DELAY_MS)

    def start_drag(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_offset = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            self.titlebar.setCursor(Qt.ClosedHandCursor)

    def drag_window(self, event):
        if self.drag_offset is None:
            return
        screen = QApplication.screenAt(event.globalPosition().toPoint()) or QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        raw_x = event.globalPosition().toPoint().x() - self.drag_offset.x()
        min_x = screen_geometry.x()
        max_x = screen_geometry.x() + screen_geometry.width() - NOTE_WIDTH
        docked_x = max(min_x, min(raw_x, max_x))
        shown_y = screen_geometry.y()
        hidden_y = screen_geometry.y() - NOTE_HEIGHT

        self.shown_geometry = QRect(docked_x, shown_y, NOTE_WIDTH, NOTE_HEIGHT)
        self.hidden_geometry = QRect(docked_x, hidden_y, NOTE_WIDTH, NOTE_HEIGHT)
        self.move(self.shown_geometry.topLeft())
        self.handle_geometry_changed.emit(self.geometry())

    def end_drag(self, event):
        self.drag_offset = None
        self.titlebar.setCursor(Qt.OpenHandCursor)

    def toggle_pin(self):
        self.pinned = not self.pinned
        self.hide_timer.stop()
        self.pin_btn.setToolTip("已固定" if self.pinned else "固定/自动收起")
        self.apply_theme()

    def clear_note(self):
        self.editor.clear()
        self.save_note()

    def load_note(self):
        self.notes = [{"id": DEFAULT_NOTE_ID, "text": "", "updated_at": time.time()}]
        if not self.note_file.exists():
            return
        try:
            data = json.loads(self.note_file.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return

        if isinstance(data.get("notes"), list):
            self.notes = data["notes"] or self.notes
        elif "text" in data:
            self.notes = [{"id": DEFAULT_NOTE_ID, "text": data.get("text", ""), "updated_at": time.time()}]

        self.current_note_id = data.get("current_note_id") or self.notes[0]["id"]
        self.theme_name = data.get("theme") if data.get("theme") in THEMES else "light"

    def save_note(self):
        self.update_current_note_text()
        data = {
            "current_note_id": self.current_note_id,
            "theme": self.theme_name,
            "notes": self.notes,
        }
        self.note_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        self.refresh_note_list()

    def on_text_changed(self):
        if self.loading_note:
            return
        self.update_current_note_text()
        self.save_timer.start(SAVE_DEBOUNCE_MS)

    def update_current_note_text(self):
        note = self.current_note()
        if note is None:
            return
        text = self.editor.toPlainText()
        if note.get("text") != text:
            note["text"] = text
            note["updated_at"] = time.time()

    def current_note(self):
        for note in self.notes:
            if note.get("id") == self.current_note_id:
                return note
        return None

    def note_title(self, note) -> str:
        text = note.get("text", "").strip()
        if not text:
            return "未命名"
        first_line = text.splitlines()[0].strip()
        return first_line[:12] + ("..." if len(first_line) > 12 else "")

    def refresh_note_list(self):
        selected_id = self.current_note_id
        self.note_list.blockSignals(True)
        self.note_list.clear()

        sorted_notes = sorted(self.notes, key=lambda item: item.get("updated_at", 0), reverse=True)
        for note in sorted_notes:
            item = QListWidgetItem(self.note_title(note))
            item.setData(Qt.UserRole, note.get("id"))
            item.setSizeHint(QSize(96, 30))
            self.note_list.addItem(item)
            if note.get("id") == selected_id:
                self.note_list.setCurrentItem(item)

        self.note_list.blockSignals(False)

    def on_note_selected(self, current, previous):
        if current is None:
            return
        self.update_current_note_text()
        self.current_note_id = current.data(Qt.UserRole)
        self.select_note(self.current_note_id, update_editor=True)
        self.save_timer.start(SAVE_DEBOUNCE_MS)

    def select_note(self, note_id: str, update_editor: bool):
        if not any(note.get("id") == note_id for note in self.notes):
            note_id = self.notes[0]["id"]
        self.current_note_id = note_id

        if update_editor:
            note = self.current_note()
            self.loading_note = True
            self.editor.setPlainText(note.get("text", "") if note else "")
            self.loading_note = False

    def create_note(self):
        self.update_current_note_text()
        note_id = str(int(time.time() * 1000))
        self.notes.insert(0, {"id": note_id, "text": "", "updated_at": time.time()})
        self.current_note_id = note_id
        self.refresh_note_list()
        self.select_note(note_id, update_editor=True)
        self.editor.setFocus()
        self.save_note()

    def delete_current_note(self):
        if not self.notes:
            return
        current_index = next(
            (index for index, note in enumerate(self.notes) if note.get("id") == self.current_note_id),
            0,
        )

        if len(self.notes) == 1:
            self.notes[0]["text"] = ""
            self.notes[0]["updated_at"] = time.time()
        else:
            del self.notes[current_index]

        next_index = min(current_index, len(self.notes) - 1)
        self.current_note_id = self.notes[next_index]["id"]
        self.refresh_note_list()
        self.select_note(self.current_note_id, update_editor=True)
        self.save_note()

    def toggle_theme(self):
        self.theme_name = "dark" if self.theme_name == "light" else "light"
        self.apply_theme()
        self.theme_changed.emit(self.theme_name)
        self.save_note()

    def apply_theme(self):
        theme = THEMES[self.theme_name]
        icon_color = QColor(theme["text"])
        self.pin_btn.setIcon(make_action_icon("pin", icon_color))
        self.save_btn.setIcon(make_action_icon("save", icon_color))
        self.delete_btn.setIcon(make_action_icon("trash", icon_color))
        self.new_note_btn.setIcon(make_action_icon("plus", icon_color))
        self.theme_btn.setIcon(
            make_action_icon("sun" if self.theme_name == "dark" else "moon", icon_color)
        )

        pin_background = theme["accent"] if self.pinned else theme["button"]
        pin_color = "#ffffff" if self.pinned else theme["text"]

        self.pin_btn.setStyleSheet(
            f"""
            QPushButton {{
                background: {pin_background};
                color: {pin_color};
                border: 0;
                border-radius: 8px;
                font-size: 11px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background: {theme["button_hover"] if not self.pinned else theme["accent"]};
            }}
            """
        )

        self.setStyleSheet(
            f"""
            QToolTip {{
                background: {theme["editor_focus"]};
                color: {theme["text"]};
                border: 1px solid {theme["border"]};
                border-radius: 6px;
                padding: 4px 7px;
            }}
            QFrame#card {{
                background: {theme["card"]};
                border: 0;
                border-radius: 16px;
            }}
            QFrame#titlebar {{
                background: transparent;
                min-height: 28px;
            }}
            QFrame#content {{
                background: transparent;
            }}
            QFrame#sidebar {{
                background: {theme["sidebar"]};
                border: 0;
                border-radius: 12px;
            }}
            QListWidget#noteList {{
                background: transparent;
                border: 0;
                color: {theme["text"]};
                outline: 0;
                font-size: 12px;
            }}
            QListWidget#noteList::item {{
                border-radius: 7px;
                padding: 5px 7px;
                min-height: 20px;
            }}
            QListWidget#noteList::item:hover {{
                background: {theme["hover_item"]};
            }}
            QListWidget#noteList::item:selected {{
                background: {theme["active_item"]};
                color: {theme["text"]};
            }}
            QPlainTextEdit {{
                background: {theme["editor"]};
                border: 1px solid {theme["border"]};
                border-radius: 12px;
                color: {theme["text"]};
                selection-background-color: {theme["accent"]};
                padding: 14px;
                font-size: 15px;
                line-height: 1.35;
            }}
            QPlainTextEdit:focus {{
                border: 1px solid {theme["border"]};
                background: {theme["editor_focus"]};
            }}
            QPushButton {{
                background: {theme["button"]};
                color: {theme["text"]};
                border: 0;
                border-radius: 8px;
                padding: 0;
            }}
            QPushButton:hover {{
                background: {theme["button_hover"]};
            }}
            QPushButton#saveButton {{
                min-width: 32px;
                min-height: 30px;
            }}
            QPushButton#deleteButton:hover {{
                background: rgba(255, 59, 48, 42);
            }}
            QPushButton#sideButton {{
                min-width: 32px;
                min-height: 30px;
            }}
            """
        )


class TopNoteApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setApplicationName(APP_NAME)
        self.app.setQuitOnLastWindowClosed(False)

        self.note = NoteWindow()
        self.hot_zone = HotZone()
        self.hot_zone.activated.connect(self.note.show_note)
        self.note.handle_geometry_changed.connect(self.hot_zone.follow_note)
        self.note.theme_changed.connect(self.hot_zone.set_theme)
        self.hot_zone.set_theme(self.note.theme_name)
        self.hover_timer = QTimer(self.app)
        self.hover_timer.timeout.connect(self.monitor_hover)
        self.hover_timer.start(45)

        self.tray = QSystemTrayIcon(make_tray_icon(), self.app)
        self.tray.setToolTip(APP_NAME)
        self.tray.activated.connect(self.on_tray_activated)
        self.tray.setContextMenu(self.build_tray_menu())
        self.tray.show()

        self.hot_zone.follow_note(self.note.geometry())
        self.hot_zone.show()

    def monitor_hover(self):
        if not self.note.isVisible() or self.note.pinned:
            return

        cursor_pos = QCursor.pos()
        over_note = self.note.geometry().contains(cursor_pos)
        over_handle = self.hot_zone.geometry().contains(cursor_pos)

        if over_note or over_handle:
            self.note.hide_timer.stop()
        elif not self.note.hide_timer.isActive():
            self.note.hide_timer.start(AUTO_HIDE_DELAY_MS)

    def build_tray_menu(self) -> QMenu:
        menu = QMenu()

        show_action = QAction("显示", menu)
        hide_action = QAction("隐藏", menu)
        quit_action = QAction("退出", menu)

        show_action.triggered.connect(lambda: self.note.show_note())
        hide_action.triggered.connect(lambda: self.note.hide_note(force=True))
        quit_action.triggered.connect(lambda: self.quit())

        menu.addAction(show_action)
        menu.addAction(hide_action)
        menu.addSeparator()
        menu.addAction(quit_action)
        return menu

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.note.show_note()

    def quit(self):
        self.note.save_note()
        self.tray.hide()
        self.app.quit()

    def run(self) -> int:
        return self.app.exec()


if __name__ == "__main__":
    sys.exit(TopNoteApp().run())
