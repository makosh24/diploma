#region Import
from news_getter import downloadNews
from news_getter import writeNews
from news_getter import readNews

from stocks_getter import downloadStock
from stocks_getter import writeStock
from stocks_getter import readStock

from stemmer import stem

from connector import connect
from connector import writeConnections
from connector import readConnections

from helper import minArray
from helper import maxArray
from helper import normalizeArray
from helper import denormalizeArray

from keras.preprocessing import sequence
from keras.preprocessing.text import Tokenizer
from keras.models import Sequential
from keras.models import load_model
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM
from keras.layers import Dropout
from keras.layers import Dense
from keras.layers import Activation
from keras.regularizers import l1_l2
from keras.optimizers import Adam
from keras.losses import binary_crossentropy
from keras.metrics import binary_accuracy

import numpy
import os
import csv
#endregion

#region System
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
#path = 'D:\\Projects\\Diploma\\src\\'
path = '/home/zernov/Documents/Projects/diploma/src/'
#endregion

#region Data
company = 'gazprom'
amount = 2500
datef = '01/09/2016'
datet = '08/05/2017'
#endregion

#region Learning
num_words = 3000
dropout_rate = 0.5
dimension = 16
l1_rate = 0.1
l2_rate = 0.1
l_rate = 0.01
batch_size = 2
epochs = 16
validation_split = 0.1
#endregion

#region News Getter
#news_dates, news, news_count = downloadNews(company, amount)
#writeNews(news_dates, news, news_count, path + 'news/{}.csv'.format(company))
#news_dates, news, news_count = readNews(path + 'news/{}.csv'.format(company))
#endregion

#region Stock Getter
#stocks_dates, stocks, stocks_count = downloadStock(company, datef, datet)
#writeStock(stocks_dates, stocks, stocks_count, path + 'stocks/{}.csv'.format(company))
#stocks_dates, stocks, stocks_count = readStock(path + 'stocks/{}.csv'.format(company))
#endregion

#region Stemmer
#stems_dates, stems, stems_count = stem(news_dates, news, news_count)
#writeNews(stems_dates, stems, stems_count, path + 'stems/{}.csv'.format(company))
#stems_dates, stems, stems_count = readNews(path + 'stems/{}.csv'.format(company))
#endregion

#region Connector
#connections_dates, connections_news, connections_stocks, connections_count = connect(stems_dates, stems, stems_count, stocks_dates, stocks, stocks_count)
#writeConnections(connections_dates, connections_news, connections_stocks, connections_count, path + 'connections/{}.csv'.format(company))
connections_dates, connections_news, connections_stocks, connections_count = readConnections(path + 'connections/{}.csv'.format(company))
#endregion

tokenizer = Tokenizer(num_words=num_words)
tokenizer.fit_on_texts(texts=connections_news)

total_dates = connections_dates
total_news = tokenizer.texts_to_sequences(connections_news)
total_stocks = connections_stocks
total_count = connections_count

total_news_sequence = sequence.pad_sequences(sequences=total_news)

border = int(connections_count * 0.75)

training_dates = total_dates[:border]
training_news = total_news_sequence[:border]
training_stocks = total_stocks[:border]
training_count = border

testing_dates = total_dates[border:]
testing_news = total_news_sequence[border:]
testing_stocks = total_stocks[border:]
testing_count = total_count - border

training_X = numpy.array(training_news)
training_y = numpy.array(training_stocks)

testing_X = numpy.array(testing_news)
testing_y = numpy.array(testing_stocks)

def fit(name):

    model = Sequential()
    model.add(Embedding(input_dim=num_words, output_dim=dimension))
    model.add(LSTM(units=dimension))
    model.add(Dropout(rate=dropout_rate))
    model.add(Dense(units=1, kernel_regularizer=l1_l2(l1=l1_rate, l2=l2_rate)))
    model.add(Activation(activation='sigmoid'))
    model.compile(optimizer=Adam(lr=l_rate), loss=binary_crossentropy, metrics=[binary_accuracy])

    hist = model.fit(training_X, training_y, batch_size=batch_size, epochs=epochs, validation_split=validation_split)
    model.save(path + 'models/{}_model-{}.h5'.format(company, name))

    with open(path + 'models/{}_history-{}.txt'.format(company, name), 'w+', encoding='utf8') as temp:
        temp.write(str(hist.history))

    score = model.evaluate(testing_X, testing_y, batch_size=batch_size)
    with open(path + 'models/{}_score-{}.txt'.format(company, name), 'w+', encoding='utf8') as temp:
        temp.write(str(score))

def predict(X, name):

    model = load_model(path + 'models/{}_model-{}.h5'.format(company, name))

    result = model.predict(X)

    return result
'''
fit('01')

y = predict(training_X, '01')
for item in y:
    print(item, end = ' ')
print()
for item in y:
    print(0 if item[0] < 0.5 else 1, end = ' ')
print()
for item in training_y:
    print(item, end = ' ')
kek = 0
print()
for i in range(len(y)):
    lol = 0 if y[i][0] < 0.5 else 1
    if (str(lol) == str(training_y[i])):
        kek += 1
        print('+', end = ' ')
    else:
        print('-', end = ' ')
print()
print(kek / len(y))
'''

tokenizer2 = Tokenizer(num_words=num_words)
tokenizer2.fit_on_texts(texts=['итог торг стоимост глобальн депозитарн расписок роснефт выросл доллар лукойл доллар цен расписок новатэк доллар бумаг газпром подрожа доллар цен расписок газпр нефт оста уровн предыдущ закрыт доллар бумаг втб подешевел доллар сбербанк доллар стоимост расписок котор вход тинькофф банк уменьш доллар расписк норникел выросл цен оказа уровн доллар северста доллар стоимост бумаг нлмк показа никак динамик сохран уровн доллар цен бумаг магнит опуст доллар лент доллар бумаг афк систем выросл стоимост доллар дан укртрансгаз уровен заполнен хранилищ увелич состоян сентябр украинск пхг наход миллиард кубометр газ ран премьер министр украин владимир гройсма сообщ правительств нафтогаз ищут компромисс вопрос минимальн объем газ пхг котор необходим накоп начал отопительн сезон слов реч идет диапазон миллиард кубометр очеред глав минэнерг украин игор насалик говор украин сможет накоп пхг рамк подготовк зим миллиард кубометр газ счет европейск направлен закупок росс глав газпром алекс миллер август выража обеспокоен уровн закачк газ пхг украин'])
indxs = tokenizer2.texts_to_sequences(['итог торг стоимост глобальн депозитарн расписок роснефт выросл доллар лукойл доллар цен расписок новатэк доллар бумаг газпром подрожа доллар цен расписок газпр нефт оста уровн предыдущ закрыт доллар бумаг втб подешевел доллар сбербанк доллар стоимост расписок котор вход тинькофф банк уменьш доллар расписк норникел выросл цен оказа уровн доллар северста доллар стоимост бумаг нлмк показа никак динамик сохран уровн доллар цен бумаг магнит опуст доллар лент доллар бумаг афк систем выросл стоимост доллар дан укртрансгаз уровен заполнен хранилищ увелич состоян сентябр украинск пхг наход миллиард кубометр газ ран премьер министр украин владимир гройсма сообщ правительств нафтогаз ищут компромисс вопрос минимальн объем газ пхг котор необходим накоп начал отопительн сезон слов реч идет диапазон миллиард кубометр очеред глав минэнерг украин игор насалик говор украин сможет накоп пхг рамк подготовк зим миллиард кубометр газ счет европейск направлен закупок росс глав газпром алекс миллер август выража обеспокоен уровн закачк газ пхг украин'])

for item in tokenizer2.word_index:
    print(tokenizer2.word_index[item], ' ', item)

print(indxs)