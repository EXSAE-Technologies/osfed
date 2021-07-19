from PyQt5.QtCore import QUrl, pyqtSignal
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
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
import sys, os
import api

class CustomPage(QWebEnginePage):
    onConsoleLog = pyqtSignal(int, str, int, str)
    def javaScriptConsoleMessage(self, level: 'QWebEnginePage.JavaScriptConsoleMessageLevel', message: str, lineNumber: int, sourceID: str) -> None:
        self.onConsoleLog.emit(int(level), message, lineNumber, sourceID)
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

        self.actionAdd = self.menuBar().addMenu("Add")
        self.actionAdd.addAction("Element").triggered.connect(self.NewElementDialog)

        self.browser = QWebEngineView()
        page = CustomPage(parent=self.browser)
        page.onConsoleLog.connect(self.console_log)
        self.browser.setPage(page)
        self.browser.setHtml(api.generateDocument(self.document))
        self.browser.loadFinished.connect(lambda: self.browser.page().runJavaScript('document.addEventListener("click", (data)=>{console.log(data.target.getAttribute("osfed"));});'))
        self.baseLayout.addWidget(self.browser)
    
    def console_log(self, level, message):
        if level == 0:
            if message == "null":
                print(message)
            else:
                self.EditElementDialog(message)
    
    def NewElementDialog(self):
        dlg = QDialog()
        dlg.setWindowTitle("Edit Element")
        dlg.setWindowIcon(self.icon)

        layout = QVBoxLayout()
        dlg.setLayout(layout)

        message = QLabel("New element")
        layout.addWidget(message)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.rejected.connect(dlg.reject)
        buttonBox.accepted.connect(dlg.accept)
        layout.addWidget(buttonBox)

        dlg.exec_()
    
    def EditElementDialog(self, index):
        dlg = QDialog()
        dlg.setWindowTitle("Edit Element")
        dlg.setWindowIcon(self.icon)

        layout = QVBoxLayout()
        dlg.setLayout(layout)

        message = QLabel(index)
        layout.addWidget(message)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.rejected.connect(dlg.reject)
        buttonBox.accepted.connect(dlg.accept)
        layout.addWidget(buttonBox)

        dlg.exec_()
    
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
        with open(os.path.join(self.source_dir, "tmp/"+name+".html"), "w") as file:
            file.write(api.generateDocument(self.document))

        self.browser.load(QUrl.fromLocalFile(os.path.join(self.source_dir, "tmp/"+name+".html")))

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
