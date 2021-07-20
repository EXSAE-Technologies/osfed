from PyQt5.QtCore import QObject, QUrl, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFormLayout,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QPushButton,
    QSplashScreen,
    QStackedWidget,
    QToolBar,
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

class Document(QObject):
    viewUpdated = pyqtSignal()
    documentChanged = pyqtSignal()
    def __init__(self):
        QObject.__init__(self)
        self.doc = api.Doc()
    
    def changeDocument(self):
        self.documentChanged.emit()
    
    def updateView(self):
        self.viewUpdated.emit()
        
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("OSFED")
        self.source_dir = os.path.abspath(os.path.dirname(__file__))
        self.icon = QIcon(os.path.join(self.source_dir, "images/designer.ico"))
        self.setWindowIcon(self.icon)
        self.showMaximized()

        self.central = QWidget()
        self.setCentralWidget(self.central)

        self.baseLayout = QVBoxLayout()
        self.central.setLayout(self.baseLayout)

        self.document = Document()
        self.document.viewUpdated.connect(self.reloadView)
        self.document.documentChanged.connect(self.onDocumentChange)
        self.document.changeDocument()

        self.actionDocument = self.menuBar().addMenu("Document")
        self.actionDocument.addAction(QIcon(os.path.join(self.source_dir, "images/new_document.svg")), "New").triggered.connect(self.NewDocumentDialog)
        self.actionDocument.addAction(QIcon(os.path.join(self.source_dir, "images/save_document.svg")), "Save").triggered.connect(self.saveWorkSpace)
        self.actionDocument.addAction(QIcon(os.path.join(self.source_dir, "images/open_workspace.svg")), "Open").triggered.connect(self.openWorkSpace)

        self.toolBar = QToolBar()
        self.addToolBar(self.toolBar)
        self.toolBar.addAction(QIcon(os.path.join(self.source_dir, "images/new_element.svg")), "Add element").triggered.connect(self.NewElementDialog)

        self.browser = QWebEngineView()
        page = CustomPage(parent=self.browser)
        page.onConsoleLog.connect(self.console_log)
        self.browser.setPage(page)
        self.browser.setHtml(api.generateDocument(self.document.doc))
        self.browser.loadFinished.connect(lambda: self.browser.page().runJavaScript('document.addEventListener("dblclick", (data)=>{console.log(data.target.getAttribute("osfed"));});'))
        self.baseLayout.addWidget(self.browser)
    
    def console_log(self, level, message):
        if level == 0:
            if message == "null":
                print(message)
            else:
                self.EditElementDialog(message)
    
    def saveWorkSpace(self):
        filename = os.path.join(self.source_dir, "tmp/"+self.document.doc.name+".json")
        api.export_to_json(filename, self.document.doc)
    
    def openWorkSpace(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open document", os.path.join(self.source_dir, "tmp"), "JSON (*.json)")
        self.document.doc = api.open_from_file(filename)
        self.document.updateView()
        self.document.changeDocument()
    
    def NewElementDialog(self):
        dlg = QDialog()
        dlg.setWindowTitle("New Element")
        dlg.setWindowIcon(self.icon)

        layout = QFormLayout()
        dlg.setLayout(layout)
        
        combo = QComboBox()
        for element in self.document.doc.childObjects:
            if element.type == "open":
                pass
            else:
                combo.addItem(element.osfed)
        layout.addRow(QLabel("Parent Element OSFED ID: "), combo)

        elementType = QComboBox()
        elementType.addItems(["closed", "open"])
        layout.addRow(QLabel("Type: "), elementType)

        elementName = QLineEdit()
        layout.addRow(QLabel("Element Name"), elementName)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.rejected.connect(dlg.reject)
        buttonBox.accepted.connect(dlg.accept)
        layout.addWidget(buttonBox)

        dlg.accepted.connect(lambda: self.add_new_element(combo.currentText(), elementName.text(), elementType.currentText()))

        dlg.exec_()
    
    def add_new_element(self, parent, name, type):
        element = api.El(name=name, type=type)
        p = self.document.doc.childObjects[int(parent)]
        p.addChild(element, self.document.doc)

        self.EditElementDialog(element.osfed)

    def EditElementDialog(self, index):
        element = self.document.doc.childObjects[int(index)]

        dlg = QDialog()
        dlg.setWindowTitle("Edit Element")
        dlg.setWindowIcon(self.icon)

        baseLayout = QVBoxLayout()
        dlg.setLayout(baseLayout)

        splitter = QSplitter()
        baseLayout.addWidget(splitter)

        pageList = QListWidget()
        splitter.addWidget(pageList)

        stack = QStackedWidget()
        splitter.addWidget(stack)

        #General Page
        pageList.addItem("General")
        general = QWidget()
        stack.addWidget(general)

        generalLayout = QFormLayout()
        general.setLayout(generalLayout)

        generalLayout.addRow(QLabel("OSFED ID:"), QLabel(index))

        name = QLineEdit()
        name.setText(element.name)
        generalLayout.addRow(QLabel("Name:"), name)

        innerHTML = QLineEdit()
        innerHTML.setText(element.innerHTML)
        generalLayout.addRow(QLabel("innerHTML:"), innerHTML)

        applyChanges = QPushButton(text="Apply Changes")
        applyChanges.clicked.connect(lambda: self.changeGeneralElement(index, name.text(), innerHTML.text()))
        generalLayout.addWidget(applyChanges)

        delete = QPushButton(text="Delete")
        delete.clicked.connect(lambda: self.deleteElement(index, dlg))
        generalLayout.addWidget(delete)
        #/General Page

        #Classes Page
        pageList.addItem("Classes")
        classesPage = QWidget()
        stack.addWidget(classesPage)

        classesLayout = QVBoxLayout()
        classesPage.setLayout(classesLayout)

        classes = QListWidget()
        classes.addItems(element.classes)
        classesLayout.addWidget(classes)

        addclass = QPushButton(text="Add a class")
        addclass.clicked.connect(lambda: self.AddAClassDialog(index, classes))
        classesLayout.addWidget(addclass)
        #/Classes Page

        pageList.currentRowChanged.connect(stack.setCurrentIndex)

        dlg.exec_()
    
    def deleteElement(self, index, dlg):
        self.document.doc.deleteChild(index)
        self.document.updateView()
        dlg.reject()
    
    def AddAClassDialog(self, index, classes):
        dlg = QDialog()
        dlg.setWindowTitle("Add A Class")
        dlg.setWindowIcon(self.icon)

        layout = QVBoxLayout()
        dlg.setLayout(layout)

        message = QLabel("Enter Class name:")
        layout.addWidget(message)

        lineEdit = QLineEdit()
        layout.addWidget(lineEdit)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.rejected.connect(dlg.reject)
        buttonBox.accepted.connect(dlg.accept)
        layout.addWidget(buttonBox)

        dlg.accepted.connect(lambda: self.add_class(lineEdit.text(), index, classes) )

        dlg.exec_()

    def add_class(self, class_name, index, classes):
        element = self.document.doc.childObjects[int(index)]
        element.classes.append(class_name)

        classes.clear()
        classes.addItems(element.classes)

        self.document.updateView()
    
    def changeGeneralElement(self, index, name, innerHTML):
        element = self.document.doc.childObjects[int(index)]
        element.name = name
        element.innerHTML = innerHTML

        self.document.updateView()
    
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
        self.document.doc = api.new_document(name) 
        self.document.changeDocument()
        with open(os.path.join(self.source_dir, "tmp/"+name+".html"), "w") as file:
            file.write(api.generateDocument(self.document.doc))

        self.browser.load(QUrl.fromLocalFile(os.path.join(self.source_dir, "tmp/"+name+".html")))
    
    def reloadView(self):
        with open(os.path.join(self.source_dir, "tmp/"+self.document.doc.name+".html"), "w") as file:
            file.write(api.generateDocument(self.document.doc))

        self.browser.load(QUrl.fromLocalFile(os.path.join(self.source_dir, "tmp/"+self.document.doc.name+".html")))
    
    def onDocumentChange(self):
        self.setWindowTitle("OSFED: "+self.document.doc.name)

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
