import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QPushButton, QFileDialog, QMessageBox,
                             QGridLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import (QIcon, QPixmap)


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

    def createImageLabelAndButtonsLinkedWithActions(self):
        image_label = QLabel(self)
        image_label.setFixedSize(200, 200)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        botao_abrir = self.createButtonWithIcon('images/open_file.png',
                                                     'Clique neste botão para escolher uma imagem')
        botao_abrir.clicked.connect(lambda: self.openImage(image_label))

        botao_limpar = self.createButtonWithIcon('images/clear.png',
                                                      'Clique neste botão para limpar a imagem')
        botao_limpar.clicked.connect(lambda: self.clearImage(image_label))
        return image_label, botao_abrir, botao_limpar

    def setUpMainWindow(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QGridLayout()
        for i in range(0, 6, 2):
            image_label, botao_abrir, botao_limpar = self.createImageLabelAndButtonsLinkedWithActions()
            layout.addWidget(image_label, 0, i, 1, 2)
            layout.addWidget(botao_abrir, 1, i)
            layout.addWidget(botao_limpar, 1, i+1)
        central_widget.setLayout(layout)

    def openImage(self, i_label):
        image_file, _ = QFileDialog.getOpenFileName(self, "Open Image", "",
                                                    "JPG Files (*.jpeg *.jpg );;PNG Files (*.png);;"
                                                    "Bitmap Files (*.bmp);;GIF Files (*.gif)")
        image = QPixmap(image_file)

        if not image.isNull():
            i_label.setPixmap(image.scaled(i_label.size(), Qt.AspectRatioMode.KeepAspectRatio,
                                           Qt.TransformationMode.SmoothTransformation))
            i_label.update()
        else:
            QMessageBox.information(self, "No Image", "No Image Selected.", QMessageBox.StandardButton.Ok)

    def clearImage(self, i_label):
        i_label.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setAttribute(
        Qt.ApplicationAttribute.AA_DontShowIconsInMenus, True)
    window = MainWindow()
    sys.exit(app.exec())
