from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QWidget
)
import sys, os

class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("OSFED")
        source_dir = os.path.abspath(os.path.dirname(__file__))
        icon = QIcon(os.path.join(source_dir, "images/designer.ico"))
        self.setWindowIcon(icon)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()