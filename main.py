import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow,
                             QWidget, QLabel, QPushButton, QDockWidget, QDialog,
                             QFileDialog, QMessageBox, QToolBar, QStatusBar,
                             QVBoxLayout)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import (QIcon, QAction, QPixmap)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        """Set up the application's GUI."""
        self.setFixedSize(650, 650)
        self.setWindowTitle("Quem Parece Mais?")

        self.setUpMainWindow()
        self.createActions()
        # self.createToolBar()
        self.show()

    def setUpMainWindow(self):
        """Create and arrange widgets in the main window."""

        self.botao_abrir = QPushButton("Abrir Imagem", self)
        self.botao_abrir.clicked.connect(self.openImage)

        self.image = QPixmap()

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.botao_abrir)
        self.layout.addWidget(self.image_label)
        self.setLayout(self.layout)

        # Create the status bar
        self.setStatusBar(QStatusBar())

    def createActions(self):
        """Create the application's menu actions."""
        # Create actions for File menu
        self.open_act = QAction(QIcon("images/open_file.png"), "Open")
        self.open_act.setStatusTip("Open a new image")
        self.open_act.triggered.connect(self.openImage)

        self.quit_act = QAction(QIcon("images/exit.png"), "Quit")
        self.quit_act.setShortcut("Ctrl+Q")
        self.quit_act.setStatusTip("Quit program")
        self.quit_act.triggered.connect(self.close)

        self.clear_act = QAction(QIcon("images/clear.png"), "Clear Image")
        self.clear_act.setStatusTip("Clear the current image")
        self.clear_act.triggered.connect(self.clearImage)

    def createToolBar(self):
        """Create the application's toolbar."""
        tool_bar = QToolBar("Photo Editor Toolbar")
        tool_bar.setIconSize(QSize(24, 24))
        self.addToolBar(tool_bar)

        # Add actions to the toolbar
        tool_bar.addAction(self.open_act)
        tool_bar.addAction(self.clear_act)
        tool_bar.addSeparator()
        tool_bar.addAction(self.quit_act)

    def openImage(self):
        """Open an image file and display its contents on the
        QLabel widget."""
        image_file, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "",
            "JPG Files (*.jpeg *.jpg );;PNG Files (*.png);;\
                Bitmap Files (*.bmp);;GIF Files (*.gif)")

        if image_file:
            self.image = QPixmap(image_file)

            self.image_label.setPixmap(self.image.scaled(self.image_label.size(),
                                                         Qt.AspectRatioMode.KeepAspectRatio,
                                                         Qt.TransformationMode.SmoothTransformation))
        else:
            QMessageBox.information(self, "No Image",
                                    "No Image Selected.", QMessageBox.StandardButton.Ok)

    def clearImage(self):
        """Clears current image in the QLabel widget."""
        self.image_label.clear()
        self.image = QPixmap()  # Reset pixmap so that isNull() = True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setAttribute(
        Qt.ApplicationAttribute.AA_DontShowIconsInMenus, True)
    window = MainWindow()
    sys.exit(app.exec())
