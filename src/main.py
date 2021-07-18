from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QLineEdit,
    QMainWindow,
    QSplashScreen,
    QWidget,
    QSplitter,
    QVBoxLayout,
    QLabel
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys, os
import api

class CustomPage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level: 'QWebEnginePage.JavaScriptConsoleMessageLevel', message: str, lineNumber: int, sourceID: str) -> None:
        print(level)
        #return super().javaScriptConsoleMessage(level, message, lineNumber, sourceID)
        
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("OSFED")
        self.source_dir = os.path.abspath(os.path.dirname(__file__))
        self.icon = QIcon(os.path.join(self.source_dir, "images/designer.ico"))
        self.setWindowIcon(self.icon)

        self.central = QWidget()
        self.setCentralWidget(self.central)

        self.baseLayout = QVBoxLayout()
        self.central.setLayout(self.baseLayout)

        self.document = api.Doc()

        self.actionDocument = self.menuBar().addMenu("Document")
        self.actionDocument.addAction("New").triggered.connect(self.NewDocumentDialog)

        self.splitter = QSplitter()
        self.baseLayout.addWidget(self.splitter)

        #self.left = QWidget()
        #self.splitter.addWidget(self.left)

        self.right = QWidget()
        self.splitter.addWidget(self.right)

        self.layoutRight = QVBoxLayout()
        self.right.setLayout(self.layoutRight)

        self.browser = QWebEngineView()
        page = CustomPage(parent=self.browser)
        self.browser.setPage(page)
        self.browser.setHtml(api.genereteDocument(self.document))
        self.browser.loadFinished.connect(lambda: self.browser.page().runJavaScript('document.addEventListener("click", (data)=>{console.log(data.target.getAttribute("osfed"));});'))
        self.layoutRight.addWidget(self.browser)
    
    def NewDocumentDialog(self):
        dlg = QDialog()
        dlg.setWindowTitle("Add Element")
        dlg.setWindowIcon(self.icon)

        layout = QVBoxLayout()
        dlg.setLayout(layout)

        message = QLabel("Enter document name:")
        layout.addWidget(message)

        lineEdit = QLineEdit()
        lineEdit.setText("new-document")
        layout.addWidget(lineEdit)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.rejected.connect(dlg.reject)
        buttonBox.accepted.connect(dlg.accept)
        layout.addWidget(buttonBox)

        dlg.accepted.connect(lambda: self.createNewDocument(lineEdit.text()))

        dlg.exec_()
    
    def createNewDocument(self, name):
        self.document = api.new_document(name)
        self.browser.setHtml(api.genereteDocument(self.document))

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
