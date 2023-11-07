from PySide6.QtWidgets import *

class RestDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Rest?")
        self.setFixedSize(150,50)
        self.layout = QHBoxLayout()
        self.yes = QPushButton("Yes")
        self.no = QPushButton("No")
        self.layout.addWidget(self.yes)
        self.layout.addWidget(self.no)
        self.setLayout(self.layout)


