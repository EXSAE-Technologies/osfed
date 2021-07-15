from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QSplashScreen,
    QWidget,
    QSplitter,
    QVBoxLayout
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys, os
import test
import api

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("OSFED")
        self.source_dir = os.path.abspath(os.path.dirname(__file__))
        icon = QIcon(os.path.join(self.source_dir, "images/designer.ico"))
        self.setWindowIcon(icon)

        self.central = QWidget()
        self.setCentralWidget(self.central)

        self.baseLayout = QVBoxLayout()
        self.central.setLayout(self.baseLayout)

        self.splitter = QSplitter()
        self.baseLayout.addWidget(self.splitter)

        self.left = QWidget()
        self.splitter.addWidget(self.left)

        self.right = QWidget()
        self.splitter.addWidget(self.right)

        self.layoutRight = QVBoxLayout()
        self.right.setLayout(self.layoutRight)

        self.browser = QWebEngineView()
        self.browser.setHtml(test.show())
        self.layoutRight.addWidget(self.browser)

app = QApplication(sys.argv)

source_dir = os.path.abspath(os.path.dirname(__file__))
splash_pix = QPixmap(os.path.join(source_dir, "images/designer.png"))
splash = QSplashScreen(splash_pix)
splash.setMask(splash_pix.mask())
splash.show()
app.processEvents()

window = MainWindow()
window.show()

splash.finish(window)
app.exec_()