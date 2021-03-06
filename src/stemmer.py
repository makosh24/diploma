from helper import printProgress

from nltk.stem.snowball import RussianStemmer
from nltk.corpus import stopwords

from keras.preprocessing.text import text_to_word_sequence

from string import punctuation

import sys

#import nltk
#nltk.download('stopwords')

stemmer = RussianStemmer()
stemmer.stopwords = stopwords.words('russian')

def stem(news_dates, news, news_count):

    stems_dates = []
    [stems_dates.append(date) for date in news_dates if date not in stems_dates]
    stems = []
    stems_count = len(stems_dates)
    i = 0
    j = 0

    print('Stemming news...')
    sys.stdout.flush()

    while i < stems_count:
        stem = []
        printProgress(i, stems_count)

        while j < news_count and stems_dates[i] == news_dates[j]:
            words = text_to_word_sequence(news[j], filters = ''.join(punctuation) + '–—01234567890abcdefghijklmnopqrstuvwxyz')
            for word in words:
                if word not in stemmer.stopwords and word != ' ':
                    stem.append(stemmer.stem(word))

            j += 1

        i += 1
        stems.append(' '.join(stem))

    printProgress(stems_count, stems_count, True)
    print('Done!')
    sys.stdout.flush()

    return stems_dates, stems, stems_count