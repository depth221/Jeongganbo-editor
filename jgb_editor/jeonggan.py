import json
import re
import os

from PyQt5.QtCore import QMargins
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip, QStatusBar, QMainWindow, \
    QApplication, QGridLayout, QLabel, QAction, qApp, QDesktopWidget, QDialog, QLineEdit, QFormLayout, QHBoxLayout, \
    QVBoxLayout, QFrame, QSizePolicy, QStackedLayout, QStackedWidget, QStyle, QGraphicsOpacityEffect, QLayout, QMenu
from PyQt5.QtGui import QFont, QIcon, QColor, QPalette, QFontMetrics, QPainter, QTextOption, QPixmap
from PyQt5 import QtCore

from jgb_editor.pitch_name import PitchName, PitchNamePlus1, PitchNamePlus2, PitchNameMinus1, PitchNameMinus2
from jgb_editor.pitch_etc_name import PitchEtcName

css_content = None

base_dir = os.path.dirname(os.path.abspath(__file__))
CSS_FILE_PATH = os.path.join(base_dir, 'style.css')
KEY_MAPPING_PATH = os.path.join(base_dir, 'key_mapping.json')
IMAGE_PATH = os.path.join(base_dir, 'image/')


class Page(QWidget):
    def __init__(self, gaks: int = 6, gangs: int = 4, jeonggans: int = 3,
                 title: bool = False, _id: int = None, parent: QMainWindow = None):
        super().__init__()

        self.parent = parent
        self.id = _id

        self.gaks = gaks
        self.gaks_obj = []  # list(QgridLayout)

        self.gangs = gangs
        self.jeonggans = jeonggans

        self.page_layout = QGridLayout()
        self.setLayout(self.page_layout)

        self.setContentsMargins(0, 0, 0, 0)

        self.page_layout.setSpacing(0)
        self.page_layout.setContentsMargins(0, 0, 0, 0)
        self.page_layout.setAlignment(QtCore.Qt.AlignJustify)

        self.jeonggan_grid = QGridLayout()
        self.jeonggan_grid.setSpacing(0)
        self.jeonggan_grid.setContentsMargins(0, 0, 0, 0)

        self.page_layout.addLayout(LeftPart(parent=self), 0, 0)
        self.page_layout.addWidget(BottomPart(), 1, 0, 1, 3)

        for i in range(gaks - 1, -1, -1):
            tmp_gak = Gak(num=gangs, jeonggans=jeonggans, _id=gaks - i - 1, parent=self)
            self.jeonggan_grid.addLayout(tmp_gak, 0, i)
            self.gaks_obj.append(tmp_gak)

        self.page_layout.addLayout(self.jeonggan_grid, 0, 1)

        if title is True:
            self.title_part = TitlePart(parent=self)
            self.page_layout.addLayout(self.title_part, 0, 2)
        else:
            self.page_layout.addWidget(NonTitlePart(parent=self), 0, 2)

    def find_next_gak(self, _id: int):
        if _id == self.gaks - 1:
            next_page = self.parent.find_next_page()
            if next_page.id == self.id:  # not next
                return self.gaks_obj[_id]
            else:  # next
                return next_page.gaks_obj[0]
        else:
            return self.gaks_obj[_id + 1]

    def find_prev_gak(self, _id: int):
        if _id == 0:
            prev_page = self.parent.find_prev_page()
            if prev_page.id == self.id:  # not prev
                return self.gaks_obj[_id]
            else:  # prev
                return prev_page.gaks_obj[prev_page.gaks - 1]
        else:
            return self.gaks_obj[_id - 1]


class TopPart(QLabel):
    def __init__(self, parent: Page = None):
        super().__init__(parent)
        self.set_style()

        self.setMargin(0)
        self.setFixedHeight(70 - 8)
        self.setFixedWidth(35 + 54)
        self.setContentsMargins(0, 0, 0, 0)

    def set_style(self) -> None:
        global css_content
        if css_content is None:
            with open(CSS_FILE_PATH, 'r') as f:
                css_content = f.read()

        self.setStyleSheet(css_content)


class LeftPart(QVBoxLayout):
    calc_width = None

    def __init__(self, parent: Page = None):
        super().__init__()
        self.parent = parent

        self.setContentsMargins(0, 0, 0, 0)

        width = 20

        tmp_label_0 = QLabel()
        tmp_label_0.setObjectName("LeftPart0")
        tmp_label_0.setFixedSize(width, 70 - 1)
        self.addWidget(tmp_label_0)

        tmp_label_1 = QLabel()
        tmp_label_1.setObjectName("LeftPart1")
        tmp_label_1.setFixedSize(width, 66 * self.parent.gangs * self.parent.jeonggans + 1)
        self.addWidget(tmp_label_1)

        tmp_label_2 = QLabel()
        tmp_label_2.setObjectName("LeftPart2")
        tmp_label_2.setFixedSize(width, 8)
        self.addWidget(tmp_label_2)

    def set_style(self) -> None:
        global css_content
        if css_content is None:
            with open(CSS_FILE_PATH, 'r') as f:
                css_content = f.read()

        self.setStyleSheet(css_content)


class BottomPart(QLabel):
    calc_width = None

    def __init__(self, parent: Page = None):
        super().__init__()
        self.parent = parent

        self.setMargin(0)
        self.setContentsMargins(0, 0, 0, 0)

        self.setFixedHeight(20)

    def set_style(self) -> None:
        global css_content
        if css_content is None:
            with open(CSS_FILE_PATH, 'r') as f:
                css_content = f.read()

        self.setStyleSheet(css_content)


class NonTitlePart(QLabel):
    calc_width = None

    def __init__(self, parent: Page = None):
        super().__init__()
        self.parent = parent

        self.setMargin(0)
        self.setContentsMargins(0, 0, 0, 0)

        if NonTitlePart.calc_width is None:
            global css_content
            # subtitle font size
            s_css_style = json_extract(css_content, "TitlePart", "left")
            s_p = re.compile("font-size: ([0-9]+)pt;")
            s_search_result = s_p.search(s_css_style)

            s_font_size = 14  # default
            if s_search_result is not None:
                s_font_size = int(s_search_result.groups()[0])

            s_font = QFont("NanumGothic", s_font_size, QFont.Normal)
            s_font_metrics = QFontMetrics(s_font)
            s_px_from_pt = s_font_metrics.fontDpi() / 72 * s_font_size
            print(s_px_from_pt)

            # title font size
            t_css_style = json_extract(css_content, "TitlePart", "right")  # title font size
            t_p = re.compile("font-size: ([0-9]+)pt;")
            t_search_result = t_p.search(t_css_style)

            t_font_size = 24  # default
            if t_search_result is not None:
                t_font_size = int(t_search_result.groups()[0])

            t_font = QFont("NanumGothic", t_font_size, QFont.Normal)
            t_font_metrics = QFontMetrics(t_font)
            t_px_from_pt = t_font_metrics.fontDpi() / 72 * t_font_size

            NonTitlePart.calc_width = 30 + int(s_px_from_pt + t_px_from_pt) + 60 - 35 - 54 - 1

        self.setFixedWidth(NonTitlePart.calc_width)

        self.set_style()

    def set_style(self) -> None:
        global css_content
        if css_content is None:
            with open(CSS_FILE_PATH, 'r') as f:
                css_content = f.read()

        self.setStyleSheet(css_content)


class TitlePartFrame(QFrame):
    def __init__(self, layout: "TitlePart", parent: Page = None):
        super().__init__()
        self.parent = parent
        self.layout = layout

        self.setFrameShape(QFrame.Box)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.setContentsMargins(1, 1, 1, 1)
        self.setFixedHeight(70 + 66 * self.parent.gangs * self.parent.jeonggans + 8)

    def mousePressEvent(self, event) -> None:
        position = event.pos()
        print(f"Clicked at position: {position.x()}, {position.y()}")
        print(f"x: {self.geometry().x()}, y: {self.geometry().y()}, "
              f"width: {self.geometry().width()}, height: {self.geometry().height()}")

        self.layout.dialog_open()


class TitlePart(QGridLayout):
    def __init__(self, parent: Page = None):
        super().__init__()
        self.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)
        self.parent = parent

        self.frame = TitlePartFrame(layout=self, parent=parent)
        self.addWidget(self.frame)

        self.gridlayout = QGridLayout()
        self.gridlayout.setSpacing(0)
        self.gridlayout.setContentsMargins(0, 0, 0, 0)
        self.frame.setLayout(self.gridlayout)

        self.dialog = QDialog()

        label_top = QLabel()
        self.set_style(label_top, "top_margin")
        self.gridlayout.addWidget(label_top, 0, 0, 1, 4)

        label_left = QLabel()
        self.set_style(label_left, "left_margin")
        self.gridlayout.addWidget(label_left, 1, 0)

        self.title_layout = QVBoxLayout()
        self.subtitle_layout = QVBoxLayout()
        self.title_layout.setContentsMargins(0, 0, 0, 0)
        self.subtitle_layout.setContentsMargins(0, 0, 0, 0)
        self.gridlayout.addLayout(self.subtitle_layout, 1, 1)
        self.gridlayout.addLayout(self.title_layout, 1, 2)

        label_right = QLabel()
        self.set_style(label_right, "right_margin")
        self.gridlayout.addWidget(label_right, 1, 3)

        label_bottom = QLabel()
        self.set_style(label_bottom, "bottom_margin")
        self.gridlayout.addWidget(label_bottom, 2, 0, 1, 4)

        self.set_style(self.frame)

        self.title = "제목"
        self.subtitle = "소제목 또는 작곡가"
        self.convert_vertical_rl(0, 0)

    def set_style(self, obj: QLabel, attr: str = None) -> None:
        global css_content
        if css_content is None:
            with open(CSS_FILE_PATH, 'r') as f:
                css_content = f.read()

        if attr is None:
            obj.setStyleSheet(css_content)
            return

        width_dict = {"left_margin": 30, "right_margin": 60}
        height_dict = {"top_margin": 100, "bottom_margin": 40}
        font_size = {"left": 14, "right": 24}

        if attr in ["left_margin", "right_margin"]:
            css_style = json_extract(css_content, "TitlePart", attr)
            obj.setStyleSheet(css_style)
            obj.setFixedWidth(width_dict[attr])
        elif attr in ["top_margin", "bottom_margin"]:
            css_style = json_extract(css_content, "TitlePart", attr)
            obj.setStyleSheet(css_style)
            obj.setFixedHeight(height_dict[attr])
        elif attr in ["left", "right"]:  # subtitle, title
            css_style = json_extract(css_content, "TitlePart", attr)
            obj.setStyleSheet(css_style)

    def dialog_open(self) -> None:
        title_cover_layout = QVBoxLayout()
        titles_layout = QFormLayout()

        title_widget = QLineEdit()
        subtitle_widget = QLineEdit()
        title_widget.setText(self.title)
        subtitle_widget.setText(self.subtitle)

        save_cancel_layout = QHBoxLayout()
        save_cancel_layout.setAlignment(QtCore.Qt.AlignHCenter)

        save_button = QPushButton("저장")
        save_button.clicked.connect(
            lambda: self.save_title_and_close(title_widget.text(), subtitle_widget.text())
        )
        cancel_button = QPushButton("취소")
        cancel_button.clicked.connect(
            lambda: self.save_title_and_close()
        )

        save_cancel_layout.addWidget(save_button, alignment=QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
        save_cancel_layout.addWidget(cancel_button, alignment=QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)

        titles_layout.addRow("제목: ", title_widget)
        titles_layout.addRow("소제목 또는 작곡가: ", subtitle_widget)

        title_cover_layout.addLayout(titles_layout)
        title_cover_layout.addLayout(save_cancel_layout)

        self.dialog.setLayout(title_cover_layout)
        self.dialog.setWindowTitle("제목 수정하기")
        self.dialog.setMinimumWidth(300)
        self.dialog.show()

    def save_title_and_close(self, title: str = None, subtitle: str = None) -> None:
        if title is not None:
            self.title = title
            self.subtitle = subtitle

            self.convert_vertical_rl()

        self.dialog.deleteLater()
        self.dialog = QDialog()

        self.parent.parent.is_saved = False

        self.dialog.close()

    def convert_vertical_rl(self, title_layout_size: int = None, subtitle_layout_size: int = None) -> None:
        if title_layout_size is None:
            title_layout_size = self.title_layout.count()
        if subtitle_layout_size is None:
            subtitle_layout_size = self.subtitle_layout.count()

        # remove the exising widgets
        for i in range(title_layout_size):
            self.title_layout.removeWidget(self.title_layout.itemAt(0).widget())

        for i in range(subtitle_layout_size):
            self.subtitle_layout.removeWidget(self.subtitle_layout.itemAt(0).widget())

        # add the new widgets
        for i in range(min(len(self.title), 18)):  # title
            tmp_label = QLabel()
            self.set_style(tmp_label, "right")
            tmp_label.setText(self.title[i])
            self.title_layout.insertWidget(i, tmp_label, alignment=QtCore.Qt.AlignVCenter | QtCore.Qt.AlignCenter)
        self.title_layout.addStretch(1)

        self.subtitle_layout.addStretch(1)
        for i in range(min(len(self.subtitle), 30)):  # subtitle
            tmp_label = QLabel()
            self.set_style(tmp_label, "left")
            tmp_label.setText(self.subtitle[i])
            self.subtitle_layout.insertWidget(i + 1, tmp_label, alignment=QtCore.Qt.AlignVCenter | QtCore.Qt.AlignCenter)

    def get_title(self) -> str:
        return self.title

    def get_subtitle(self) -> str:
        return self.subtitle


class Sumpyo(QLabel):
    SIZE = {"up": (8, 8), "down": (8, 8)}
    ICON_PATH = {"up": IMAGE_PATH + "/sumpyo2.png", "down": IMAGE_PATH + "/sumpyo2_down.png"}

    def __init__(self, _id: int, label_type: str,
                 is_first: bool = False, is_last: bool = False,
                 is_bottom_border: bool = False, is_first_row: bool = False, parent: "Gasaran" = None):
        super().__init__()
        self.parent = parent

        self.is_first = is_first
        self.is_last = is_last
        self.is_bottom_border = is_bottom_border
        self.is_first_row = is_first_row

        self.is_enabled = False

        self.id = _id
        self.label_type = label_type
        self.set_style()

        self.setMargin(0)
        self.setContentsMargins(0, 0, 0, 0)
        self.setObjectName(label_type)

    def set_style(self) -> None:
        global css_content
        if css_content is None:
            with open(CSS_FILE_PATH, 'r') as f:
                css_content = f.read()

        if self.label_type is None:
            self.setStyleSheet(css_content)
            return
        else:
            self.setStyleSheet(css_content)

        if self.label_type in ["up"]:
            if self.is_first and self.is_bottom_border:
                css_style = json_extract(css_content, "Sumpyo", self.label_type + "+first+bottom_border")
            elif self.is_bottom_border:
                css_style = json_extract(css_content, "Sumpyo", self.label_type + "+bottom_border")
            else:
                css_style = json_extract(css_content, "Sumpyo", self.label_type)
            self.setStyleSheet(css_style)
            self.setPixmap(QPixmap(Sumpyo.ICON_PATH[self.label_type]))
            self.setFixedSize(*Sumpyo.SIZE[self.label_type])
        elif self.label_type in ["down"]:
            if self.is_last:
                css_style = json_extract(css_content, "Sumpyo", self.label_type + "+last")
            else:
                css_style = json_extract(css_content, "Sumpyo", self.label_type)
            self.setStyleSheet(css_style)
            self.setPixmap(QPixmap(Sumpyo.ICON_PATH[self.label_type]))
            self.setFixedSize(*Sumpyo.SIZE[self.label_type])

        if not self.is_enabled:
            self.clear()

    def get_id(self) -> int:
        return self.id

    def mousePressEvent(self, event) -> None:
        position = event.pos()
        print(f"Clicked at position: {position.x()}, {position.y()}")
        print(f"x: {self.geometry().x()}, y: {self.geometry().y()}, "
              f"width: {self.geometry().width()}, height: {self.geometry().height()}")

        self.click()

    def click(self, is_me: bool = True):
        if self.is_enabled:
            self.clear()
            self.is_enabled = False
        else:
            self.setPixmap(QPixmap(Sumpyo.ICON_PATH[self.label_type]))
            self.is_enabled = True

        if is_me:
            if self.label_type == "up":
                my_pos = self.parent.get_sumpyo_pos(self.id)

                if my_pos == self.parent.get_max_sumpyo() - 1:
                    next_gang = self.parent.parent.parent.find_next_gang(self.parent.parent.get_id())
                    next_gasaran = next_gang.get_gasaran()
                    next_gasaran.get_sumpyos(0).click(is_me=False)
                else:
                    self.parent.get_sumpyos(my_pos + 1).click(is_me=False)
            elif self.label_type == "down":
                my_pos = self.parent.get_sumpyo_pos(self.id)

                if my_pos == 0:
                    prev_gang = self.parent.parent.parent.find_prev_gang(self.parent.parent.get_id())
                    prev_gasaran = prev_gang.get_gasaran()
                    prev_gasaran_max = prev_gasaran.get_max_sumpyo()
                    prev_gasaran.get_sumpyos(prev_gasaran_max - 1).click(is_me=False)
                else:
                    self.parent.get_sumpyos(my_pos - 1).click(is_me=False)


class Sigimsae(QLabel):
    ICON_PATH = {"araero_ddeoneun_pyo": IMAGE_PATH + "/sigimsae/araero_ddeoneun_pyo.png",
                 "araero_ddeoneun_pyo_bottom": IMAGE_PATH + "/sigimsae/araero_ddeoneun_pyo_bottom.png",

                 "gyop_heullim_pyo": IMAGE_PATH + "/sigimsae/gyop_heullim_pyo.png",
                 "gyop_heullim_pyo_bottom": IMAGE_PATH + "/sigimsae/gyop_heullim_pyo.png",

                 "gyop_mineun_pyo": IMAGE_PATH + "/sigimsae/gyop_mineun_pyo.png",
                 "gyop_mineun_pyo_bottom": IMAGE_PATH + "/sigimsae/gyop_mineun_pyo.png",

                 "heullim_pyo1": IMAGE_PATH + "/sigimsae/heullim_pyo1.png",
                 "heullim_pyo1_bottom": IMAGE_PATH + "/sigimsae/heullim_pyo1.png",
                 "heullim_pyo2": IMAGE_PATH + "/sigimsae/heullim_pyo2.png",
                 "heullim_pyo2_bottom": IMAGE_PATH + "/sigimsae/heullim_pyo2_bottom.png",
                 "heullim_pyo3": IMAGE_PATH + "/sigimsae/heullim_pyo3.png",
                 "heullim_pyo3_bottom": IMAGE_PATH + "/sigimsae/heullim_pyo3_bottom.png",

                 "mineun_pyo1": IMAGE_PATH + "/sigimsae/mineun_pyo1.png",
                 "mineun_pyo1_bottom": IMAGE_PATH + "/sigimsae/mineun_pyo1.png",
                 "mineun_pyo2": IMAGE_PATH + "/sigimsae/mineun_pyo2.png",
                 "mineun_pyo2_bottom": IMAGE_PATH + "/sigimsae/mineun_pyo2_bottom.png",
                 "mineun_pyo3": IMAGE_PATH + "/sigimsae/mineun_pyo3.png",
                 "mineun_pyo3_bottom": IMAGE_PATH + "/sigimsae/mineun_pyo3_bottom.png",

                 "nongeum1": IMAGE_PATH + "/sigimsae/nongeum1.png", "nongeum1_bottom": IMAGE_PATH + "/sigimsae/nongeum1_bottom.png",
                 "nongeum2": IMAGE_PATH + "/sigimsae/nongeum2.png", "nongeum2_bottom": IMAGE_PATH + "/sigimsae/nongeum2_bottom.png",
                 "nongeum3": IMAGE_PATH + "/sigimsae/nongeum3.png", "nongeum3_bottom": IMAGE_PATH + "/sigimsae/nongeum3_bottom.png",
                 "nongeum4": IMAGE_PATH + "/sigimsae/nongeum4.png", "nongeum4_bottom": IMAGE_PATH + "/sigimsae/nongeum4_bottom.png",
                 "nongeum5": IMAGE_PATH + "/sigimsae/nongeum5.png", "nongeum5_bottom": IMAGE_PATH + "/sigimsae/nongeum5_bottom.png",
                 "nongeum6": IMAGE_PATH + "/sigimsae/nongeum6.png", "nongeum6_bottom": IMAGE_PATH + "/sigimsae/nongeum6_bottom.png",
                 "nongeum7": IMAGE_PATH + "/sigimsae/nongeum7.png", "nongeum7_bottom": IMAGE_PATH + "/sigimsae/nongeum7_bottom.png",
                 "nongeum8": IMAGE_PATH + "/sigimsae/nongeum8.png", "nongeum8_bottom": IMAGE_PATH + "/sigimsae/nongeum8_bottom.png",

                 "pureo_naerinuen_pyo": IMAGE_PATH + "/sigimsae/pureo_naerinuen_pyo.png",
                 "pureo_naerinuen_pyo_bottom": IMAGE_PATH + "/sigimsae/pureo_naerinuen_pyo_bottom.png",

                 "wiro_ddeoneun_pyo": IMAGE_PATH + "/sigimsae/wiro_ddeoneun_pyo.png",
                 "wiro_ddeoneun_pyo_bottom": IMAGE_PATH + "/sigimsae/wiro_ddeoneun_pyo_bottom.png"}

    ICON_PLACEMENT = [["araero_ddeoneun_pyo", "gyop_heullim_pyo", "gyop_mineun_pyo"],

                      ["heullim_pyo1", "heullim_pyo2", "heullim_pyo3"],

                      ["mineun_pyo1", "mineun_pyo2", "mineun_pyo3"],

                      ["nongeum1", "nongeum2", "nongeum3"],
                      ["nongeum4", "nongeum5", "nongeum6"],
                      ["nongeum7", "nongeum8", "wiro_ddeoneun_pyo"],

                      ["pureo_naerinuen_pyo",  "nongeum3", "nongeum3"]]

    current_pos = None
    opened_dialog: list[QDialog] = []

    def __init__(self, _id: int, is_bottom_border: bool = False, is_first_row: bool = False,
                 parent: "Gasaran" = None):
        super().__init__()
        self.parent = parent

        self.is_bottom_border = is_bottom_border
        self.is_first_row = is_first_row
        self.id = _id
        self.label_type = None

        self.set_style(self)

        self.dialog = None

        self.setMargin(0)
        self.setContentsMargins(0, 0, 0, 0)

        self.set_sigimsae(self)

    def set_style(self, obj: QLabel) -> None:
        global css_content
        if css_content is None:
            with open(CSS_FILE_PATH, 'r') as f:
                css_content = f.read()

        obj.setStyleSheet(css_content)

        if self.is_bottom_border:
            css_style = json_extract(css_content, "Sigimsae", "bottom_border")
            obj.setStyleSheet(css_style)
        # obj.setPixmap(QPixmap(icon_path[attr]))
        obj.setFixedSize(35 - 8, 66 // 3)

        # if attr in ["up"]:

    def get_id(self) -> int:
        return self.id

    @staticmethod
    def set_sigimsae(obj: "Sigimsae") -> None:
        obj.clear()
        if obj.label_type is not None:
            if obj.is_bottom_border:
                obj.setPixmap(QPixmap(Sigimsae.ICON_PATH[obj.label_type + "_bottom"]))
            else:
                obj.setPixmap(QPixmap(Sigimsae.ICON_PATH[obj.label_type]))
        else:
            obj.clear()

    def mousePressEvent(self, event) -> None:
        position = event.pos()
        print(f"Clicked at position: {position.x()}, {position.y()}")
        print(f"x: {self.geometry().x()}, y: {self.geometry().y()}, "
              f"width: {self.geometry().width()}, height: {self.geometry().height()}")

        for dialog in Sigimsae.opened_dialog:
            dialog.close()
            dialog.deleteLater()
        Sigimsae.opened_dialog.clear()

        self.parent.parent.parent.parent.parent.is_saved = False

        self.dialog_open()

    def dialog_open(self) -> None:
        self.dialog = QDialog()
        Sigimsae.opened_dialog.append(self.dialog)

        dialog_layout = QVBoxLayout()
        sigimsae_grid = QGridLayout()
        sigimsae_grid.setContentsMargins(0, 0, 0, 0)
        dialog_layout.addLayout(sigimsae_grid)

        sigimsae_buttons: list[QPushButton] = []

        Sigimsae.current_pos = self

        col = 0
        for col_item in Sigimsae.ICON_PLACEMENT:
            row = 0
            for item in col_item:
                sigimsae_button = QPushButton()
                sigimsae_button.setIcon(QIcon(Sigimsae.ICON_PATH[item]))
                sigimsae_button.setToolTip(item)
                sigimsae_button.setFixedSize(27, 22)
                sigimsae_button.setContentsMargins(0, 0, 0, 0)
                sigimsae_buttons.append(sigimsae_button)
                sigimsae_grid.addWidget(sigimsae_button, row, col)

                row += 1

            col += 1

        for button_item in sigimsae_buttons:
            tmp_str = button_item.toolTip()
            button_item.clicked.connect(
                lambda _, s=tmp_str: self.apply_sigimsae(obj=Sigimsae.current_pos, label_type=s)
            )

        apply_cancel_layout = QHBoxLayout()
        apply_cancel_layout.setAlignment(QtCore.Qt.AlignHCenter)
        dialog_layout.addLayout(apply_cancel_layout)

        apply_button = QPushButton("확인")
        apply_button.clicked.connect(self.dialog.close)
        cancel_button = QPushButton("삭제")
        cancel_button.clicked.connect(
            lambda _: self.delete_sigimsae(obj=Sigimsae.current_pos)
        )

        apply_cancel_layout.addWidget(apply_button, alignment=QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
        apply_cancel_layout.addWidget(cancel_button, alignment=QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)

        self.dialog.setLayout(dialog_layout)
        self.dialog.setWindowTitle("시김새 넣기")
        self.dialog.setMinimumWidth(300)
        self.dialog.show()

    @staticmethod
    def apply_sigimsae(obj: "Sigimsae", label_type: str = None) -> None:
        if label_type is not None:
            obj.label_type = label_type
        obj.set_sigimsae(obj)

        my_pos = obj.parent.get_sigimsae_pos(obj.id)

        if my_pos == obj.parent.get_max_sigimsae() - 1:
            next_gang = obj.parent.parent.parent.find_next_gang(obj.parent.parent.get_id())
            next_gasaran = next_gang.get_gasaran()
            Sigimsae.current_pos = next_gasaran.get_sigimsaes(0)
        else:
            Sigimsae.current_pos = obj.parent.get_sigimsaes(my_pos + 1)

    @staticmethod
    def delete_sigimsae(obj: "Sigimsae") -> None:
        obj.label_type = None
        obj.set_sigimsae(obj)

        my_pos = obj.parent.get_sigimsae_pos(obj.id)

        if my_pos == obj.parent.get_max_sigimsae() - 1:
            next_gang = obj.parent.parent.parent.find_next_gang(obj.parent.parent.get_id())
            next_gasaran = next_gang.get_gasaran()
            Sigimsae.current_pos = next_gasaran.get_sigimsaes(0)
        else:
            Sigimsae.current_pos = obj.parent.get_sigimsaes(my_pos + 1)


class Gasaran(QHBoxLayout):
    def __init__(self, num: int = 1, parent: "Gang" = None):
        super().__init__()

        self.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)

        self.parent = parent
        self.num = num
        self.sigimsaes: list[Sigimsae] = list()
        self.sumpyos: list[Sumpyo] = list()

        self.sumpyos_layout = QVBoxLayout()
        self.sumpyos_layout.setContentsMargins(0, 0, 0, 0)
        self.sumpyos_layout.setSpacing(0)

        self.sigimsae_layout = QVBoxLayout()
        self.sigimsae_layout.setContentsMargins(0, 0, 0, 0)
        self.sigimsae_layout.setSpacing(0)

        self.addLayout(self.sumpyos_layout)
        self.addLayout(self.sigimsae_layout)

        #    8(시작부)              22
        #    1
        #    16(1/3 부분)
        # 66 16(1/2 부분)           22
        #    16(2/3 부분)
        #    1
        #    8(종료부)              22
        # ---------------------------------------------
        #        8              19      +       8
        #                    35

        self._id_sumpyo_count = 0
        self._id_sigimsae_count = 0

        for i in range(num):
            self.sumpyos.append(Sumpyo(label_type="down", _id=self._id_sumpyo_count, parent=self))
            self.sumpyos_layout.addWidget(self.sumpyos[-1], 0 + 10 * i)
            self._id_sumpyo_count += 1

            self.sumpyos_layout.addWidget(self.setting_form("sumpyo_yeobaek"), 1 + 10 * i)

            for j in range(3):
                self.sumpyos.append(Sumpyo(label_type="up", _id=self._id_sumpyo_count, parent=self))
                self.sumpyos_layout.addWidget(self.sumpyos[-1], 2 + 2 * j + 10 * i)
                self._id_sumpyo_count += 1
                self.sumpyos.append(Sumpyo(label_type="down", _id=self._id_sumpyo_count, parent=self))
                self.sumpyos_layout.addWidget(self.sumpyos[-1], 3 + 2 * j + 10 * i)
                self._id_sumpyo_count += 1

            self.sumpyos_layout.addWidget(self.setting_form("sumpyo_yeobaek"), 8 + 10 * i)
            self.sumpyos.append(Sumpyo(label_type="up", _id=self._id_sumpyo_count,
                                       is_bottom_border=(i == num - 1), parent=self))
            self.sumpyos_layout.addWidget(self.sumpyos[-1], 9 + 10 * i)
            self._id_sumpyo_count += 1

            for k in range(2):
                self.sigimsaes.append(Sigimsae(_id=self._id_sigimsae_count, parent=self))
                self.sigimsae_layout.addWidget(self.sigimsaes[-1], 3 * i + k)
                self._id_sigimsae_count += 1

            self.sigimsaes.append(Sigimsae(_id=self._id_sigimsae_count, is_bottom_border=(i == num - 1), parent=self))
            self.sigimsae_layout.addWidget(self.sigimsaes[-1], 3 * i + 2)
            self._id_sigimsae_count += 1

    def setting_form(self, label_type: str) -> QLabel:
        size = {"sumpyo_yeobaek": (8, 1), "sigimsae": (35 - 8, 66 // 3)}
        icon_path = {"sumpyo_yeobaek": None, "sigimsae": None}

        tmp_label = QLabel()
        tmp_label.setMargin(0)
        tmp_label.setContentsMargins(0, 0, 0, 0)
        tmp_label.setObjectName(label_type)
        tmp_label.setFixedSize(*size[label_type])

        if icon_path[label_type] is not None:
            tmp_label.setPixmap(QPixmap(icon_path[label_type]))

        if label_type in ["sigimsaes"]:
            self.sigimsaes.append(tmp_label)

        return tmp_label

    def set_style(self) -> None:
        global css_content
        if css_content is None:
            with open(CSS_FILE_PATH, 'r') as f:
                css_content = f.read()

        self.setStyleSheet(css_content)

    def get_sumpyos(self, pos: int) -> Sumpyo:
        return self.sumpyos[pos]

    def get_sumpyo_pos(self, _id: int) -> int:
        for i in range(len(self.sumpyos)):
            if self.sumpyos[i].get_id() == _id:
                return i
        else:
            raise IndexError(f"{self.get_sumpyo_pos.__name__}: "
                             f"요청한 id 값이 해당 객체에 존재하지 않습니다({_id}).")

    def get_max_sumpyo(self) -> int:
        return len(self.sumpyos)

    def insert_sumpyos_pos(self, pos: int, label_type: str,
                 is_first: bool = False, is_last: bool = False,
                 is_bottom_border: bool = False, is_first_row: bool = False, parent: "Gasaran" = None) -> None:
        self.sumpyos.insert(pos, Sumpyo(label_type=label_type, _id=self._id_sumpyo_count,
                                   is_first=is_first, is_last=is_last,
                                   is_bottom_border=is_bottom_border, is_first_row=is_first_row, parent=parent))
        self._id_sumpyo_count += 1

    def append_sumpyos(self, label_type: str,
                 is_first: bool = False, is_last: bool = False,
                 is_bottom_border: bool = False, is_first_row: bool = False, parent: "Gasaran" = None) -> None:
        self.sumpyos.append(Sumpyo(label_type=label_type, _id=self._id_sumpyo_count,
                                   is_first=is_first, is_last=is_last,
                                   is_bottom_border=is_bottom_border, is_first_row=is_first_row, parent=parent))
        self._id_sumpyo_count += 1

    def get_sigimsae_pos(self, _id: int) -> int:
        for i in range(len(self.sigimsaes)):
            if self.sigimsaes[i].get_id() == _id:
                return i
        else:
            raise IndexError(f"{self.get_sigimsae_pos.__name__}: "
                             f"요청한 id 값이 해당 객체에 존재하지 않습니다({_id}).")

    def get_max_sigimsae(self) -> int:
        return len(self.sigimsaes)

    def get_sigimsaes(self, pos: int) -> Sigimsae:
        return self.sigimsaes[pos]

    def get_sumpyo_list(self) -> list[Sumpyo]:
        return self.sumpyos

    def get_sigimsae_list(self) -> list[Sigimsae]:
        return self.sigimsaes


class Gak(QGridLayout):  # Gang * n
    def __init__(self, num: int = 4, jeonggans: int = 3, _id=None, parent: Page = None):
        super().__init__()
        self.parent = parent
        self.id = _id

        self.gangs = num
        self.gangs_obj = []  # list(QgridLayout)

        self.setContentsMargins(0, 0, 0, 0)

        for i in range(num):
            tmp_label = None
            if i == 0:
                tmp_label = Gang(num=jeonggans, _id=i, is_first=True, is_last=False, parent=self)
            elif i == num - 1:
                tmp_label = Gang(num=jeonggans, _id=i, is_first=False, is_last=True, parent=self)
            else:
                tmp_label = Gang(num=jeonggans, _id=i, is_first=False, is_last=False, parent=self)
            self.gangs_obj.append(tmp_label)
            self.addLayout(tmp_label, i, 0)

    def get_max_gang(self):
        return self.gangs - 1

    def find_next_gang(self, _id: int):
        if _id == self.gangs - 1:
            next_gak = self.parent.find_next_gak(self.id)
            if next_gak.id == self.id:  # not next
                return self.gangs_obj[_id]
            else:  # next
                return next_gak.gangs_obj[0]
        else:
            return self.gangs_obj[_id + 1]

    def find_prev_gang(self, _id: int):
        if _id == 0:
            prev_gak = self.parent.find_prev_gak(self.id)
            if prev_gak.id == self.id:  # not prev
                return self.gangs_obj[_id]
            else:  # prev
                return prev_gak.gangs_obj[prev_gak.gangs - 1]
        else:
            return self.gangs_obj[_id - 1]


class Gang(QGridLayout):  # Gasaran + Jeonggan * n
    def __init__(self, num=3, _id=None, is_first: bool = False, is_last: bool = False, parent: Gak = None):
        super().__init__()
        self.parent = parent
        self.id = _id

        self.jeonggans = num
        self.jeonggans_obj = []  # list(QgridLayout)

        self.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)

        self.gasaran = Gasaran(num=num, parent=self)

        self.is_first = is_first
        self.is_last = is_last

        jeonggan_start_point = 0

        if self.is_first:
            self.addWidget(TopPart(), 0, 0, 1, 2)

            self.addWidget(self.setting_form("first_top_left"), 1, 0)

            sumpyo_and_right_down = QHBoxLayout()
            sumpyo_and_right_down.setContentsMargins(0, 0, 0, 0)
            sumpyo_and_right_down.setSpacing(0)

            self.gasaran.insert_sumpyos_pos(0, label_type="up",
                                            is_first=True, is_bottom_border=True, parent=self.gasaran)
            sumpyo_and_right_down.addWidget(self.gasaran.get_sumpyos(0))

            sumpyo_and_right_down.addWidget(self.setting_form("first_top_right"))

            self.addLayout(sumpyo_and_right_down, 1, 1)

            jeonggan_start_point = 2

        for i in range(self.jeonggans):
            tmp_label = Jeonggan(row=1, _id=i, parent=self)
            self.jeonggans_obj.append(tmp_label)
            self.addLayout(self.jeonggans_obj[i], i + jeonggan_start_point, 0)

        self.addLayout(self.gasaran, jeonggan_start_point, 1, self.jeonggans, 1)

        if self.is_last:
            self.addWidget(self.setting_form("last_bottom_left"), self.jeonggans + jeonggan_start_point, 0)

            sumpyo_and_right_down_last = QHBoxLayout()
            sumpyo_and_right_down_last.setContentsMargins(0, 0, 0, 0)
            sumpyo_and_right_down_last.setSpacing(0)

            self.gasaran.append_sumpyos(label_type="down", is_last=True, parent=self.gasaran)
            sumpyo_and_right_down_last.addWidget(self.gasaran.get_sumpyos(-1))

            if self.id == 0:  # the first row
                sumpyo_and_right_down_last.addWidget(self.setting_form("last_bottom_right_id0"))
            else:
                sumpyo_and_right_down_last.addWidget(self.setting_form("last_bottom_right"))
            self.addLayout(sumpyo_and_right_down_last, self.jeonggans + jeonggan_start_point, 1)

    def setting_form(self, label_type: str) -> QLabel:
        size = {"sumpyo_up": (8, 8), "sumpyo_down": (8, 8),
                "sumpyo_up_for_first": (8, 8), "sumpyo_down_for_last": (8, 8),
                "first_top_left": (54, 8), "first_top_right": (35 - 8, 8),
                "last_bottom_left": (54, 8), "last_bottom_right": (35 - 8, 8),
                "last_bottom_right_id0": (35 - 8, 8)}
        icon_path = {"sumpyo_up": IMAGE_PATH + "/sumpyo2.png", "sumpyo_down": IMAGE_PATH + "/sumpyo2_down.png",
                     "sumpyo_up_for_first": IMAGE_PATH + "/sumpyo2.png", "sumpyo_down_for_last": IMAGE_PATH + "/sumpyo2_down.png",
                     "first_top_left": None, "first_top_right": None,
                     "last_bottom_left": None, "last_bottom_right": None,
                     "last_bottom_right_id0": None}

        tmp_label = QLabel()
        tmp_label.setMargin(0)
        tmp_label.setContentsMargins(0, 0, 0, 0)
        tmp_label.setObjectName(label_type)
        tmp_label.setFixedSize(*size[label_type])

        if icon_path[label_type] is not None:
            tmp_label.setPixmap(QPixmap(icon_path[label_type]))

        if label_type in ["sumpyo_up", "sumpyo_down", "sumpyo_up_for_first", "sumpyo_down_for_last"]:
            self.gasaran.sumpyos.append(tmp_label)

        return tmp_label

    def get_id(self) -> int:
        return self.id

    def get_gasaran(self) -> Gasaran:
        return self.gasaran

    def get_max_jeonggan(self):
        return self.jeonggans - 1

    def find_jeonggan_by_pos(self, _row: int):
        if _row >= self.jeonggans:
            return self.jeonggans_obj[self.jeonggans - 1]  # the last Jeonggan

        return self.jeonggans_obj[_row]

    def find_next_jeonggan(self, _id: int):
        if _id == self.jeonggans - 1:
            next_gang = self.parent.find_next_gang(self.id)
            if next_gang.id == self.id:  # not next
                return self.jeonggans_obj[_id]
            else:  # next
                return next_gang.find_jeonggan_by_pos(0)
        else:
            return self.jeonggans_obj[_id + 1]

    def find_prev_jeonggan(self, _id: int):
        if _id == 0:
            prev_gang = self.parent.find_prev_gang(self.id)
            if prev_gang.id == self.id:  # not prev
                return self.jeonggans_obj[_id]
            else:  # prev
                return prev_gang.find_jeonggan_by_pos(prev_gang.get_max_jeonggan())
        else:
            return self.jeonggans_obj[_id - 1]


class Jeonggan(QGridLayout):
    def __init__(self, row=1, _id: int = None, parent: Gang = None):
        super().__init__()
        self.parent = parent
        self.id = _id
        self.rows = row
        self.rows_obj = []  # list(QgridLayout)
        self.kans = []  # list(size: int)
        self.kans_obj = []  # list(list(Kan))

        for i in range(row):
            self.rows_obj.append(QGridLayout())
            self.kans.append(0)
            self.kans_obj.append([])
            self.addLayout(self.rows_obj[i], i, 0)

        for i in range(row):
            self.append(i)

        self.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)

    def get_rows(self) -> int:
        return self.rows

    def append(self, row: int) -> "Kan":
        return self.insert(row, self.kans[row])

    def insert(self, row: int, col: int) -> "Kan":
        if row < 0:
            raise IndexError(f"{self.insert.__name__}: "
                             f"row 값이 0보다 작습니다({row}).")

        if row >= self.rows:
            raise IndexError(f"{self.insert.__name__}: "
                             f"row 값이 Jeonggan.row = {self.rows}보다 작지 않습니다({row}).")

        if self.kans[row] > 3:
            raise IndexError(f"{self.insert.__name__}: "
                             f"row 행의 박자 수가 3보다 큽니다({self.kans[row]}).")

        if col < 0:
            raise IndexError(f"{self.insert.__name__}: "
                             f"col이 0보다 작습니다({col}).")

        if col > self.kans[row]:
            raise IndexError(f"{self.insert.__name__}: "
                             f"row 행의 박자 수가 col = {col}보다 큽니다({self.kans[row]}).")

        tmp_kam = None
        if row == 0 and self.rows == 1:
            tmp_kan = Kan(self.rows, self.kans[row] + 1, is_first=True, is_last=True, parent=self)
            self.kans_obj[row].insert(col, tmp_kan)
        elif row == 0:
            tmp_kan = Kan(self.rows, self.kans[row] + 1, is_first=True, is_last=False, parent=self)
            self.kans_obj[row].insert(col, tmp_kan)
        elif row == self.rows - 1:
            tmp_kan = Kan(self.rows, self.kans[row] + 1, is_first=False, is_last=True, parent=self)
            self.kans_obj[row].insert(col, tmp_kan)
        else:
            tmp_kan = Kan(self.rows, self.kans[row] + 1, is_first=False, is_last=False, parent=self)
            self.kans_obj[row].insert(col, tmp_kan)

        for i in self.kans_obj[row]:
            self.rows_obj[row].removeWidget(i)

        for tmp_kan_for in self.kans_obj[row]:
            tmp_kan_for.set_cols(self.kans[row] + 1)

        self.kans[row] += 1

        for i in range(self.kans[row]):
            self.rows_obj[row].addWidget(self.kans_obj[row][i], 0, i)

        return self.kans_obj[row][col]

    def append_row(self) -> "kan":
        return self.insert_row(self.rows)

    def insert_row(self, row_pos: int) -> "Kan":
        for i in range(self.rows):
            self.removeItem(self.rows_obj[i])

        self.rows_obj.insert(row_pos, QGridLayout())
        self.kans.insert(row_pos, 0)
        self.kans_obj.insert(row_pos, [])
        self.rows += 1

        self.append(row_pos)

        for each_row in range(self.rows):  # re-render
            for i in self.kans_obj[each_row]:
                i.set_rows(self.rows)

        if row_pos == self.rows - 1:  # is no longer the last
            for i in self.kans_obj[self.rows - 2]:
                i.set_is_last(False)

        for i in range(self.rows):
            self.addLayout(self.rows_obj[i], i, 0)

        return self.kans_obj[row_pos][0]

    def erase(self, _id: int):
        row, col = self.find_kan(_id)

        if row < 0:
            raise IndexError(f"{self.erase.__name__}: "
                             f"row 값이 0보다 작습니다({row}).")

        if row >= self.rows:
            raise IndexError(f"{self.erase.__name__}: "
                             f"row 값이 Jeonggan.row = {self.rows}보다 작지 않습니다({row}).")

        if self.kans[row] <= 0:
            raise IndexError(f"{self.erase.__name__}: "
                             f"row 행의 박자 수가 1보다 작습니다({self.kans[row]}).")

        if self.kans[row] <= col or col < 0:
            raise Exception(f"{self.erase.__name__}: "
                            f"삭제하려는 id가 잘못되었습니다({col}).")

        for i in self.kans_obj[row]:
            self.rows_obj[row].removeWidget(i)

        self.kans_obj[row][col].deleteLater()
        del self.kans_obj[row][col]
        self.kans[row] -= 1

        for tmp_kan in self.kans_obj[row]:
            tmp_kan.set_cols(self.kans[row])

        for i in range(self.kans[row]):
            self.rows_obj[row].addWidget(self.kans_obj[row][i], 0, i)

    def erase_row(self, row_pos: int = None):
        if row_pos is None:  # erase the last row
            row_pos = self.rows - 1

        if row_pos < 0:
            raise IndexError(f"{self.erase_row.__name__}: "
                             f"row 값이 0보다 작습니다({row_pos}).")

        if row_pos >= self.rows:
            raise IndexError(f"{self.erase_row.__name__}: "
                             f"row 값이 Jeonggan.row = {self.rows}보다 작지 않습니다({row_pos}).")

        for i in self.kans_obj[row_pos]:
            self.rows_obj[row_pos].removeWidget(i)
            i.deleteLater()

        for i in range(self.rows):
            self.removeItem(self.rows_obj[i])

        del self.rows_obj[row_pos]
        del self.kans[row_pos]
        del self.kans_obj[row_pos]
        self.rows -= 1

        for each_row in range(self.rows):  # re-render
            for i in self.kans_obj[each_row]:
                i.set_rows(self.rows)

        if row_pos == self.rows:  # is now the last
            for i in self.kans_obj[self.rows - 1]:
                i.set_is_last(True)

        for i in range(self.rows):
            self.addLayout(self.rows_obj[i], i, 0)

    def extend_1_to_2(self) -> "Kan":
        if self.rows != 1:
            raise IndexError(f"{self.extend_1_to_2.__name__}: "
                             f"row 값이 1이 아닙니다({self.rows}).")

        if self.kans[0] != 1:
            raise IndexError(f"{self.extend_1_to_2.__name__}: "
                             f"1번째 줄의 칸이 1개가 아닙니다({self.kans[0]}).")

        self.append_row()

        return self.kans_obj[1][0]

    def extend_2_to_3(self) -> "Kan":
        if self.rows != 2:
            raise IndexError(f"{self.extend_2_to_3.__name__}: "
                             f"row 값이 2가 아닙니다({self.rows}).")

        if self.kans[0] != 1:
            raise IndexError(f"{self.extend_2_to_3.__name__}: "
                             f"1번째 줄의 칸이 1개가 아닙니다({self.kans[0]}).")

        if self.kans[1] != 1:
            raise IndexError(f"{self.extend_2_to_3.__name__}: "
                             f"2번째 줄의 칸이 1개가 아닙니다({self.kans[1]}).")

        self.append_row()

        return self.kans_obj[2][0]

    def extend_3_to_4(self) -> "Kan":
        if self.rows != 3:
            raise IndexError(f"{self.extend_3_to_4.__name__}: "
                             f"row 값이 3이 아닙니다({self.rows}).")

        if self.kans[0] != 1:
            raise IndexError(f"{self.extend_3_to_4.__name__}: "
                             f"1번째 줄의 칸이 1개가 아닙니다({self.kans[0]}).")

        if self.kans[1] != 1:
            raise IndexError(f"{self.extend_3_to_4.__name__}: "
                             f"2번째 줄의 칸이 1개가 아닙니다({self.kans[1]}).")

        if self.kans[2] != 1:
            raise IndexError(f"{self.extend_3_to_4.__name__}: "
                             f"3번째 줄의 칸이 1개가 아닙니다({self.kans[2]}).")

        note_2_type = self.kans_obj[1][0].type
        note_2_value = self.kans_obj[1][0].text()
        note_2_key = self.kans_obj[1][0].key
        note_2_octave = self.kans_obj[1][0].octave

        note_3_type = self.kans_obj[2][0].type
        note_3_value = self.kans_obj[2][0].text()
        note_3_key = self.kans_obj[2][0].key
        note_3_octave = self.kans_obj[2][0].octave

        self.erase_row(2)
        self.append(0)
        self.append(1)

        if note_2_type == "note":
            self.kans_obj[0][1].set_note(note_2_key, note_2_octave)
        elif note_2_type == "jangsikeum":
            self.kans_obj[0][1].set_jangsikeun(note_2_key)

        if note_3_type == "note":
            self.kans_obj[1][0].set_note(note_3_key, note_3_octave)
        elif note_3_type == "jangsikeum":
            self.kans_obj[1][0].set_jangsikeun(note_3_key)

        return self.kans_obj[1][1]

    def extend_4_to_5(self) -> "Kan":
        if self.rows != 2:
            raise IndexError(f"{self.extend_4_to_5.__name__}: "
                             f"row 값이 2가 아닙니다({self.rows}).")

        if self.kans[0] != 2:
            raise IndexError(f"{self.extend_4_to_5.__name__}: "
                             f"1번째 줄의 칸이 2개가 아닙니다({self.kans[0]}).")

        if self.kans[1] != 2:
            raise IndexError(f"{self.extend_4_to_5.__name__}: "
                             f"2번째 줄의 칸이 2개가 아닙니다({self.kans[1]}).")

        self.append_row()

        return self.kans_obj[2][0]

    def extend_5_to_6(self) -> "Kan":
        if self.rows != 3:
            raise IndexError(f"{self.extend_5_to_6.__name__}: "
                             f"row 값이 3이 아닙니다({self.rows}).")

        if self.kans[0] != 2:
            raise IndexError(f"{self.extend_5_to_6.__name__}: "f""
                             f"1번째 줄의 칸이 2개가 아닙니다({self.kans[0]}).")

        if self.kans[1] != 2:
            raise IndexError(f"{self.extend_5_to_6.__name__}: "
                             f"2번째 줄의 칸이 2개가 아닙니다({self.kans[1]}).")

        if self.kans[2] != 1:
            raise IndexError(f"{self.extend_5_to_6.__name__}: "
                             f"3번째 줄의 칸이 1개가 아닙니다({self.kans[2]}).")

        self.append(self.rows - 1)

        return self.kans_obj[2][1]

    def get_max_kan(self, row=None) -> list:
        if row is None:  # last row + col
            return [self.rows - 1, self.kans[self.rows - 1] - 1]
        else:
            return [row, self.kans[row] - 1]

    def find_kan(self, _id: int) -> list:
        row_num = 0
        col_num = 0

        for row in self.kans_obj:
            col_num = 0

            for kan in row:
                if kan.id == _id:
                    return [row_num, col_num]
                col_num += 1
            row_num += 1

        raise Exception(f"{self.find_kan.__name__}: 논리 오류.")

    def find_kan_by_pos(self, _row: int, _col: int):
        if _row >= self.rows:
            return self.kans_obj[self.rows - 1][self.kans[self.rows - 1]]  # the last Kan
        if _col >= self.kans[_row]:
            return self.kans_obj[_row][self.kans[_row]]  # the last Kan

        return self.kans_obj[_row][_col]

    def find_next_kan(self, _id: int):
        curr_pos = self.find_kan(_id)

        if curr_pos[1] == self.kans[curr_pos[0]] - 1:  # the last Kan of the row
            if curr_pos[0] == self.rows - 1:  # the last Kan
                next_jeonggan = self.parent.find_next_jeonggan(self.id)

                if next_jeonggan.id == self.id:  # not next
                    return self.kans_obj[curr_pos[0]][curr_pos[1]]
                else:  # next
                    return next_jeonggan.find_kan_by_pos(0, 0)
            else:
                return self.kans_obj[curr_pos[0] + 1][0]
        else:
            return self.kans_obj[curr_pos[0]][curr_pos[1] + 1]

    def exist_next_kan(self, _id: int) -> bool:
        curr_pos = self.find_kan(_id)
        return curr_pos[1] != self.kans[curr_pos[0]] - 1  # the last Kan of the row

    def find_top_kan(self, _id: int):
        curr_pos = self.find_kan(_id)

        if curr_pos[0] == 0:  # the first Kan
            prev_jeonggan = self.parent.find_prev_jeonggan(self.id)
            prev_jeonggan_max_row = prev_jeonggan.get_rows() - 1
            candidate_pos_col = prev_jeonggan.get_max_kan(prev_jeonggan_max_row)[1]

            if prev_jeonggan.id == self.id:  # not prev
                return self.kans_obj[curr_pos[0]][curr_pos[1]]
            else:  # prev
                if candidate_pos_col < curr_pos[1]:
                    return prev_jeonggan.find_kan_by_pos(prev_jeonggan_max_row, candidate_pos_col)
                else:
                    return prev_jeonggan.find_kan_by_pos(prev_jeonggan_max_row, curr_pos[1])
        else:
            candidate_pos_col = self.get_max_kan(curr_pos[0] - 1)[1]
            if candidate_pos_col < curr_pos[1]:
                return self.kans_obj[curr_pos[0] - 1][candidate_pos_col]
            else:
                return self.kans_obj[curr_pos[0] - 1][curr_pos[1]]

    def find_prev_kan(self, _id: int):
        curr_pos = self.find_kan(_id)

        if curr_pos[1] == 0:  # the first Kan of the row
            if curr_pos[0] == 0:  # the first Kan
                prev_jeonggan = self.parent.find_prev_jeonggan(self.id)
                prev_jeonggan_max_row = prev_jeonggan.get_max_kan()

                if prev_jeonggan.id == self.id:  # not prev
                    return self.kans_obj[curr_pos[0]][curr_pos[1]]
                else:  # prev
                    return prev_jeonggan.find_kan_by_pos(*prev_jeonggan_max_row)
            else:
                return self.kans_obj[curr_pos[0] - 1][self.kans[curr_pos[0] - 1] - 1]
        else:
            return self.kans_obj[curr_pos[0]][curr_pos[1] - 1]

    def exist_prev_kan(self, _id: int) -> bool:
        curr_pos = self.find_kan(_id)
        return curr_pos[1] != 0  # the first Kan of the row

    def find_bottom_kan(self, _id: int):
        curr_pos = self.find_kan(_id)

        if curr_pos[0] == self.rows - 1:  # the last Kan
            next_jeonggan = self.parent.find_next_jeonggan(self.id)
            candidate_pos_col = next_jeonggan.get_max_kan(0)[1]

            if next_jeonggan.id == self.id:  # not next
                return self.kans_obj[curr_pos[0]][curr_pos[1]]
            else:  # next
                if candidate_pos_col < curr_pos[1]:
                    return next_jeonggan.find_kan_by_pos(0, candidate_pos_col)
                else:
                    return next_jeonggan.find_kan_by_pos(0, curr_pos[1])
        else:
            candidate_pos_col = self.get_max_kan(curr_pos[0] + 1)[1]
            if candidate_pos_col < curr_pos[1]:
                return self.kans_obj[curr_pos[0] + 1][candidate_pos_col]
            else:
                return self.kans_obj[curr_pos[0] + 1][curr_pos[1]]

    def get_kans(self, rec_list: list = None) -> int:
        count = 0
        if rec_list is None:
            rec_list = self.kans_obj

        for item in rec_list:
            if isinstance(item, list):
                count += self.get_kans(item)
            else:
                count += 1

        return count

    def get_id(self) -> int:
        return self.id


class Kan(QLabel):
    count = 0
    clicked_obj = None

    key_mapping = None

    JANGSIKEUM = ["nire", "nira", "none", "neone", "noniro", "nanireu", "neuronireu", "nanina",
                  "naneuna", "neunireu", "ni", "ri", "no", "ro", "nina"]

    def __init__(self, rows=0, cols=0, is_first: bool = False, is_last: bool = False,
                 parent: Jeonggan = None):
        super().__init__()

        self.is_first = is_first
        self.is_last = is_last
        self.parent = parent

        self.is_empty = True
        self.id = Kan.count
        Kan.count += 1
        if Kan.clicked_obj is None:
            Kan.clicked_obj = self

        self.rows = rows
        self.cols = cols

        self.set_style()

        self.setMargin(0)
        self.setContentsMargins(0, 0, 0, 0)

        self.type = None
        self.key = None
        self.setText("")
        self.octave = 0

        self.isClicked = False

        self.menu = QMenu()
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        for key in Kan.JANGSIKEUM:
            action = QAction(key, self)
            action.setIcon(QIcon(IMAGE_PATH + f"/jangsikeum/{key}.png"))
            action.triggered.connect(lambda _, l=key: self.set_jangsikeun(label_type=l))
            self.menu.addAction(action)

        self.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, pos) -> None:
        print(pos)
        self.menu.exec_(self.mapToGlobal(pos))

    def set_style(self) -> None:
        global css_content
        if css_content is None:
            with open(CSS_FILE_PATH, 'r') as f:
                css_content = f.read()

        font_size = 16

        if max(self.rows, self.cols) == 1:
            font_size = 24
        elif max(self.rows, self.cols) == 2:
            font_size = 18
        elif max(self.rows, self.cols) == 3:
            font_size = 14

        css_clicked = json_extract(css_content, "Kan", "clicked")
        css_first = json_extract(css_content, "Kan", "first")
        css_last = json_extract(css_content, "Kan", "last")

        stylesheet = f"font-size: {font_size}pt;"

        if self.is_first:
            stylesheet += css_first

        if self.is_last:
            stylesheet += css_last

        if Kan.clicked_obj is not None:
            if Kan.clicked_obj.id == self.id:
                stylesheet += css_clicked

        self.setStyleSheet(stylesheet)

        self.setFixedHeight(66 // self.rows)
        self.setFixedWidth(54 // self.cols)
        self.setAlignment(QtCore.Qt.AlignCenter)

    def get_rows(self) -> int:
        return self.rows

    def get_cols(self) -> int:
        return self.cols

    def set_rows(self, rows: int):
        self.rows = rows
        self.set_style()

    def set_cols(self, cols: int):
        self.cols = cols
        self.set_style()

    def set_is_first(self, is_first: bool):
        self.is_first = is_first
        self.set_style()

    def set_is_last(self, is_last: bool):
        self.is_last = is_last
        self.set_style()

    def click(self, set_style: bool = True):
        last_clicked_obj = Kan.clicked_obj
        Kan.clicked_obj = self
        if set_style:
            last_clicked_obj.set_style()
            self.set_style()

    def mousePressEvent(self, event):
        position = event.pos()
        print(f"Clicked at position: {position.x()}, {position.y()}")
        print(f"x: {self.geometry().x()}, y: {self.geometry().y()}, "
              f"width: {self.geometry().width()}, height: {self.geometry().height()}")

        self.click()

    def input_by_keyboard(self, key: str, octave: int = 0):
        if Kan.key_mapping is None:
            with open(KEY_MAPPING_PATH, 'r') as f:
                Kan.key_mapping = json.load(f)

        print("Key Pressed:", key)
        self.parent.parent.parent.parent.parent.is_saved = False

        max_kan_row, max_kan_col = self.parent.get_max_kan()
        my_row, my_col = self.parent.find_kan(self.id)
        dict_pitchname = PitchName.__members__.items()
        dict_etc_note = PitchEtcName.__members__.items()
        list_all_note = list(dict_pitchname) + list(dict_etc_note)

        for pitchname_key, pitchname_member in list_all_note:
            if key in Kan.key_mapping[pitchname_key]:
                next_kan = None

                note = None
                self.octave = octave
                if octave == 0:
                    note = pitchname_member.value
                elif octave == 1:
                    for pitchname_key_1, pitchname_member_1 in PitchNamePlus1.__members__.items():
                        if pitchname_key == pitchname_key_1:
                            note = pitchname_member_1.value
                            break
                elif octave == 2:
                    for pitchname_key_1, pitchname_member_1 in PitchNamePlus2.__members__.items():
                        if pitchname_key == pitchname_key_1:
                            note = pitchname_member_1.value
                            break
                elif octave == -1:
                    for pitchname_key_1, pitchname_member_1 in PitchNameMinus1.__members__.items():
                        if pitchname_key == pitchname_key_1:
                            note = pitchname_member_1.value
                            break
                elif octave == -2:
                    for pitchname_key_1, pitchname_member_1 in PitchNameMinus2.__members__.items():
                        if pitchname_key == pitchname_key_1:
                            note = pitchname_member_1.value
                            break
                elif isinstance(pitchname_member, PitchName):  # 음표이지만 옥타브 인자가 없음
                    raise Exception(f"{self.input_by_keyboard.__name__}: "
                                    f"옥타브 값이 -2~2의 정수가 아닙니다({octave}).")
                else:  # 음표가 아님
                    note = pitchname_member.value

                if self.is_empty:  # insert
                    self.set_note(pitchname_key, octave)
                    next_kan = self.parent.find_next_kan(self.id)
                else:  # insert & append
                    # 1 beat -> 2 beats
                    if max_kan_row == 0 \
                            and self.parent.get_max_kan(0)[1] == 0 \
                            and self.parent.find_kan(self.id) == self.parent.get_max_kan():
                        next_kan = self.parent.extend_1_to_2()

                    # 2 beats -> 3 beats
                    elif max_kan_row == 1 \
                            and self.parent.get_max_kan(0)[1] == 0 \
                            and self.parent.get_max_kan(1)[1] == 0 \
                            and self.parent.find_kan(self.id) == self.parent.get_max_kan():
                        next_kan = self.parent.extend_2_to_3()

                    # 3 beats -> 4 beats
                    elif max_kan_row == 2 \
                            and self.parent.get_max_kan(0)[1] == 0 \
                            and self.parent.get_max_kan(1)[1] == 0 \
                            and self.parent.get_max_kan(2)[1] == 0 \
                            and self.parent.find_kan(self.id) == self.parent.get_max_kan():
                        next_kan = self.parent.extend_3_to_4()

                    # 4 beats -> 5 beats
                    elif max_kan_row == 1 \
                            and self.parent.get_max_kan(0)[1] == 1 \
                            and self.parent.get_max_kan(1)[1] == 1 \
                            and self.parent.find_kan(self.id) == self.parent.get_max_kan():
                        next_kan = self.parent.extend_4_to_5()

                    # 5 beats -> 6 beats
                    elif max_kan_row == 2 \
                            and self.parent.get_max_kan(0)[1] == 1 \
                            and self.parent.get_max_kan(1)[1] == 1 \
                            and self.parent.get_max_kan(2)[1] == 0 \
                            and self.parent.find_kan(self.id) == self.parent.get_max_kan():
                        next_kan = self.parent.extend_5_to_6()

                    # 6 beats -> the next Jeonggan
                    elif max_kan_row == 2 and max_kan_col == 1 \
                            and self.parent.get_kans() == 6 \
                            and self.parent.find_kan(self.id) == self.parent.get_max_kan():
                        next_kan = self.parent.find_next_kan(self.id)

                    else:
                        if self.parent.get_max_kan(my_row)[1] >= 2 \
                                and self.parent.get_max_kan(my_row)[1] == my_col \
                                and self.parent.get_rows() - 1 == my_row \
                                and self.parent.get_rows() < 3:  # append a row
                            next_kan = self.parent.append_row()
                        elif not self.parent.exist_next_kan(self.id) \
                                and self.parent.get_max_kan(my_row)[1] < 2:  # extend
                            next_kan = self.parent.append(my_row)
                        else:
                            next_kan = self.parent.find_next_kan(self.id)

                    next_kan.set_note(pitchname_key, octave)

                    if next_kan is None:
                        raise Exception(f"{self.input_by_keyboard.__name__}: 다음 칸 정보가 없습니다.")

                    next_kan.click()

                break
        else:
            if key in Kan.key_mapping["MOVE_RIGHT"]:
                (self.parent.find_next_kan(self.id)).click()

            elif key in Kan.key_mapping["MOVE_LEFT"]:
                (self.parent.find_prev_kan(self.id)).click()

            elif key in Kan.key_mapping["MOVE_UP"]:
                self.parent.find_top_kan(self.id).click()

            elif key in Kan.key_mapping["MOVE_DOWN"]:
                self.parent.find_bottom_kan(self.id).click()

            elif key in Kan.key_mapping["MOVE_TO_THE_PREV_JEONGGAN"]:
                tmp_prev_jeonggan = self.parent.parent.find_prev_jeonggan(self.parent.get_id())
                tmp_prev_jeonggan.find_kan_by_pos(*tmp_prev_jeonggan.get_max_kan()).click()

            elif key in Kan.key_mapping["MOVE_TO_THE_NEXT_JEONGGAN"]:
                tmp_next_jeonggan = self.parent.parent.find_next_jeonggan(self.parent.get_id())
                tmp_next_jeonggan.find_kan_by_pos(0, 0).click()

            elif key in Kan.key_mapping["DELETE"]:
                self.clear_all()

            elif key in Kan.key_mapping["ERASE"]:
                if self.parent.get_max_kan(self.parent.find_kan(self.id)[0])[1] == 0:
                    if self.parent.get_rows() > 1:
                        (self.parent.find_prev_kan(self.id)).click()
                        self.parent.erase_row(self.parent.find_kan(self.id)[0])
                    else:  # deletion instead of erasing
                        self.clear_all()
                        (self.parent.find_prev_kan(self.id)).click()
                else:
                    (self.parent.find_prev_kan(self.id)).click()
                    self.parent.erase(self.id)
                    del self

            elif key in Kan.key_mapping["NEWLINE"]:
                if self.parent.get_rows() < 3:  # insert a row
                    next_kan = self.parent.insert_row(my_row + 1)
                    next_kan.click()
                else:  # move to the next Kan
                    (self.parent.find_next_kan(self.id)).click()

            elif key in Kan.key_mapping["INSERT_LEFT"]:
                prev_kan = None

                if self.parent.get_max_kan(my_row)[1] >= 2 \
                        and my_col == 0 \
                        and self.parent.get_rows() < 3:  # insert a row
                    prev_kan = self.parent.insert_row(my_row)
                elif self.parent.get_max_kan(my_row)[1] < 2:
                    prev_kan = self.parent.insert(my_row, my_col)
                else:
                    prev_kan = self.parent.find_prev_kan(self.id)
                prev_kan.click()

            elif key in Kan.key_mapping["INSERT_RIGHT"]:
                next_kan = None

                if self.parent.get_max_kan(my_row)[1] >= 2 \
                        and self.parent.get_max_kan(my_row)[1] == my_col \
                        and self.parent.get_rows() < 3:  # insert a row
                    next_kan = self.parent.insert_row(my_row + 1)
                elif self.parent.get_max_kan(my_row)[1] < 2:
                    next_kan = self.parent.insert(my_row, my_col + 1)
                else:
                    next_kan = self.parent.find_next_kan(self.id)
                next_kan.click()

            else:
                print("Unknown Command: ", key)

    @staticmethod
    def find_value_by_key(key: str, octave: int = 0) -> str:
        dict_pitchname = PitchName.__members__.items()
        dict_etc_note = PitchEtcName.__members__.items()

        note = None

        for pitchname_key, pitchname_member in dict_etc_note:
            if key == pitchname_key:
                return pitchname_member.value

        for pitchname_key, pitchname_member in dict_pitchname:
            if key == pitchname_key:
                if octave == 0:
                    note = pitchname_member.value
                elif octave == 1:
                    for pitchname_key_1, pitchname_member_1 in PitchNamePlus1.__members__.items():
                        if pitchname_key == pitchname_key_1:
                            note = pitchname_member_1.value
                            break
                elif octave == 2:
                    for pitchname_key_1, pitchname_member_1 in PitchNamePlus2.__members__.items():
                        if pitchname_key == pitchname_key_1:
                            note = pitchname_member_1.value
                            break
                elif octave == -1:
                    for pitchname_key_1, pitchname_member_1 in PitchNameMinus1.__members__.items():
                        if pitchname_key == pitchname_key_1:
                            note = pitchname_member_1.value
                            break
                elif octave == -2:
                    for pitchname_key_1, pitchname_member_1 in PitchNameMinus2.__members__.items():
                        if pitchname_key == pitchname_key_1:
                            note = pitchname_member_1.value
                            break
                elif isinstance(pitchname_member, PitchName):  # 음표이지만 옥타브 인자가 없음
                    raise Exception(f"{Kan.find_value_by_key.__name__}: "
                                    f"옥타브 값이 -2~2의 정수가 아닙니다({octave}).")
                else:  # 음표가 아님
                    note = pitchname_member.value

                break

        return note

    def set_note(self, key: str, octave: int = 0) -> None:
        value = Kan.find_value_by_key(key, octave)

        self.clear()
        self.setText(value)
        self.key = key
        self.type = "note"
        self.octave = octave

        if key is None:
            self.is_empty = True
        else:
            self.is_empty = False

    def set_jangsikeun(self, label_type: str) -> None:
        self.clear()
        self.setText("")
        self.setPixmap(QPixmap(IMAGE_PATH + f"/jangsikeum/{label_type}.png"))
        self.key = label_type
        self.type = "jangsikeum"
        self.octave = 0

        self.is_empty = False

    def clear_all(self):
        self.clear()
        self.setText("")
        self.type = None
        self.is_empty = True
        self.octave = 0


def json_extract(text: str, object_name: str, suffix: str) -> str:
    start_index = text.find(object_name + ":" + suffix + " {")
    end_index = text.find("}", start_index)
    return text[start_index + len(object_name + ":" + suffix + " {") + 2:end_index - 1]