# ============================================
# Spontaneous Event Example
# ============================================
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, 
    QLabel, 
    QMainWindow,
)


class MW(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.show()

    def init_ui(self):
        self.setGeometry(100, 100, 360, 200)
        self.setWindowTitle("Spontaneous Event Ex")

        label = QLabel(
            """
            <p>
                Press the <b>ESC</b> key
                to quit this program.
            </p>
            """
        )

        self.setCentralWidget(label)

    def keyPressEvent(self, event):
        """
        key press event를 처리하는 Event Handler.

        사용자가 실제 keyboard key를 누르면,
        OS / window system에서 native key event가 발생하고,
        Qt는 이를 QKeyEvent로 변환하여 이 method로 전달함.
        """

        if event.key() == Qt.Key.Key_Escape:
            print("ESC key pressed by real keyboard input.")
            self.close()
            return

        # ESC 이외의 key event는 parent class의 기본 처리에 위임.
        super().keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MW()
    sys.exit(app.exec())