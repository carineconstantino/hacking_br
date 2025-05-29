import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# data frame 
# dados para testar o modelo
dataset_train = pd.read_csv('/content/Google_Stock_Price_Train.csv')
#print("Data Frame: \n", dataset_train)

# variáveis independentes
# values cria um alias para as variáveis independentes
# a previsão será feita usando o valor de abertura do preço das ações
training_set = dataset_train.iloc[:, 1:2].values
#print("Variáveis independentes: \n", training_set)


# normalização com feature scalling
from sklearn.preprocessing import MinMaxScaler

# coloca os valores na mesma escala
# transforma os valores entre 0 e 1
sc = MinMaxScaler(feature_range = (0, 1))
#print("Aplica a normalização para ficar entre 0 e 1: \n", sc)

# dados já normalizados 
training_set_scaled = sc.fit_transform(training_set)
#print("Dados normalizados: \n",training_set_scaled)


# listas com dados de treino e dados de teste
# x_train intervalo de 60 dias
X_train = []
# y_train é o resultado
y_train = []

# intervalo de 60 dias que deverá ser avaliado para gerar a previsão
# 1258 = número de dias para ser observado
for i in range(60, 1258):
  # define para sempre buscar 60 dias para atrás
    X_train.append(training_set_scaled[i-60:i, 0])
    # 
    y_train.append(training_set_scaled[i, 0])

# cria um index com os dados organizados em 60 dias
X_train, y_train = np.array(X_train), np.array(y_train)
#print("Dados para avaliar: \n", X_train)
#print("Dados conhecidos/Resultado conhecido (histórico): \n", y_train)

# organiza os dados no formato do Keras em 3 dimensões:
# batch_size = quantidade de dados que irão "passar" pela rede neural a cada treinamento
# será usado o numero de linhas no shape[0]
# time steps = são 60 time steps
# numero de indicadores = 1 
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
#print("Dados formatados para o keras: \n", X_train)

# Rede Neural
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout

# inicia a rede 
regressor = Sequential()

# 1
# camada de entrada
# LSTM é o tipo da rede
# units = quantidade de neurônios
# return_sequence = rede neural em sequência para ocorrer o treino
# input_shape = objeto criado para o keras, objeto em 3 dimensões
regressor.add(LSTM(units = 50, return_sequences = True, input_shape = (X_train.shape[1], 1)))

# camada Dropout para reduzir o overfitting
# remove alguns neurônios, neste caso são 2 neurônios
regressor.add(Dropout(0.2))

# 2
# camadas internas
regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))
# 3
regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))

# 4
# ultima camada oculta
# remove o return_sequences
regressor.add(LSTM(units = 50))
regressor.add(Dropout(0.2))

# camada de saída
regressor.add(Dense(units = 1))

# compila da rede neural 
# a rede usa lógica de regressão e não de classificação
# e por isso usa a função loss = 'mean_squared_error'
# otimizador da rede = adam
regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')

# cria as epocs para treinar a rede
regressor.fit(X_train, y_train, epochs = 100, batch_size = 32)

# dados de teste
dataset_test = pd.read_csv('/content/Google_Stock_Price_Test.csv')
#print("Dados de teste: \n", dataset_test)

# variáveis independentes dos dados de teste
# não se normaliza os dados de teste
real_stock_price = dataset_test.iloc[:, 1:2].values

# concatena os dados de ttreino e dados de treino usando a coluna "Open"
dataset_total = pd.concat((dataset_train['Open'], dataset_test['Open']), axis = 0)
#print("Dados concatenados: \n", dataset_total)


# len(dataset_test) = 20 dias
# dataset_total = concatenação dos dados de treino (1258 dias) + dados de teste (20 dias) = 1278 dias
# len(dataset_total) - len(dataset_test) - 60 = 1278 - 20 - 60 = 1198
inputs = dataset_total[len(dataset_total) - len(dataset_test) - 60:].values

inputs = inputs.reshape(-1,1)
# faz a normalização dos dados concatenados
inputs = sc.transform(inputs)

# lista
X_test = []


# começa em 60, vai até 79 (inclusive) ⇒ total de 20 iterações
# a cada iteração, ele pega uma janela de 60 dias anterior ao dia i (em inputs) e armazena como uma entrada de teste
for i in range(60, 80):
    X_test.append(inputs[i-60:i, 0])

# cria um indice com os dados de teste
X_test = np.array(X_test)

# organiza os dados de teste de acordo com o keras
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

# previsão do valor das ações 
predicted_stock_price = regressor.predict(X_test)
predicted_stock_price = sc.inverse_transform(predicted_stock_price)

# gráfico de previsões 
# compara os valores reais com os valores previstos pela rede
plt.plot(real_stock_price, color = 'red', label = 'Dados Reais de Ações do Google')
plt.plot(predicted_stock_price, color = 'blue', label = 'Dados Previstos de Ações do Google')
plt.title('Previsão de Preços de Ações')
plt.xlabel('Tempo')
plt.ylabel('Preços de Ações do Google')
plt.legend()
plt.show()
