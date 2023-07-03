import sys
import json

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip, QStatusBar, QMainWindow, \
    QApplication, QGridLayout, QLabel, QAction, qApp, QDesktopWidget, QShortcut, QDialog, QStackedWidget, QVBoxLayout, \
    QFrame, QScrollArea
from PyQt5.QtGui import QFont, QIcon, QColor, QKeySequence, QPalette, QScreen
from PyQt5 import QtCore

from jeonggan import Page, TopPart, TitlePart, Gasaran, Gak, Gang, Jeonggan, Kan
from pitch_name import PitchName


class MyApp(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.set_style()
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        self.octave = 0

        self.curr_page = 1

        self.shortcuts = dict()

        self.key_mapping()

        self.main_widget = QStackedWidget()
        # self.main_widget.setFrameShape(QFrame.Box)
        self.pages_obj = list()
        self.pages_obj.append(Page(gaks=6, title=True, _id=0, parent=self))

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.main_widget)

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

        for page in self.pages_obj:
            self.main_widget.addWidget(page)
        # self.setCentralWidget(self.main_widget)
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

        saveAction = QAction(QIcon('image/save.svg'), 'Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Save the file')
        saveAction.triggered.connect(qApp.quit)

        filemenu.addAction(saveAction)

        self.toolbar = self.addToolBar('Tools')
        self.toolbar.addAction(saveAction)

        # exit
        exitAction = QAction(QIcon('image/exit.svg'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        filemenu.addAction(exitAction)

        self.toolbar.addAction(exitAction)

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
            tmp_page = Page(gaks=7, _id=len(self.pages_obj), parent=self)
            self.pages_obj.append(tmp_page)
            self.main_widget.addWidget(tmp_page)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
