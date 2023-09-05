import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow,
                             QWidget, QLabel, QPushButton, QDockWidget, QDialog,
                             QFileDialog, QMessageBox, QToolBar, QStatusBar,
                             QVBoxLayout, QGridLayout)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import (QIcon, QAction, QPixmap)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        """Set up the application's GUI."""
        self.setMinimumSize(650, 200)
        self.setWindowTitle("Quem Parece Mais?")

        self.setUpMainWindow()
        self.show()

    def createButtonWithIcon(self, image_icon_path, tooltip):
        botao = QPushButton(self)
        icon = QIcon(image_icon_path)
        botao.setIcon(icon)
        botao.setIconSize(icon.actualSize(botao.size()))
        botao.setToolTip(tooltip)
        botao.setGeometry(50, 50, 100, 100)
        return botao

    def setUpMainWindow(self):
        """Create and arrange widgets in the main window."""

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.image_label = QLabel()
        self.image_label.setFixedSize(200, 200)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.botao_abrir = self.createButtonWithIcon('images/open_file.png',
                                                     'Clique neste botão para escolher uma imagem')
        self.botao_abrir.clicked.connect(lambda: self.openImage(self.image_label))

        self.botao_limpar = self.createButtonWithIcon('images/clear.png',
                                                      'Clique neste botão para limpar a imagem')
        self.botao_limpar.clicked.connect(lambda: self.clearImage(self.image_label))

        layout = QGridLayout()
        layout.addWidget(self.image_label, 0, 0, 1, 2)
        layout.addWidget(self.botao_abrir, 1, 0)
        layout.addWidget(self.botao_limpar, 1, 1)
        central_widget.setLayout(layout)

    def openImage(self, i_label):
        """Open an image file and display its contents on the
        QLabel widget."""
        image_file, _ = QFileDialog.getOpenFileName(self, "Open Image", "",
                                                    "JPG Files (*.jpeg *.jpg );;PNG Files (*.png);;"
                                                    "Bitmap Files (*.bmp);;GIF Files (*.gif)")
        image = QPixmap(image_file)

        if not image.isNull():
            i_label.setPixmap(image.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio,
                                                    Qt.TransformationMode.SmoothTransformation))
            i_label.update()
        else:
            QMessageBox.information(self, "No Image", "No Image Selected.", QMessageBox.StandardButton.Ok)

    def clearImage(self, i_label):
        """Clears current image in the QLabel widget."""
        i_label.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setAttribute(
        Qt.ApplicationAttribute.AA_DontShowIconsInMenus, True)
    window = MainWindow()
    sys.exit(app.exec())
