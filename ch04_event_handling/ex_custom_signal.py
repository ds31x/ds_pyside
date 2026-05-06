# ==================================================================
# 4.3 커스텀 시그널과 슬롯


import sys, os

# PySide6 우선, PyQt6는 백업용
qt_binding = None
try:
    from PySide6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout
    )
    from PySide6.QtGui import QPixmap, QKeyEvent
    from PySide6.QtCore import Qt, Signal, QObject, QSize
    qt_binding = 'PySide6'
except ImportError:
    try:
        from PyQt6.QtWidgets import (
            QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout
        )
        from PyQt6.QtGui import QPixmap, QKeyEvent
        from PyQt6.QtCore import Qt, pyqtSignal, QObject, QSize
        Signal = pyqtSignal  # PyQt6에서는 pyqtSignal을 Signal로 대응
        qt_binding = 'PyQt6'
    except ImportError:
        print("Neither PySide6 nor PyQt6 is installed.")
        sys.exit(1)

print(f"Using {qt_binding} binding.")

# class DsSignal(QObject):
#    """Define a signal, change_pixmap, that takes int argument."""
#    if qt_binding == 'PySide6':
#        change_pixmap = Signal(int)
#    else:   
#        change_pixmap = pyqtSignal(int)
#

class MW(QMainWindow):
    """
    메인 윈도우 클래스. 
    QMainWindow는 QObject를 상속하므로
    Qt의 signal/slot 시스템을 사용할 수 있음.
    """

    # Signal은 반드시 class variable로 선언해야 함!
    # 이유: Qt의 메타클래스(QMetaObject)가 클래스 정의 시 Signal을 인식하고
    #    내부적으로 C++ 신호 슬롯 시스템과 연결함.
    #    만약 __init__ 안에서 self.signal = Signal(...)처럼 instance variable로 정의하면
    #    메타클래스가 이를 감지할 수 없어 동작하지 않음.
    if qt_binding == "PySide6":
        change_pixmap = Signal(int)
    else:
        change_pixmap = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """UI 구성 및 창 설정"""
        self.fstr = os.path.dirname(os.path.abspath(__file__))
        self.setGeometry(100, 100, 200, 300)
        self.setWindowTitle("Custom Signals Example")
        self.setup_main_wnd()
        self.show()

    def setup_main_wnd(self):
        """메인 위젯 및 레이아웃 구성"""
        self.idx = 0

        # # create instance of DsSignal class
        # self.signal = DsSignal()
        # self.signal.change_pixmap.connect(self.change_pixmap_handler)

        # 커스텀 시그널을 슬롯 함수에 연결
        self.change_pixmap.connect(self.change_pixmap_handler)

        lm = QVBoxLayout()

        info_label = QLabel("<p>Press <b>+</b> or <b>-</b> to <i>change image</i></p>")
        info_label.setTextFormat(Qt.TextFormat.RichText)  # HTML 태그가 적용되도록 명시
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lm.addWidget(info_label)

        self.img_label = QLabel()

        img_path = os.path.join(self.fstr, "img", "0.png")
        pixmap = QPixmap(img_path)
        if pixmap.isNull():
            print(f"이미지 로딩 실패: {img_path}")
        self.img_label.setPixmap(pixmap.scaled(
            QSize(180, 250),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        ))
        self.img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lm.addWidget(self.img_label)

        container = QWidget()
        container.setLayout(lm)
        self.setCentralWidget(container)

    def keyPressEvent(self, event: QKeyEvent):
        """
        키 이벤트 핸들러
        - + 또는 - 키 입력 시 이미지 인덱스 변경을 위한 시그널을 발생시킴
        - [중요] super().keyPressEvent(event)는 반드시 호출해야 함:
          → 이유: 이 호출을 생략하면 하위 위젯(QLineEdit 등)의 키 입력 기능,
             메뉴 단축키, 포커스 이동 등의 Qt 기본 이벤트 전달 흐름이 중단됨
        - [참고] return 문은 필요하지 않음:
          → keyPressEvent()는 반환값이 없는 void 타입 함수 (return None)
        """
        if event.key() == Qt.Key.Key_Plus:
            self.change_pixmap.emit(1)
        elif event.key() == Qt.Key.Key_Minus:
            self.change_pixmap.emit(-1)

        super().keyPressEvent(event)

    def change_pixmap_handler(self, offset: int):
        """
        이미지 인덱스를 변경하여 새 이미지로 갱신
        - Python의 % 연산은 음수 대응이 자동이므로 추가 조건 필요 없음
        - 이미지 로딩 실패 시 콘솔에 경고 출력
        """
        self.idx = (self.idx + offset) % 10

        img_path = os.path.join(self.fstr, "img", f"{self.idx}.png")
        pixmap = QPixmap(img_path)
        if pixmap.isNull():
            print(f"이미지 로딩 실패: {img_path}")
        self.img_label.setPixmap(pixmap.scaled(
            QSize(180, 250),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        ))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MW()
    sys.exit(app.exec())
