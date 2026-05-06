import sys

from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class MW(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.show()

    def init_ui(self):
        self.setWindowTitle("Sent Close Event Ex")
        self.resize(420, 220)

        self.label = QLabel(
            "Close Window button을 누르면 self.close()가 호출됨.\n"
            "self.close()는 QCloseEvent를 발생시키고,\n"
            "closeEvent(self, event)가 즉시 호출됨."
        )

        self.unsaved_checkbox = QCheckBox(
            "Unsaved changes가 있다고 가정"
        )
        self.unsaved_checkbox.setChecked(True)

        self.close_button = QPushButton("Close Window")
        self.close_button.clicked.connect(self.request_close)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.unsaved_checkbox)
        layout.addWidget(self.close_button)
        self.setLayout(layout)

    def request_close(self):
        """
        Sent Event 흐름을 보여주는 method.

        close()를 호출하면 QWidget은 QCloseEvent를 생성하여
        현재 widget의 closeEvent()로 즉시 전달함.
        queue를 거치지 않고 호출 흐름 안에서 바로 처리됨.
        """

        print("[1] before self.close()")
        closed = self.close()
        print("[3] after self.close()")
        print(f"[4] close result: {closed}")

    def closeEvent(self, event: QCloseEvent):
        """
        window가 닫히려 할 때 호출되는 Event Handler.

        사용자가 title bar의 X button을 눌러도 호출되고,
        code에서 self.close()를 호출해도 호출됨.
        """

        print("[2] closeEvent() called")

        if self.unsaved_checkbox.isChecked():
            reply = QMessageBox.question(
                self,
                "Confirm Close",
                "저장하지 않은 변경 사항이 있음.\n"
                "정말 닫겠는가?",
                QMessageBox.StandardButton.Yes
                | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )

            if reply == QMessageBox.StandardButton.Yes:
                print("close accepted")
                event.accept()
            else:
                print("close ignored")
                event.ignore()

            return

        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MW()
    sys.exit(app.exec())