import json
import re

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip, QStatusBar, QMainWindow, \
    QApplication, QGridLayout, QLabel, QAction, qApp, QDesktopWidget, QDialog, QLineEdit, QFormLayout, QHBoxLayout, \
    QVBoxLayout, QFrame
from PyQt5.QtGui import QFont, QIcon, QColor, QPalette, QFontMetrics
from PyQt5 import QtCore

from pitch_name import PitchName, PitchNamePlus1, PitchNamePlus2, PitchNameMinus1, PitchNameMinus2
from pitch_etc_name import PitchEtcName


class Page(QWidget):
    def __init__(self, gaks: int = 6, title: bool = False, _id: int = None, parent=None):
        super().__init__()

        self.parent = parent
        self.id = _id

        self.gaks = gaks
        self.gaks_obj = []  # list(QgridLayout)

        self.page_layout = QGridLayout()
        self.setLayout(self.page_layout)

        self.page_layout.setSpacing(0)
        self.page_layout.setContentsMargins(0, 0, 0, 0)
        self.page_layout.setAlignment(QtCore.Qt.AlignJustify)

        self.jeonggan_grid = QGridLayout()
        self.jeonggan_grid.setSpacing(0)
        self.jeonggan_grid.setContentsMargins(0, 0, 0, 0)

        self.page_layout.addWidget(TopPart(), 0, 0)
        self.page_layout.addLayout(self.jeonggan_grid, 1, 0)
        if title is True:
            self.page_layout.addLayout(TitlePart(), 0, 1, 2, 1)
        else:
            self.page_layout.addWidget(NonTitlePart(), 0, 1, 2, 1)

        for i in range(gaks - 1, -1, -1):
            tmp_gak = Gak(num=4, _id=gaks - i - 1, parent=self)
            self.jeonggan_grid.addLayout(tmp_gak, 0, i)
            self.gaks_obj.append(tmp_gak)

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
    css_content = None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.set_style()

        self.setMargin(0)
        self.setFixedHeight(70)

    def set_style(self) -> None:
        if TopPart.css_content is None:
            with open("style.css", 'r') as f:
                TopPart.css_content = f.read()

        self.setStyleSheet(TopPart.css_content)


class NonTitlePart(QLabel):
    css_content = None

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

        # subtitle font size
        s_css_style = json_extract(TitlePart.css_content, "TitlePart", "left")
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
        t_css_style = json_extract(TitlePart.css_content, "TitlePart", "right")  # title font size
        t_p = re.compile("font-size: ([0-9]+)pt;")
        t_search_result = t_p.search(t_css_style)

        t_font_size = 24  # default
        if t_search_result is not None:
            t_font_size = int(t_search_result.groups()[0])

        t_font = QFont("NanumGothic", t_font_size, QFont.Normal)
        t_font_metrics = QFontMetrics(t_font)
        t_px_from_pt = t_font_metrics.fontDpi() / 72 * t_font_size
        print(t_px_from_pt)

        self.setFixedWidth(30 + round(s_px_from_pt + t_px_from_pt) + 60 - 35 - 54)

        self.set_style()

    def set_style(self) -> None:
        if NonTitlePart.css_content is None:
            with open("style.css", 'r') as f:
                NonTitlePart.css_content = f.read()

        self.setStyleSheet(NonTitlePart.css_content)


class TitlePartFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

        self.setFrameShape(QFrame.Box)

    def mousePressEvent(self, event) -> None:
        position = event.pos()
        print(f"Clicked at position: {position.x()}, {position.y()}")
        print(f"x: {self.geometry().x()}, y: {self.geometry().y()}, "
              f"width: {self.geometry().width()}, height: {self.geometry().height()}")

        self.parent.dialog_open()


class TitlePart(QGridLayout):
    css_content = None

    def __init__(self, parent=None):
        super().__init__()
        self.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)

        self.frame = TitlePartFrame(parent=self)
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

    def set_style(self, obj, attr: str = None) -> None:
        if TitlePart.css_content is None:
            with open("style.css", 'r') as f:
                TitlePart.css_content = f.read()

        if attr is None:
            obj.setStyleSheet(TitlePart.css_content)
            return

        width_dict = {"left_margin": 30, "right_margin": 60}
        height_dict = {"top_margin": 100, "bottom_margin": 40}

        if attr in ["left_margin", "right_margin"]:
            css_style = json_extract(TitlePart.css_content, "TitlePart", attr)
            obj.setStyleSheet(css_style)
            obj.setFixedWidth(width_dict[attr])
        elif attr in ["top_margin", "bottom_margin"]:
            css_style = json_extract(TitlePart.css_content, "TitlePart", attr)
            obj.setStyleSheet(css_style)
            obj.setFixedHeight(height_dict[attr])
        elif attr in ["left", "right"]:  # subtitle, title
            css_style = json_extract(TitlePart.css_content, "TitlePart", attr)
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


class Gasaran(QLabel):
    css_content = None

    def __init__(self, beats=1, parent=None):
        super().__init__(parent)
        self.set_style()

        self.setMargin(0)
        self.setFixedWidth(35)

    def set_style(self) -> None:
        if Gasaran.css_content is None:
            with open("style.css", 'r') as f:
                Gasaran.css_content = f.read()

        self.setStyleSheet(Gasaran.css_content)


class Gak(QGridLayout):  # Gang * n
    def __init__(self, num=3, _id=None, parent=None):
        super().__init__()
        self.parent = parent
        self.id = _id

        self.gangs = num
        self.gangs_obj = []  # list(QgridLayout)

        self.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)

        for i in range(num):
            tmp_label = Gang(num=3, _id=i, parent=self)
            self.gangs_obj.append(tmp_label)
            self.addLayout(tmp_label, i, 1)

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
                return prev_gak.gangs_obj[prev_gak.get_max_gang()]
        else:
            return self.gangs_obj[_id - 1]


class Gang(QGridLayout):  # Gasaran + Jeonggan * n
    def __init__(self, num=3, _id=None, parent=None):
        super().__init__()
        self.parent = parent
        self.id = _id

        self.jeonggans = num
        self.jeonggans_obj = []  # list(QgridLayout)

        self.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)

        self.addWidget(Gasaran(), 0, 0, num, 1)
        for i in range(num):
            tmp_label = Jeonggan(row=1, _id=i, parent=self)

            self.jeonggans_obj.append(tmp_label)
            self.addLayout(tmp_label, i, 1)

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
    def __init__(self, row=1, _id=None, parent=None):
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

    def append(self, row: int):
        return self.insert(row, self.kans[row])

    def insert(self, row: int, col: int):
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

    def append_row(self):
        return self.insert_row(self.rows)

    def insert_row(self, row_pos: int):
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

    def extend_1_to_2(self):
        if self.rows != 1:
            raise IndexError(f"{self.extend_1_to_2.__name__}: "
                             f"row 값이 1이 아닙니다({self.rows}).")

        if self.kans[0] != 1:
            raise IndexError(f"{self.extend_1_to_2.__name__}: "
                             f"1번째 줄의 칸이 1개가 아닙니다({self.kans[0]}).")

        self.append_row()

        return self.kans_obj[1][0]

    def extend_2_to_3(self):
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

    def extend_3_to_4(self):
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

        note_2 = self.kans_obj[1][0].text()
        note_3 = self.kans_obj[2][0].text()

        self.erase_row(2)
        self.append(0)
        self.append(1)

        self.kans_obj[0][1].setText(note_2)
        self.kans_obj[1][0].setText(note_3)

        return self.kans_obj[1][1]

    def extend_4_to_5(self):
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

    def extend_5_to_6(self):
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
    css_content = None

    key_mapping = None

    def __init__(self, rows=0, cols=0, is_first: bool = False, is_last: bool = False,
                 parent: Jeonggan = None):
        super().__init__()

        self.is_first = is_first
        self.is_last = is_last
        self.parent = parent

        self.id = Kan.count
        Kan.count += 1
        if Kan.clicked_obj is None:
            Kan.clicked_obj = self

        self.rows = rows
        self.cols = cols

        self.set_style()

        self.setMargin(0)

        self.setText("")

        self.isClicked = False

    def set_style(self):
        if Kan.css_content is None:
            with open("style.css", 'r') as f:
                Kan.css_content = f.read()

        font_size = 16

        if max(self.rows, self.cols) == 1:
            font_size = 24
        elif max(self.rows, self.cols) == 2:
            font_size = 18
        elif max(self.rows, self.cols) == 3:
            font_size = 14

        css_clicked = json_extract(Kan.css_content, "Kan", "clicked")
        css_first = json_extract(Kan.css_content, "Kan", "first")
        css_last = json_extract(Kan.css_content, "Kan", "last")

        stylesheet = f"font-size: {font_size}pt;"

        if self.is_first:
            stylesheet += css_first

        if self.is_last:
            stylesheet += css_last

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

    def input_by_keyboard(self, key: str, octave: int = None):
        if Kan.key_mapping is None:
            with open('key_mapping.json', 'r') as f:
                Kan.key_mapping = json.load(f)

        print("Key Pressed:", key)

        max_kan_row, max_kan_col = self.parent.get_max_kan()
        my_row, my_col = self.parent.find_kan(self.id)
        dict_pitchname = PitchName.__members__.items()
        dict_etc_note = PitchEtcName.__members__.items()
        list_all_note = list(dict_pitchname) + list(dict_etc_note)

        for pitchname_key, pitchname_member in list_all_note:
            if key in Kan.key_mapping[pitchname_key]:
                next_kan = None

                note = None
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

                if self.text() in ["O", ""]:  # insert
                    self.setText(note)
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

                    next_kan.setText(note)

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
                self.setText("")

            elif key in Kan.key_mapping["ERASE"]:
                if self.parent.get_max_kan(self.parent.find_kan(self.id)[0])[1] == 0:
                    if self.parent.get_rows() > 1:
                        (self.parent.find_prev_kan(self.id)).click()
                        self.parent.erase_row(self.parent.find_kan(self.id)[0])
                    else:  # deletion instead of erasing
                        self.setText("")
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


def json_extract(text: str, object_name: str, suffix: str) -> str:
    start_index = text.find(object_name + ":" + suffix + " {")
    end_index = text.find("}", start_index)
    return text[start_index + len(object_name + ":" + suffix + " {") + 2:end_index - 1]
