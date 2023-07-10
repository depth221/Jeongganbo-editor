import sys
import json

from PyQt5.QtCore import QTimer, QCoreApplication
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip, QStatusBar, QMainWindow, \
    QApplication, QGridLayout, QLabel, QAction, qApp, QDesktopWidget, QShortcut, QDialog, QStackedWidget, QVBoxLayout, \
    QFrame, QScrollArea, QFileDialog, QMessageBox, QHBoxLayout, QLineEdit, QFormLayout
from PyQt5.QtGui import QFont, QIcon, QColor, QKeySequence, QPalette, QScreen
from PyQt5 import QtCore

from jeonggan import Page, TopPart, TitlePart, Gasaran, Gak, Gang, Jeonggan, Kan
from pitch_name import PitchName
from save_xml import SaveJGBX


class MyApp(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.set_style()
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        self.gaks = 6
        self.gangs = 4
        self.jeonggans = 3

        self.octave = 0

        self.curr_page = 1

        self.shortcuts = dict()

        self.key_mapping()

        self.main_widget = QStackedWidget()
        self.pages_obj = list()
        self.add_new_page(title=True)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.main_widget)

        self.potential_error_in_exporting_page: list[str] = []
        self.is_saved = True

        self.toolbar = None
        self.new_file_dialog = QDialog()

        self.init_ui()

    def set_style(self):
        with open("style.css", 'r') as f:
            self.setStyleSheet(f.read())

    def init_ui(self):
        self.statusBar.showMessage('Ready')

        # self.add_push_button()

        self.menuBar().setNativeMenuBar(False)

        self.add_file_items()

        self.main_widget.setAutoFillBackground(True)
        p = QPalette()
        p.setColor(QPalette.Background, QColor(239, 239, 239))
        self.main_widget.setPalette(p)

        self.setCentralWidget(self.scroll_area)

        screen = QApplication.primaryScreen()
        screen_width, screen_height = screen.geometry().width(), screen.geometry().height()
        width, height = 800, 950

        self.setWindowTitle(f"정간보 편집기 - {len(self.pages_obj)}쪽 중 {self.curr_page}쪽")
        self.statusBar.showMessage(f"{len(self.pages_obj)}쪽 중 {self.curr_page}쪽")
        self.setGeometry((screen_width - width) // 2, (screen_height - height) // 2, width, height)
        self.center()
        self.show()

    def add_file_items(self):
        filemenu = self.menuBar().addMenu('&File')
        self.toolbar = self.addToolBar('Tools')

        # new file
        new_action = QAction(QIcon('image/new.svg'), 'New File', self)
        new_action.setShortcut('Ctrl+N')
        new_action.setStatusTip('Make a the file')
        new_action.triggered.connect(self.new_file)

        filemenu.addAction(new_action)
        self.toolbar.addAction(new_action)

        # save
        save_action = QAction(QIcon('image/save.svg'), 'Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.setStatusTip('Save the file')
        save_action.triggered.connect(self.save_as)

        filemenu.addAction(save_action)
        self.toolbar.addAction(save_action)

        # export
        export_action = QAction(QIcon('image/export.svg'), 'Export', self)
        export_action.setShortcut('Ctrl+E')
        export_action.setStatusTip('Export the file')
        export_action.triggered.connect(self.export_wait)

        filemenu.addAction(export_action)
        self.toolbar.addAction(export_action)

        # exit
        exit_action = QAction(QIcon('image/exit.svg'), 'Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(self.close)

        filemenu.addAction(exit_action)
        self.toolbar.addAction(exit_action)

    def add_push_button(self):
        btn = QPushButton('Quit', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.move(50, 50)
        btn.resize(btn.sizeHint())
        btn.clicked.connect(QCoreApplication.instance().quit)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def set_octave(self, octave: int):
        self.octave = octave
        print("set_octave: ", self.octave)

    def get_octave(self) -> int:
        return self.octave

    def call_prev_page(self):
        if self.curr_page != 1:
            self.curr_page -= 1

        self.main_widget.setCurrentIndex(self.curr_page - 1)
        self.setWindowTitle(f"정간보 편집기 - {len(self.pages_obj)}쪽 중 {self.curr_page}쪽")
        self.statusBar.showMessage(f"{len(self.pages_obj)}쪽 중 {self.curr_page}쪽")

    def find_prev_page(self):
        self.call_prev_page()

        return self.pages_obj[self.curr_page - 1]

    def call_next_page(self):
        if self.curr_page == len(self.pages_obj):
            self.add_new_page(title=False)

        self.curr_page += 1
        self.main_widget.setCurrentIndex(self.curr_page - 1)
        self.setWindowTitle(f"정간보 편집기 - {len(self.pages_obj)}쪽 중 {self.curr_page}쪽")
        self.statusBar.showMessage(f"{len(self.pages_obj)}쪽 중 {self.curr_page}쪽")

    def find_next_page(self):
        self.call_next_page()

        return self.pages_obj[self.curr_page - 1]

    def key_mapping(self):
        key_mapping_file_path = "key_mapping.json"

        with open(key_mapping_file_path, 'r') as f:
            key_mapping = json.load(f)

        for key in PitchName.__members__.keys():
            self.shortcuts[key] = list()

            try:
                for shortcut in key_mapping[key]:
                    print("key: ", shortcut)
                    tmp_shortcut = QShortcut(QKeySequence(shortcut), self)
                    tmp_shortcut.activated.connect(
                        lambda k=shortcut: Kan.clicked_obj.input_by_keyboard(k, self.octave))
                    self.shortcuts[key].append(tmp_shortcut)
            except KeyError as e:
                print(f"경고: {e}의 단축키가 {key_mapping_file_path}에 없습니다.", file=sys.stderr)

        for key in ["REST", "CONTINUOUS",
                    "MOVE_LEFT", "MOVE_RIGHT", "MOVE_UP", "MOVE_DOWN",
                    "MOVE_TO_THE_PREV_JEONGGAN", "MOVE_TO_THE_NEXT_JEONGGAN",
                    "DELETE", "ERASE", "NEWLINE",
                    "INSERT_LEFT", "INSERT_RIGHT"]:
            self.shortcuts[key] = list()

            try:
                for shortcut in key_mapping[key]:
                    print("key: ", shortcut)
                    tmp_shortcut = QShortcut(QKeySequence(shortcut), self)
                    tmp_shortcut.activated.connect(
                        lambda k=shortcut: Kan.clicked_obj.input_by_keyboard(k))
                    self.shortcuts[key].append(tmp_shortcut)
            except KeyError as e:
                print(f"경고: {e}의 단축키가 {key_mapping_file_path}에 없습니다.", file=sys.stderr)

        for key in ["OCTAVE_UP"]:
            self.shortcuts[key] = list()

            try:
                for shortcut in key_mapping[key]:
                    print("key: ", shortcut)
                    tmp_shortcut = QShortcut(QKeySequence(shortcut), self)
                    tmp_shortcut.activated.connect(
                        lambda: self.set_octave(-2) if self.octave >= 2 else self.set_octave(self.octave + 1)
                    )
            except KeyError as e:
                print(f"경고: {e}의 단축키가 {key_mapping_file_path}에 없습니다.", file=sys.stderr)

        for key in ["OCTAVE_DOWN"]:
            self.shortcuts[key] = list()

            try:
                for shortcut in key_mapping[key]:
                    print("key: ", shortcut)
                    tmp_shortcut = QShortcut(QKeySequence(shortcut), self)
                    tmp_shortcut.activated.connect(
                        lambda: self.set_octave(2) if self.octave <= -2 else self.set_octave(self.octave - 1)
                    )
            except KeyError as e:
                print(f"경고: {e}의 단축키가 {key_mapping_file_path}에 없습니다.", file=sys.stderr)

        for key in ["PREV_PAGE"]:
            self.shortcuts[key] = list()

            try:
                for shortcut in key_mapping[key]:
                    print("key: ", shortcut)
                    tmp_shortcut = QShortcut(QKeySequence(shortcut), self)
                    tmp_shortcut.activated.connect(self.call_prev_page)
            except KeyError as e:
                print(f"경고: {e}의 단축키가 {key_mapping_file_path}에 없습니다.", file=sys.stderr)

        for key in ["NEXT_PAGE"]:
            self.shortcuts[key] = list()

            try:
                for shortcut in key_mapping[key]:
                    print("key: ", shortcut)
                    tmp_shortcut = QShortcut(QKeySequence(shortcut), self)
                    tmp_shortcut.activated.connect(self.call_next_page)
            except KeyError as e:
                print(f"경고: {e}의 단축키가 {key_mapping_file_path}에 없습니다.", file=sys.stderr)

    def export_wait(self):
        tmp_clicked_obj = Kan.clicked_obj
        Kan.clicked_obj = None
        tmp_clicked_obj.set_style()
        Kan.clicked_obj = tmp_clicked_obj

        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Export", "", "Image Files(*.png);;All Files(*)",
                                                   options=options)

        if file_name:
            if file_name[-4:] != ".png":
                file_name += ".png"

            self.showFullScreen()
            original_curr_page = self.curr_page
            self.toolbar.setEnabled(False)
            self.statusBar.showMessage("정간보를 내보내는 중입니다... 저장 중에는 정간보 화면 위에 다른 창을 올려놓지 마세요!")

            QTimer.singleShot(500, lambda: self.export(file_name, original_curr_page))

    def export(self, path: str, original_page: int):
        for i in range(len(self.pages_obj)):
            QTimer.singleShot(500 + 500 * (i + 1) + 250,
                              lambda page=i + 1, p=path, o=original_page:
                              self.export_each_page(page, p, o)
                              )
            QTimer.singleShot(500 + 500 * (i + 1),
                              lambda page=i + 1:
                              self.main_widget.setCurrentIndex(page - 1)
                              )

    def export_each_page(self, page: int, path: str, original_page: int):
        self.setWindowTitle(f"정간보 편집기 - {len(self.pages_obj)}쪽 중 {page}쪽")
        self.statusBar.showMessage(f"정간보를 내보내는 중입니다({len(self.pages_obj)}쪽 중 {page}쪽" +
                                   f" - {round(page * 100 / len(self.pages_obj), 1)}%)... " +
                                   "저장 중에는 정간보 화면 위에 다른 창을 올려놓지 마세요!")

        height = self.pages_obj[page - 1].height()

        title_part = self.pages_obj[page - 1].page_layout.itemAtPosition(0, 2)
        left_part = self.pages_obj[page - 1].page_layout.itemAtPosition(0, 0)
        bottom_part = self.pages_obj[page - 1].page_layout.itemAtPosition(1, 0)

        if title_part.widget() is None:
            height = sum([left_part.itemAt(i).widget().height() for i in range(3)])
        else:
            height = title_part.widget().height() + bottom_part.widget().height()
        width = self.pages_obj[self.curr_page - 1].page_layout.itemAtPosition(1, 0).widget().width()

        screen_x, screen_y = self.pages_obj[self.curr_page - 1].page_layout.geometry().x(), self.geometry().y()
        screen_width, screen_height = self.geometry().width(), self.geometry().height()
        window = self.pages_obj[self.curr_page - 1].page_layout.geometry()

        screen = QApplication.primaryScreen()
        screenshot = screen.grabWindow(self.main_widget.winId(),
                                       left_part.geometry().x(), left_part.geometry().y(),
                                       bottom_part.geometry().x() + bottom_part.geometry().width()
                                       - left_part.geometry().x(),
                                       bottom_part.geometry().y() + bottom_part.geometry().height()
                                       - left_part.geometry().y())

        # potential cutoff for exporting
        if bottom_part.geometry().x() + bottom_part.geometry().width() > screen.geometry().width() or \
                bottom_part.geometry().y() + bottom_part.geometry().height() > screen.geometry().height():
            self.potential_error_in_exporting_page.append(str(page))

        if len(self.pages_obj) == 1:
            screenshot.save(path, 'png')
        else:
            screenshot.save(path[:-4] + f"_{page}p.png", 'png')

        if page == len(self.pages_obj):
            self.curr_page = original_page
            self.toolbar.setEnabled(True)
            self.showNormal()
            self.statusBar.showMessage("내보내기 완료!")

            if len(self.potential_error_in_exporting_page) != 0:
                QMessageBox.warning(None, "내보내기 경고", "컴퓨터의 해상도가 너무 작거나 페이지가 너무 커\n" +
                                    "잘린 상태로 저장된 페이지가 있을 수 있습니다.\n" +
                                    ', '.join(self.potential_error_in_exporting_page) + "쪽을 확인해 보세요.")

            self.potential_error_in_exporting_page.clear()

    def closeEvent(self, event):
        if self.is_saved:
            event.accept()
        else:
            exit_result = QMessageBox.question(None, "아직 저장하지 않음",
                                               "변경 내역을 저장하지 않았습니다. 정말 종료하시겠습니까?",
                                               QMessageBox.Yes | QMessageBox.No)
            if exit_result == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()

    def new_file(self) -> None:
        if not self.is_saved:
            new_file_result = QMessageBox.question(None, "아직 저장하지 않음",
                                                   "변경 내역을 저장하지 않았습니다. 정말 새로운 정간보를 만드시겠습니까?",
                                                   QMessageBox.Yes | QMessageBox.No)
            if new_file_result != QMessageBox.Yes:
                return

        form_layout = QFormLayout()
        dialog_layout = QVBoxLayout()

        self.new_file_dialog.setLayout(dialog_layout)
        self.new_file_dialog.setContentsMargins(0, 0, 0, 0)
        form_layout.setContentsMargins(0, 0, 0, 0)

        gak_widget = QLineEdit()
        gang_widget = QLineEdit()
        jeonggan_widget = QLineEdit()
        gak_widget.setText("6")
        gang_widget.setText("4")
        jeonggan_widget.setText("3")

        new_cancel_layout = QHBoxLayout()
        new_cancel_layout.setAlignment(QtCore.Qt.AlignHCenter)

        new_button = QPushButton("생성")
        new_button.clicked.connect(
            lambda: self.add_new_file(gak_widget.text(), gang_widget.text(), jeonggan_widget.text())
        )

        new_cancel_layout.addWidget(new_button, alignment=QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)

        form_layout.addRow("한 페이지에 들어갈 각: ", gak_widget)
        form_layout.addRow("한 각에 들어갈 강: ", gang_widget)
        form_layout.addRow("한 강에 들어갈 정간: ", jeonggan_widget)

        dialog_layout.addLayout(form_layout)
        dialog_layout.addLayout(new_cancel_layout)

        self.new_file_dialog.setWindowTitle("새로운 정간보")
        self.new_file_dialog.setMinimumWidth(200)
        self.new_file_dialog.show()

    def add_new_page(self, title: bool = False) -> None:
        tmp_page = Page(gaks=self.gaks + (0 if title is True else 1), gangs=self.gangs, jeonggans=self.jeonggans,
                        title=title, _id=len(self.pages_obj), parent=self)

        self.pages_obj.append(tmp_page)
        self.main_widget.addWidget(tmp_page)

    def remove_all_page(self) -> None:
        for page in self.pages_obj:
            self.main_widget.removeWidget(page)
            page.deleteLater()

        self.pages_obj.clear()
        self.curr_page = 0
        Kan.clicked_obj = None

    def add_new_file(self, gak: int = 6, gang: int = 4, jeonggan: int = 3):
        self.new_file_dialog.close()

        try:
            gak = int(gak)
            if gak < 1:
                raise ValueError
        except ValueError:
            QMessageBox.critical(None, "새로운 정간보 생성 중 오류 발생", "'한 페이지에 들어갈 각'에 입력된 값이 자연수가 아닙니다." +
                                 "다시 입력해 주세요.")
            self.new_file()
            return

        try:
            gang = int(gang)
            if gang < 1:
                raise ValueError
        except ValueError:
            QMessageBox.critical(None, "새로운 정간보 생성 중 오류 발생", "'한 각에 들어갈 강'에 입력된 값이 자연수가 아닙니다." +
                                 "다시 입력해 주세요.")
            self.new_file()
            return

        try:
            jeonggan = int(jeonggan)
            if jeonggan < 1:
                raise ValueError
        except ValueError:
            QMessageBox.critical(None, "새로운 정간보 생성 중 오류 발생", "'한 강에 들어갈 정간'에 입력된 값이 자연수가 아닙니다." +
                                 "다시 입력해 주세요.")
            self.new_file()
            return

        self.remove_all_page()

        self.gaks = gak
        self.gangs = gang
        self.jeonggans = jeonggan

        self.add_new_page(title=True)
        self.curr_page = 1
        self.main_widget.setCurrentIndex(0)

        self.setWindowTitle(f"정간보 편집기 - {len(self.pages_obj)}쪽 중 {self.curr_page}쪽")
        self.statusBar.showMessage(f"{len(self.pages_obj)}쪽 중 {self.curr_page}쪽")

    def save_as(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save as...", "", "Jeongganbo XML File(*.jgbx);;All Files(*)",
                                                   options=options)

        if file_name:
            if file_name[-5:] != ".jgbx":
                file_name += ".jgbx"

            self.statusBar.showMessage("정간보를 저장하는 중입니다...")

            save_xml = SaveJGBX(pages=self.pages_obj)
            save_xml.save_xml(file_name=file_name)

            self.statusBar.showMessage("저장 완료!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
