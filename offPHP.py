import os
import sys
import subprocess

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtWebEngineWidgets import *
from NewTextEdit import QTextEditWithLineNum

version = "1.2.0"
st=subprocess.STARTUPINFO
st.dwFlags=subprocess.STARTF_USESHOWWINDOW
st.wShowWindow=subprocess.SW_HIDE

class MainApp(QWidget):
    def __init__(self):
        # init something
        super().__init__()
        self.phpDir = os.path.dirname(os.path.realpath(__file__))
        self.phpDir = os.path.join(self.phpDir, "php")
        self.phps = {}
        if not os.path.exists(self.phpDir):
            QMessageBox.critical(self, "Please check the php directory",
                                 "Please check the php directory in the root folder of this")
            sys.exit(1)

        self.initUI()
        self.initEvents()
        self.init_phps()

        self.set_icon("op.ico")

    def initEvents(self):
        self.to_rest(QMessageBox.Yes)
        self.browser.setHtml("Runtime is PHP5.6.0|PHP7.1.6 \nMade by Freet Bash")
        self.reset.clicked.connect(self.on_reset)
        self.loadfie.clicked.connect(self.open_file)
        self.copy.clicked.connect(self.on_copy)
        self.run.clicked.connect(self.run_code)

    def initUI(self):
        self.setGeometry(300, 300, 1000, 600)
        self.setWindowTitle("offPHP v" + version)
        self.mainLayout = QVBoxLayout(self)
        self.topLayout = QHBoxLayout()

        self.phpVersion = QComboBox(self)
        # add in init_phps()
        self.topLayout.addWidget(self.phpVersion)

        self.reset = QPushButton("Reset")
        self.topLayout.addWidget(self.reset)

        self.run = QPushButton("Run")
        self.topLayout.addWidget(self.run)


        self.copy = QPushButton("Copy")
        self.topLayout.addWidget(self.copy)

        self.loadfie = QPushButton("Open File")
        self.topLayout.addWidget(self.loadfie)

        self.bottomLayout = QHBoxLayout()

        self.codeinput = QTextEditWithLineNum()
        self.codeinput.setLineWrapMode(QTextEdit.WidgetWidth)
        self.codeinput.setAcceptRichText(False)
        self.bottomLayout.addWidget(self.codeinput)

        self.browser = QWebEngineView()
        self.browser.setFixedHeight(self.size().height())
        self.browser.setFixedWidth(self.size().width()/2)

        self.bottomLayout.addWidget(self.browser)

        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.bottomLayout)

    def init_phps(self):
        phpdirname = os.listdir(self.phpDir)
        for dir in phpdirname:
            self.phps[dir] = os.path.join(self.phpDir,dir , "php.exe"),
        self.phpVersion.addItems(phpdirname)


    def on_reset(self):
        res = QMessageBox.question(self, "Reset", "Do you want to reset?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        self.to_rest(res == QMessageBox.Yes)


    def to_rest(self, state):
        if state:
            self.codeinput.setPlainText('<?php \necho "hello word";')
            self.browser.setHtml("Runtime is PHP5.6.0|PHP7.1.6 \nMade by Freet Bash")

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Code Files (*.*)")
        if filename:
            with open(filename, "r") as f:
                self.codeinput.setPlainText(f.read())

    def on_copy(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.codeinput.toPlainText())

    def run_code(self):
        # generate temp file
        temp_php = os.path.join(os.path.dirname(os.path.realpath(__file__)), "temp.php")
        with open(temp_php, "w") as f:
            f.write(self.codeinput.toPlainText())

        # choose the php version

        try:
            # get the php path
            php = self.phps[self.phpVersion.currentText()][0]

            # handle the php code

            process = subprocess.Popen([php, "-f", temp_php], stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=st)
            stdout, stderr = process.communicate()
            content = stdout.decode("gbk")
            if stderr:
                content += "\nSTDERR: " + stderr.decode("gbk")
            self.browser.setHtml(content)

        except KeyError:
            QMessageBox.warning(self, "Warning", "PHP version not found. View the github to get more information.", QMessageBox.Ok)


    def set_icon(self,filename):
        icon = QIcon(filename)
        self.setWindowIcon(icon)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainApp()
    w.show()
    sys.exit(app.exec_())



