from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QLabel
from PyQt5.QtGui import QColor

app = QApplication([])
window = QMainWindow()

stacked_widget = QStackedWidget()

# 첫 번째 위젯
widget1 = QLabel("첫 번째 위젯")
widget1.setStyleSheet("background-color: rgba(255, 255, 255, 0.5);")
stacked_widget.addWidget(widget1)

# 두 번째 위젯
widget2 = QLabel("두 번째 위젯")
widget2.setStyleSheet("background-color: rgba(0, 0, 255, 0.3);")
stacked_widget.addWidget(widget2)

window.setCentralWidget(stacked_widget)
window.show()
app.exec_()