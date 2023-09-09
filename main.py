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

# https://github.com/davidsandberg/facenet/wiki

# import tensorflow as tf
# import cv2
# import numpy as np
#
# # Carregue o modelo FaceNet pré-treinado
# model_path = 'caminho/para/o/modelo/FaceNet'
# model = tf.keras.models.load_model(model_path)
#
# # Função para pré-processamento de imagens
# def preprocess_image(image_path):
#     img = cv2.imread(image_path)
#     img = cv2.resize(img, (160, 160))
#     img = img.astype(np.float32)
#     img = (img - 127.5) / 128.0  # Normalização
#     return img
#
# # Função para gerar embeddings faciais
# def get_face_embeddings(image_path):
#     img = preprocess_image(image_path)
#     img = np.expand_dims(img, axis=0)  # Adicionar dimensão de lote
#     embeddings = model.predict(img)
#     return embeddings
#
# # Exemplo de uso
# image_path_1 = 'caminho/para/primeira/imagem.jpg'
# image_path_2 = 'caminho/para/segunda/imagem.jpg'
#
# embeddings_1 = get_face_embeddings(image_path_1)
# embeddings_2 = get_face_embeddings(image_path_2)
#
# # Calcule a distância euclidiana entre os embeddings para comparar as faces
# distance = np.linalg.norm(embeddings_1 - embeddings_2)
#
# # Defina um limite para determinar se as faces são da mesma pessoa
# limite = 1.0  # Ajuste conforme necessário
#
# if distance < limite:
#     print("As faces pertencem à mesma pessoa.")
# else:
#     print("As faces pertencem a pessoas diferentes.")
