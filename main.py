import sys
import json

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip, QStatusBar, QMainWindow, \
    QApplication, QGridLayout, QLabel, QAction, qApp, QDesktopWidget, QShortcut, QDialog, QStackedWidget, QVBoxLayout, \
    QFrame, QScrollArea, QFileDialog, QMessageBox
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
        self.pages_obj = list()
        self.pages_obj.append(Page(gaks=6, title=True, _id=0, parent=self))

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.main_widget)

        self.potential_error_in_exporting_page: list[str] = []
        self.is_saved = True

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
        saveAction.triggered.connect(self.export_wait)

        filemenu.addAction(saveAction)

        self.toolbar = self.addToolBar('Tools')
        self.toolbar.addAction(saveAction)

        # exit
        exitAction = QAction(QIcon('image/exit.svg'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

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
            exit_result = QMessageBox.question(None, "아직 저장하지 않음", "변경 내역을 저장하지 않았습니다. 정말 종료하시겠습니까?",
                                               QMessageBox.Yes | QMessageBox.No)
            if exit_result == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
