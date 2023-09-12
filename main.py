import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QPushButton, QFileDialog, QMessageBox,
                             QGridLayout, QTextEdit, QVBoxLayout, QTextBrowser, QDialog)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import (QIcon, QPixmap, QAction)
import cv2
import numpy as np
import tensorflow as tf


def get_grafo_modelo_gerador_embeddings():
    tf.compat.v1.disable_v2_behavior()

    with tf.compat.v1.gfile.FastGFile("model/20180402-114759.pb", 'rb') as f:
        graph_def = tf.compat.v1.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')

    return tf.compat.v1.get_default_graph()


PESSOA_1 = 0
PESSOA_ALVO = 2
PESSOA_2 = 4
GRAPH = get_grafo_modelo_gerador_embeddings()


class Worker(QThread):
    update_text_edit_signal = pyqtSignal(str)

    def __init__(self, dict_pessoa_to_image_label_and_path):
        super().__init__()
        self.dict_pessoa_to_image_label_and_path = dict_pessoa_to_image_label_and_path

    def get_embeddings_images(self):
        if any(p.image_path == '' for p in self.dict_pessoa_to_image_label_and_path.values()):
            raise Exception('Alguma imagem não foi apontada.')
        embeddings = {}
        for pessoa in self.dict_pessoa_to_image_label_and_path:
            emb = get_embedding_by_graph_and_img_path(GRAPH,
                                                      self.dict_pessoa_to_image_label_and_path[pessoa].image_path)
            embeddings[pessoa] = emb
        return embeddings

    def run(self):
        """The thread begins running from here.
        run() is only called after start()."""

        embeddings = self.get_embeddings_images()
        distance_pessoa_1 = np.linalg.norm(embeddings[PESSOA_1] - embeddings[PESSOA_ALVO])
        distance_pessoa_2 = np.linalg.norm(embeddings[PESSOA_2] - embeddings[PESSOA_ALVO])
        pre_texto = f"Pessoa 1 com distância {distance_pessoa_1} e Pessoa 2 com distância {distance_pessoa_2}"

        pos_texto = "Pessoa 2 parece mais com a Pessoa Alvo"
        if distance_pessoa_1 < distance_pessoa_2:
            pos_texto = "Pessoa 1 parece mais com a Pessoa Alvo"

        self.update_text_edit_signal.emit(f'{pre_texto}. {pos_texto}.')


class ImageLabelAndPath():

    def __init__(self, image_label, image_path):
        self.image_label = image_label
        self.image_path = image_path

    def __str__(self):
        return self.image_path


class SobreDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setModal(True)

        self.setWindowTitle("Sobre o Programa")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()
        text_browser = QTextBrowser()
        text_browser.setOpenExternalLinks(True)

        # Aqui você pode adicionar informações sobre o programa.
        about_text = """
        <h2>Quem Parece Mais?</h2>
        <p>Versão: 1.0</p>
        <p>Autor: Marcelo Nunes Ribeiro</p>
        <p>Descrição: Este é um programa para saber quem, de duas pessoas, parece mais com a Pessoa Alvo.</p>
        """

        text_browser.setHtml(about_text)
        layout.addWidget(text_browser)
        self.setLayout(layout)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.dict_pessoa_to_image_label_and_path = {}
        self.initializeUI()

    def initializeUI(self):
        """Set up the application's GUI."""
        self.setMinimumSize(650, 200)
        self.setWindowTitle("Quem Parece Mais?")
        self.createMenu()
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

    def createMenu(self):
        """Create the application's menu bar."""

        self.menuBar().setNativeMenuBar(False)

        self.sobre_action = QAction("Sobre", self)
        self.sobre_action.triggered.connect(self.mostrar_sobre_dialog)

        self.quit_act = QAction("Fechar")
        self.quit_act.setShortcut("Ctrl+Q")
        self.quit_act.setStatusTip("Fecha o programa")
        self.quit_act.triggered.connect(self.close)

        # Create File menu and add actions
        file_menu = self.menuBar().addMenu("Arquivo")
        file_menu.addAction(self.quit_act)

        help_menu = self.menuBar().addMenu("Ajuda")
        help_menu.addAction(self.sobre_action)


    def createImageLabelAndButtonsLinkedWithActions(self, img_label_and_path):

        botao_abrir = self.createButtonWithIcon('images/open_file.png',
                                                     'Clique neste botão para escolher uma imagem')
        botao_abrir.clicked.connect(lambda: self.openImage(img_label_and_path))

        botao_limpar = self.createButtonWithIcon('images/clear.png',
                                                      'Clique neste botão para limpar a imagem')
        botao_limpar.clicked.connect(lambda: self.clearImage(img_label_and_path))
        return img_label_and_path.image_label, botao_abrir, botao_limpar

    def createTituloImagem(self, texto):
        titulo_label = QLabel(self)
        titulo_label.setText(texto)
        titulo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return titulo_label

    def setUpMainWindow(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # inserir botões e exibição das imagens em um layout
        layout = QGridLayout()

        for i in range(0, 6, 2):
            image_label = QLabel(self)
            image_label.setFixedSize(200, 200)
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            img_label_and_path = ImageLabelAndPath(image_label, '')
            self.dict_pessoa_to_image_label_and_path[i] = img_label_and_path

            image_label, botao_abrir, botao_limpar = self.createImageLabelAndButtonsLinkedWithActions(img_label_and_path)
            if i == 0:
                titulo_label = self.createTituloImagem("Pessoa 1")
            elif i == 2:
                titulo_label = self.createTituloImagem("Pessoa Alvo")
            else:
                titulo_label = self.createTituloImagem("Pessoa 2")
            layout.addWidget(titulo_label, 0, i, 1, 2)
            layout.addWidget(image_label, 1, i, 1, 2)
            layout.addWidget(botao_abrir, 2, i)
            layout.addWidget(botao_limpar, 2, i+1)

        # inserir botão para processar e dar o resultado em um QLAbel no layout

        self.text_edit_resultado = QTextEdit(self)
        self.text_edit_resultado.setReadOnly(True)
        self.text_edit_resultado.append('Abra as fotos e clique Processar para saber quem parece mais com a Pessoa Alvo')
        self.botao_processar = QPushButton('Processar')
        self.botao_processar.clicked.connect(self.iniciarProcessamento)

        layout.addWidget(self.botao_processar, 3, 0, 1, 6)
        layout.addWidget(self.text_edit_resultado, 4, 0, 1, 6)

        central_widget.setLayout(layout)

    def iniciarProcessamento(self):
        if any(p.image_path == '' for p in self.dict_pessoa_to_image_label_and_path.values()):
            self.text_edit_resultado.append('Alguma imagem não foi aberta. Use os botões para abrir 3 imagens.')
            return
        self.botao_processar.setEnabled(False)
        self.text_edit_resultado.append("Processando...")

        self.worker = Worker(self.dict_pessoa_to_image_label_and_path)
        self.worker.update_text_edit_signal.connect(self.updateProcessamento)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.start()

    def updateProcessamento(self, texto):
        self.botao_processar.setEnabled(True)
        self.text_edit_resultado.append(texto)

    def openImage(self, img_label_and_path):
        image_file, _ = QFileDialog.getOpenFileName(self, "Open Image", "",
                                                    "JPG Files (*.jpeg *.jpg );;PNG Files (*.png);;"
                                                    "Bitmap Files (*.bmp);;GIF Files (*.gif)")
        image = QPixmap(image_file)

        if not image.isNull():
            img_label_and_path.image_label.setPixmap(image.scaled(img_label_and_path.image_label.size(),
                                                                  Qt.AspectRatioMode.KeepAspectRatio,
                                                                  Qt.TransformationMode.SmoothTransformation))
            img_label_and_path.image_label.update()
            img_label_and_path.image_path = image_file
        else:
            QMessageBox.information(self, "No Image", "No Image Selected.", QMessageBox.StandardButton.Ok)

    def clearImage(self, img_label_and_path):
        img_label_and_path.image_label.clear()
        img_label_and_path.image_path = ''

    def mostrar_sobre_dialog(self):
        sobre_dialog = SobreDialog()
        sobre_dialog.exec()


def preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (160, 160))
    img = img.astype(np.float32)
    img = (img - 127.5) / 128.0  # Normalização)
    return np.expand_dims(img, axis=0)


def get_embedding_by_graph_and_img_path(graph, img_path):
    with tf.compat.v1.Session(graph=graph) as sess:
        images_placeholder = sess.graph.get_tensor_by_name("input:0")
        embeddings = sess.graph.get_tensor_by_name("embeddings:0")
        phase_train_placeholder = sess.graph.get_tensor_by_name("phase_train:0")
        resultado = sess.run(embeddings, feed_dict={images_placeholder: preprocess_image(img_path),
                                                    phase_train_placeholder: False})
    return resultado


if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setAttribute(
        Qt.ApplicationAttribute.AA_DontShowIconsInMenus, True)
    window = MainWindow()
    sys.exit(app.exec())
