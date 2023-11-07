import os
import subprocess

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from NewTextEdit import QTextEditWithLineNum
import sys


class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initEvents()
        self.phpDir = os.path.dirname(os.path.realpath(__file__))
        self.phpDir = os.path.join(self.phpDir, "php")
        self.php = os.path.join(self.phpDir, "php7.1","")
        self.phps = {
            "PHP5.6.0": os.path.join(self.phpDir, "php5.6.0", "php.exe"),
            "PHP7.1.6": os.path.join(self.phpDir, "php7.1.6", "php.exe"),
        }
    def initEvents(self):
        self.to_rest(QMessageBox.Yes)
        self.output.setPlaceholderText("Runtime is PHP5.6.0|PHP7.1.6")
        self.input.setPlaceholderText("Input arguments here")
        self.reset.clicked.connect(self.on_reset)
        self.loadfie.clicked.connect(self.open_file)
        self.copy.clicked.connect(self.on_copy)
        self.run.clicked.connect(self.run_code)

    def initUI(self):
        self.setGeometry(300, 300, 1000, 600)
        self.setWindowTitle("offPHP")
        self.mainLayout = QVBoxLayout(self)
        self.topLayout = QHBoxLayout()

        self.phpVersion = QComboBox(self)
        self.phpVersion.addItems(["PHP5.6.0", "PHP7.1.6"])
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
        self.bottomLayout.addWidget(self.codeinput)

        self.rightLayout = QVBoxLayout()
        self.input = QTextEditWithLineNum()
        self.input.setFixedHeight(200)
        self.rightLayout.addWidget(self.input)

        self.output = QTextEditWithLineNum()
        self.output.setFont(QFont("Consolas", 8))
        self.output.setReadOnly(True)
        self.rightLayout.addWidget(self.output)

        self.bottomLayout.addLayout(self.rightLayout)
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.bottomLayout)

    def on_reset(self):
        res = QMessageBox.question(self, "Reset", "Do you want to reset?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        self.to_rest(res == QMessageBox.Yes)


    def to_rest(self, state):
        if state:
            self.codeinput.setPlainText('<?php \necho"hello word";')
            self.output.clear()

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
        php = ""
        if self.phpVersion.currentText() == "PHP5.6.0":
            php = self.phps["PHP5.6.0"]
        elif self.phpVersion.currentText() == "PHP7.1.6":
            php = self.phps["PHP7.1.6"]

        # handle the php code
        input_data = self.input.toPlainText()
        process = subprocess.Popen([php, "-f", temp_php], stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(input=input_data.encode("utf-8"))
        content = stdout.decode("utf-8")
        if stderr:
            content += "\nSTDERR: " + stderr.decode("utf-8")

        self.output.setPlainText(content)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainApp()
    w.show()
    sys.exit(app.exec_())



