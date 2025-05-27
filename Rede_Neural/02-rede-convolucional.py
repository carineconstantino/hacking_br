from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense


## criando a rede neural
classifier = Sequential()

## camada convolucional Conv2D
## Conv2D aplica os filtros 32 é numero de filtros (numero de dectores de caracteristicas), 3x3 filtering detection
## input_shape = 64,64 e 3, define os pixes horizontal e vertical e os 3 canais do RGB 
## activation = função de ativação ReLU
classifier.add(Conv2D(32, (3, 3), input_shape = (64, 64, 3), activation = 'relu'))

## camada max pooling = destaca as características mais importantes, mais ou menos 25% da imagem. Reduz o overfitting
## reduz a complexidade de imagem
## pool_size define a matriz, padrão 2x2
## mapa de caracteristicas mais importantes
classifier.add(MaxPooling2D(pool_size = (2, 2))) 

## camada de flattening 
## cria o vetor da imagem
classifier.add(Flatten())


## camada full connection, arquitetura da camada de entrada e camada de saída
## basicamente é uma rede neural
## camada de entrada
classifier.add(Dense(units = 128, activation = 'relu'))

## camada de saída
classifier.add(Dense(units = 1, activation = 'sigmoid'))

## camada para compilar a rede 
classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])


## pre processamento de imagem para evitar super ajuste - overffiting
from keras.preprocessing.image import ImageDataGenerator

## rescale = transforma o tamanho da imagem - redimensionamento
## shear_range = transformações geométricas aleatórias na imagem
## zoom_range = zoom aleatório na imagem
## horizontal_flip = espelhamento horizontal aleatório na imagem
train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)

## reajusta os pixes
test_datagen = ImageDataGenerator(rescale = 1./255)

## dados de treino
## target_size = tamanho da imagem
## batch_size = tamanho do bloco de imagem que será processado de cada vez

training_set = train_datagen.flow_from_directory('dataset/training_set',
                                                 target_size = (64, 64),
                                                 batch_size = 32,
                                                 class_mode = 'binary')

## dados de teste
test_set = test_datagen.flow_from_directory('dataset/test_set',
                                            target_size = (64, 64),
                                            batch_size = 32,
                                            class_mode = 'binary')

## configura a rede para ser treinada
classifier.fit_generator(training_set,steps_per_epoch = 8000,epochs = 25,validation_data = test_set,validation_steps = 2000)
