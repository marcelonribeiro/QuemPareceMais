import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QPushButton, QFileDialog, QMessageBox,
                             QGridLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import (QIcon, QPixmap)
import cv2
import numpy as np
import tensorflow as tf


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


def preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (160, 160))
    img = img.astype(np.float32)
    img = (img - 127.5) / 128.0  # Normalização)
    return np.expand_dims(img, axis=0)


if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # app.setAttribute(
    #     Qt.ApplicationAttribute.AA_DontShowIconsInMenus, True)
    # window = MainWindow()
    # sys.exit(app.exec())

    tf.compat.v1.disable_v2_behavior()

    with tf.compat.v1.gfile.FastGFile("model/20180402-114759.pb", 'rb') as f:
        graph_def = tf.compat.v1.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')

    with tf.compat.v1.Session(graph=tf.compat.v1.get_default_graph()) as sess:
        images_placeholder = sess.graph.get_tensor_by_name("input:0")
        embeddings = sess.graph.get_tensor_by_name("embeddings:0")
        phase_train_placeholder = sess.graph.get_tensor_by_name("phase_train:0")
        resultado = sess.run(embeddings, feed_dict={images_placeholder: preprocess_image("images/allyne.jpg"),
                                                    phase_train_placeholder: False})
        print("Embeddings: ", resultado)

# # Calcule a distância euclidiana entre os embeddings para comparar as faces
# distance = np.linalg.norm(embeddings_1 - embeddings_2)
