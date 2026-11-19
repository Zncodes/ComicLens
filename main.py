
import sys
import os

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QTextEdit,
    QComboBox,
    QMessageBox,
    QSplitter,
    QFrame,
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from src.ocr.engine import OCREngine


class ImagePreview(QLabel):

    def __init__(self):
        super().__init__()

        self.original_pixmap = None

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setText("Open a comic image to get started")
        self.setMinimumSize(300, 300)

        self.setStyleSheet("""
            QLabel {
                background-color: #252525;
                border: 1px solid #444444;
                border-radius: 8px;
                color: #aaaaaa;
                font-size: 14px;
            }
        """)

    def set_image(self, image_path):

        pixmap = QPixmap(image_path)

        if pixmap.isNull():
            raise ValueError("Unable to load image.")

        self.original_pixmap = pixmap
        self.update_preview()

    def update_preview(self):

        if self.original_pixmap is None:
            return

        scaled = self.original_pixmap.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        self.setPixmap(scaled)

    def resizeEvent(self, event):

        super().resizeEvent(event)
        self.update_preview()


class ComicLensApp(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("ComicLens Translator")
        self.resize(1200, 750)

        self.image_path = None

        self.ocr_engine = OCREngine()

        self.setup_ui()

    def setup_ui(self):

        central = QWidget()
        main_layout = QVBoxLayout(central)

        # Header
        title = QLabel("ComicLens Translator")
        title.setStyleSheet("""
            font-size: 26px;
            font-weight: bold;
            color: white;
        """)

        subtitle = QLabel(
            "Multilingual Comic OCR and Translator"
        )

        # Toolbar
        toolbar = QHBoxLayout()

        self.open_button = QPushButton("Open Comic")
        self.open_button.clicked.connect(
            self.open_image
        )

        self.ocr_button = QPushButton("Extract Text")
        self.ocr_button.clicked.connect(
            self.run_ocr
        )
        self.ocr_button.setEnabled(False)

        self.language_selector = QComboBox()

        for name, code in (
            OCREngine.SUPPORTED_LANGUAGES.items()
        ):
            self.language_selector.addItem(name, code)

        self.language_selector.setCurrentIndex(1)

        toolbar.addWidget(self.open_button)
        toolbar.addWidget(self.ocr_button)
        toolbar.addWidget(QLabel("OCR Language:"))
        toolbar.addWidget(self.language_selector)
        toolbar.addStretch()

        # Image viewer
        self.image_viewer = ImagePreview()

        # OCR result
        result_title = QLabel("OCR Result")

        self.result_text = QTextEdit()
        self.result_text.setPlaceholderText(
            "Extracted comic text will appear here..."
        )

        self.result_text.setStyleSheet("""
            QTextEdit {
                background-color: #252525;
                color: white;
                border: 1px solid #444444;
                border-radius: 6px;
                font-size: 14px;
                padding: 8px;
            }
        """)

        # Splitter
        splitter = QSplitter(
            Qt.Orientation.Horizontal
        )

        image_container = QWidget()
        image_layout = QVBoxLayout(image_container)
        image_layout.addWidget(self.image_viewer)

        result_container = QWidget()
        result_layout = QVBoxLayout(result_container)
        result_layout.addWidget(result_title)
        result_layout.addWidget(self.result_text)

        splitter.addWidget(image_container)
        splitter.addWidget(result_container)

        splitter.setSizes([650, 450])

        # Status
        self.status_label = QLabel(
            "Application ready."
        )

        self.status_label.setStyleSheet(
            "color: #aaaaaa; padding: 5px;"
        )

        # Main layout
        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)
        main_layout.addLayout(toolbar)
        main_layout.addWidget(splitter, 1)
        main_layout.addWidget(self.status_label)

        self.setCentralWidget(central)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
                color: white;
            }

            QLabel {
                color: white;
            }

            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                padding: 9px 15px;
                border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #2563eb;
            }

            QPushButton:disabled {
                background-color: #555555;
            }

            QComboBox {
                background-color: #303030;
                color: white;
                padding: 7px;
                border: 1px solid #555555;
                border-radius: 5px;
            }
        """)

    def open_image(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Comic Image",
            "",
            "Images (*.png *.jpg *.jpeg *.webp *.bmp)"
        )

        if not file_path:
            return

        try:
            self.image_viewer.set_image(file_path)

            self.image_path = file_path

            self.ocr_button.setEnabled(True)

            self.result_text.clear()

            self.status_label.setText(
                f"Loaded: {os.path.basename(file_path)}"
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Image Error",
                str(error)
            )

    def run_ocr(self):

        if not self.image_path:
            return

        language = self.language_selector.currentData()

        self.status_label.setText(
            "Extracting text... Please wait."
        )

        QApplication.processEvents()

        try:

            extracted_text = (
                self.ocr_engine.extract_text(
                    self.image_path,
                    language
                )
            )

            if extracted_text:
                self.result_text.setPlainText(
                    extracted_text
                )

                self.status_label.setText(
                    "OCR completed successfully."
                )

            else:
                self.result_text.setPlainText(
                    "No text detected in this image."
                )

                self.status_label.setText(
                    "OCR completed. No text found."
                )

        except Exception as error:

            QMessageBox.critical(
                self,
                "OCR Error",
                str(error)
            )

            self.status_label.setText(
                "OCR failed."
            )


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = ComicLensApp()
    window.show()

    sys.exit(app.exec())
