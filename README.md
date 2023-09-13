# Quem Parece Mais?

Este programa permite comparar rostos de duas pessoas com uma pessoa alvo. Tem uma interface gráfica implementada 
em Qt 6 e usa a rede neural pré-treinada disponível no repositório [FaceNet](https://github.com/davidsandberg/facenet), 
onde está a implementação original do método proposto no artigo: ["FaceNet: A Unified Embedding for Face Recognition and Clustering"](http://arxiv.org/abs/1503.03832).
O modelo foi treinado usado o conjunto de dados [VGGFace2](https://www.robots.ox.ac.uk/~vgg/data/vgg_face2/) e a 
arquitetura de rede usada foi a Inception ResNet v1, que é uma rede neural convolucional com várias camadas e 
milhares de neurônios.

A ideia
do treinamento é usar redes neurais siamesas, onde um par de redes neurais compartilham os mesmos pesos, mas cada uma 
recebe uma imagem distinta. Uma função chamada triplet loss é usada para que a aprendizagem consiga 
ajustar uma rede que gere os chamados embeddings das imagens (vetores com 512 características) que fiquem mais 
distantes se são pessoas diferentes e mais próximas se são a mesma pessoa em um mesmo espaço de características.

O programa aqui implementado serve para calcular a distância dos pares de embeddings que representam cada foto e 
retorna qual pessoa tem a menor distância entre ela e a pessoa alvo. Esta é uma função que foi aprendida 
para a tarefa de reconhecimento facial, ou seja, se a pessoa é ou não é aquela com quem ela está sendo comparada e não
para aprender semelhanças entre pessoas. Por isso não é garantido que o programa vai de fato acertar, mas é divertido
ver o que a rede neural vai nos dizer.

## Binário

Foi compilado um executável do programa para Windows usando o comando:
<pre>
pyinstaller --onefile --noconsole --add-binary "images/clear.png;./images" --add-binary "images/open_file.png;./images" --add-binary "model/20180402-114759.pb;./model" --add-binary "images/bebe.png;./images" main.py
</pre>
Ele está disponível como release no repositório.