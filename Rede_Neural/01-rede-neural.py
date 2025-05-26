import pandas as pd

## pre-processamento
## dados para análise
dataset = pd.read_csv('/Churn_Modelling.csv')
#print("Data Frame: \n", dataset)

## variaveis independentes, eixo X
## as 3 primeiras colunas não são relevantes para a análise
## todas as linhas [:,], da coluna 3 até a 13
X = dataset.iloc[:, 3:13].values
#print("Variaveis independentes: \n", X)

## variaveis dependentes (resultado conhecido)
y = dataset.iloc[:, 13].values
#print("Variaveis dependentes: \n", y)

## dados categóricos
## transformar os dados categóricos em dados númericos
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import make_column_transformer

## coluna de país possui dados categóricos
## Label Encoder: atribui um número inteiro para cada categoria, normalmente em ordem alfabética
labelencoder_X_1 = LabelEncoder()
X[:, 1] = labelencoder_X_1.fit_transform(X[:, 1])
#print("Coluna de País com Label Encoder aplicado: ", X[:, 1])

## coluna de genero possui dados categóricos
labelencoder_X_2 = LabelEncoder()
X[:, 2] = labelencoder_X_2.fit_transform(X[:, 2])
#print("Coluna de Genero com Label Encoder aplicado: ", X[:, 2])

## One Hot Encoding: cria uma coluna para cada categoria e marca com 1 ou 0 se a categoria está presente
# Removed the 'sparse=False' argument as it is no longer supported in newer versions of scikit-learn
onehotencoder = make_column_transformer((OneHotEncoder(categories='auto'), [1]), remainder="passthrough")
#onehotencoder= make_column_transformer((OneHotEncoder(categories='auto', sparse = False), [1]), remainder="passthrough")

## adiciona as colunas do one-hot encoder ao conjunto de dados X
X=onehotencoder.fit_transform(X)

## remove a variável "dummy"
X = X[:,1:]
#print("One hot encoding: ", X)

## separa dos dados em treino e teste
from sklearn.model_selection import train_test_split
## test_size = 20% para teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)
#print("TREINO - Dados X: \n", X_train)
#print("TESTE - Dados X: \n", X_test)
#print("TREINO - Dados Y: \n", y_train)
#print("TESTE - Dados Y: \n", y_test)

## padronização dos dados feature scaling
## coloca os dados na mesma escala
from sklearn.preprocessing import StandardScaler

sc = StandardScaler()

X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)
#print("Padronização dos dados: \n", X_train)
#print("Padronização dos dados: \n", X_test)


## rede neural
from keras.models import Sequential ## inicia a rede neural
from keras.layers import Dense ## Dense para as camadas da rede neural, camadas inter-conectadas

## essa rede neural é uma rede de classificação, por isso "classifier"
classifier = Sequential()

## units = numero de neuronios da rede neural
## kernel_initializer = como os pesos da rede serão inicializados
## activation = função de ativação usando a função ReLu
## input_dim = é a camada de entrada, informa que tem 11 atributos na camada de entrada
classifier.add(Dense(units = 6, kernel_initializer = 'uniform', activation = 'relu', input_dim = 11))

## camada interna (camada oculta)
classifier.add(Dense(units = 6, kernel_initializer = 'uniform', activation = 'relu'))

## camada de saída aplica a função Sigmoid
## units = 1, possui 1 neuronio
classifier.add(Dense(units = 1, kernel_initializer = 'uniform', activation = 'sigmoid'))

## compila o modelo
## adam usa Stochastic Gradient Descent (SGD)
## loss = função de perda/ajuste da rede
## metrics para avaliar o modelo
classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

## faz o treino da rede neural
## batch_size = numeros de registros q vai passar pela rede antes de atualizar os pesos
## epochs = numero de vezes que os dados irão passar pela rede 
classifier.fit(X_train, y_train, batch_size = 10, epochs = 100)

## depois de treinar a rede neural, agora usa os dados de teste para gerar uma previsão
## faz a previsão dos dados de teste
y_pred = classifier.predict(X_test)

## se for acima de 50% ou igual a previsão é verdadeiro, se for abaixo de 50% é falso
y_pred = (y_pred > 0.5)
print("Valores previstos usando dados de teste: ", y_pred)


## matriz de confusão para comparar os valores conhecidos com os valores previstos pela rede
## a matriz mostra o desempenho da rede
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
print("Matriz de Confusão: \n", cm)
