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
import sys
#endregion

#region System
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
path = 'D:\\Projects\\Diploma\\src\\'
sep = '\\'
#path = '/home/zernov/Documents/Projects/diploma/src/'
#sep = '/'
#endregion

predict_path = ''

#region Learning
num_words = 5000
dropout_rate = 0.5
dimension = 64
l1_rate = 0.1
l2_rate = 0.1
l_rate = 0.01
batch_size = 2
epochs = 32
validation_split = 0.25
#endregion

def getData(company, amount, datef, datet):

    news_dates, news, news_count = downloadNews(company, amount)
    writeNews(news_dates, news, news_count, path + 'news' + sep + '{}.csv'.format(company))
    #news_dates, news, news_count = readNews(path + 'news' + sep + '{}.csv'.format(company))

    stocks_dates, stocks, stocks_count = downloadStock(company, datef, datet)
    writeStock(stocks_dates, stocks, stocks_count, path + 'stocks' + sep + '{}.csv'.format(company))
    #stocks_dates, stocks, stocks_count = readStock(path + 'stocks' + sep + '{}.csv'.format(company))

    stems_dates, stems, stems_count = stem(news_dates, news, news_count)
    writeNews(stems_dates, stems, stems_count, path + 'stems' + sep + '{}.csv'.format(company))
    #stems_dates, stems, stems_count = readNews(path + 'stems' + sep + '{}.csv'.format(company))

    connections_dates, connections_news, connections_stocks, connections_count = connect(stems_dates, stems, stems_count, stocks_dates, stocks, stocks_count)
    writeConnections(connections_dates, connections_news, connections_stocks, connections_count, path + 'connections' + sep + '{}.csv'.format(company))
    #connections_dates, connections_news, connections_stocks, connections_count = readConnections(path + 'connections' + sep + '{}.csv'.format(company))

def readData(company):

    return readConnections(path + 'connections' + sep + '{}.csv'.format(company))

def fit(company, training_X, training_y, testing_X, testing_y):

    model = Sequential()
    model.add(Embedding(input_dim=num_words, output_dim=dimension))
    model.add(LSTM(units=dimension))
    model.add(Dropout(rate=dropout_rate))
    model.add(Dense(units=1, kernel_regularizer=l1_l2(l1=l1_rate, l2=l2_rate)))
    model.add(Activation(activation='sigmoid'))
    model.compile(optimizer=Adam(lr=l_rate), loss=binary_crossentropy, metrics=[binary_accuracy])

    hist = model.fit(training_X, training_y, batch_size=batch_size, epochs=epochs, validation_split=validation_split)
    model.save(path + 'models' + sep + '{}_model.h5'.format(company))

    with open(path + 'models' + sep + '{}_history.txt'.format(company), 'w+', encoding='utf8') as temp:
        temp.write(str(hist.history))

    score = model.evaluate(testing_X, testing_y, batch_size=batch_size)
    with open(path + 'models' + sep + '{}_score.txt'.format(company), 'w+', encoding='utf8') as temp:
        temp.write(str(score))

def predict(X, company):

    model = load_model(path + 'models' + sep + '{}_model.h5'.format(company))

    result = model.predict(X)

    return result


if sys.argv[1] == '-f':
    company = 'sberbank'
    #company = sys.argv[2]
    amount = 150
    #amount = sys.argv[3]
    datef = '01/09/2015'
    #datef = sys.argv[4]
    datet = '28/05/2017'
    #datet = sys.argv[5]
    #getData(company, amount, datef, datet)
else:
    company = 'sberbank'
    #company = sys.argv[2]
    predict_path = 'test.csv'
    #predict_path = sys.argv[3]

connections_dates, connections_news, connections_stocks, connections_count = readData(company)

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

total_X = numpy.array(total_news_sequence)
total_y = numpy.array(total_stocks)

training_X = numpy.array(training_news)
training_y = numpy.array(training_stocks)

testing_X = numpy.array(testing_news)
testing_y = numpy.array(testing_stocks)

if sys.argv[1] == '-f':
    fit(company, training_X, training_y, testing_X, testing_y)
else:
    news_dates, news, news_count = readNews(path + predict_path)
    stems_dates, stems, stems_count = stem(news_dates, news, news_count)
    news_sequences = sequence.pad_sequences(sequences=tokenizer.texts_to_sequences(stems))
    y = predict(news_sequences, company)
    print(y)