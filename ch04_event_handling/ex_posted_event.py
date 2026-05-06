# ============================================
# Posted Paint Event Example
# ============================================
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import (
    QApplication,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class Canvas(QWidget):
    def __init__(self):
        super().__init__()

        self.circle_x = 50
        self.circle_y = 60
        self.radius = 20

        # QWidget이 그림을 그릴 영역을 가지도록 최소 크기 지정.
        self.setMinimumSize(320, 180)

    def move_circle(self):
        """
        원의 위치를 변경한 뒤 update()를 호출함.

        update()는 paintEvent()를 즉시 호출하지 않음.
        repaint request를 event queue에 등록하고,
        Event Loop가 나중에 paintEvent()를 호출하게 함.
        """

        # 1. 원의 x좌표를 이동시킴.
        self.circle_x += 20

        if self.circle_x > 280:
            self.circle_x = 50

        # 2. repaint request를 등록함.
        print("[1] before update()")
        self.update()
        print("[2] after update()")
        print("[3] paintEvent() has not necessarily been called yet")

    def paintEvent(self, event):
        """
        widget을 다시 그려야 할 때 Qt가 호출하는 Event Handler.

        update()에 의해 등록된 repaint request가
        Event Loop에서 처리되면 이 method가 호출됨.
        """

        print("[4] paintEvent() called")

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.drawText(
            10,
            20,
            "Click the button. update() schedules paintEvent().",
        )

        painter.drawEllipse(
            self.circle_x - self.radius,
            self.circle_y - self.radius,
            self.radius * 2,
            self.radius * 2,
        )
        super().paintEvent(event)


class MW(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.show()

    def init_ui(self):
        self.setWindowTitle("Posted Paint Event Ex")
        self.resize(380, 260)

        self.canvas = Canvas()
        self.button = QPushButton("Move Circle")

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)

        self.button.clicked.connect(self.canvas.move_circle)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MW()
    sys.exit(app.exec())