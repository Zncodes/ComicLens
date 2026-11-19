
import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QWidget,
    QVBoxLayout,
)

class ComicLensApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ComicLens Translator")
        self.resize(1000, 650)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        title = QLabel("ComicLens Translator")
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
        """)

        subtitle = QLabel(
            "Real-time Multilingual Comic Translator"
        )

        status = QLabel("Application is ready!")

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addStretch()
        layout.addWidget(status)

        self.setCentralWidget(central_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = ComicLensApp()
    window.show()

    sys.exit(app.exec())
