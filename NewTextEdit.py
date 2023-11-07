#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import sys

from PySide6.QtCore import Qt, QRect, QSize, QPoint
from PySide6.QtGui import QPainter, QFont
from PySide6.QtWidgets import QTextEdit, QApplication
from PySide6.QtWidgets import QWidget


class QTextEditWithLineNum(QTextEdit):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(QFont("Consolas", 12))
        self.setLineWrapMode(QTextEdit.NoWrap)  # 不自动换行
        self.lineNumberArea = LineNumPaint(self)
        self.document().blockCountChanged.connect(self.update_line_num_width)
        self.verticalScrollBar().valueChanged.connect(self.lineNumberArea.update)
        self.textChanged.connect(self.lineNumberArea.update)
        self.cursorPositionChanged.connect(self.lineNumberArea.update)
        self.update_line_num_width()

    def lineNumberAreaWidth(self):
        block_count = self.document().blockCount()
        max_value = max(1, block_count)
        d_count = len(str(max_value))
        _width = self.fontMetrics().horizontalAdvance('9') * d_count + 5
        return _width

    def update_line_num_width(self):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), Qt.lightGray)
        # 获取首个可见文本块
        first_visible_block_number = self.cursorForPosition(QPoint(0, 1)).blockNumber()
        # 从首个文本块开始处理
        blockNumber = first_visible_block_number
        block = self.document().findBlockByNumber(blockNumber)
        top = self.viewport().geometry().top()
        if blockNumber == 0:
            additional_margin = int(self.document().documentMargin() - 1 - self.verticalScrollBar().sliderPosition())
        else:
            prev_block = self.document().findBlockByNumber(blockNumber - 1)
            additional_margin = int(self.document().documentLayout().blockBoundingRect(
                prev_block).bottom()) - self.verticalScrollBar().sliderPosition()
        top += additional_margin
        bottom = top + int(self.document().documentLayout().blockBoundingRect(block).height())
        last_block_number = self.cursorForPosition(QPoint(0, self.height() - 1)).blockNumber()
        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()) and blockNumber <= last_block_number:
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                painter.setPen(Qt.black)
                painter.drawText(0, top, self.lineNumberArea.width(), height, Qt.AlignCenter, number)
            block = block.next()
            top = bottom
            bottom = top + int(self.document().documentLayout().blockBoundingRect(block).height())
            blockNumber += 1


class LineNumPaint(QWidget):
    def __init__(self, q_edit):
        super().__init__(q_edit)
        self.q_edit_line_num = q_edit

    def sizeHint(self):
        return QSize(self.q_edit_line_num.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.q_edit_line_num.lineNumberAreaPaintEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    codeEditor = QTextEditWithLineNum()
    codeEditor.setGeometry(100, 100, 800, 600)
    codeEditor.show()
    sys.exit(app.exec_())

