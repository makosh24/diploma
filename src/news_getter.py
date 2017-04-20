from bs4 import BeautifulSoup
from urllib.request import urlopen

import time
import datetime

def printProgress(current, total, done = False):

    print('[{}%] {}/{}'.format(str(int(100 * current / total)), str(current), str(total)), end = '\nDone!\n' if done else '\n')

def downloadNews(company, amount):

    domain = 'http://mfd.ru'
    prefix = 'http://mfd.ru/news/company/view/?id='
    suffix = '&page='
    page_number = 0
    news = []
    amount = int(amount)
    company = str(company)
    page_count = amount // 50
    last_page = amount % 50

    while page_number <= page_count:

        url = prefix + company + suffix + str(page_number)
        page = urlopen(url)
        data = BeautifulSoup(page, 'html.parser').find('table', {'id': 'issuerNewsList'}).findAll('tr')
        current = 0

        if page_number < page_count:
            total = len(data)
        else:
            total = last_page

        for i in range(total):
            printProgress(50 * page_number + current, amount)
            td = data[i].findAll('td')
            temp_date = td[0].getText().split(',')[0].strip()

            if temp_date == 'сегодня':
                today = datetime.date.today()
                item_date = today.strftime('%d/%m/%y')
            elif temp_date == 'вчера':
                yesterday = datetime.date.today() - datetime.timedelta(1)
                item_date = yesterday.strftime('%d/%m/%y')
            else:
                temp_date_split = temp_date.split('.')
                item_date = '{}/{}/{}'.format(str(temp_date_split[0]), str(temp_date_split[1]), str(temp_date_split[2][2:]))

            item_url = domain + td[1].find('a').get('href')
            item_page = urlopen(item_url)
            item_data = BeautifulSoup(item_page, 'html.parser').find('div', { 'class' : 'm-content' }).findAll('p')
            item_string = ''

            for j in range(1, len(item_data) - 2):
                item_string += item_data[j].getText() + ' '

            item_string = item_string.strip()

            if item_string != '':
                news.append((item_date, item_string))

            current += 1
            time.sleep(0.1)

        page_number += 1

    printProgress(amount, amount, True)

    return news[::-1]

def writeNews(news, output):

    output_file = open(output, 'w+', encoding = 'utf8')

    i = 0
    for (date, text) in news:
        if i != (len(news) - 1):
            output_file.write('\"{}\",\"{}\"\n'.format(date, text))
        else:
            output_file.write('\"{}\",\"{}\"'.format(date, text))
        i += 1

    output_file.close()

def readNews(path):

    temp = open(path, 'r', encoding = 'utf8')
    data = temp.read()
    news = []

    for item in data.split('\n'):
        split = item.split('\",\"')
        news.append((split[0][1:], split[1][:-1]))

    return news

def getDates(news):

    dates = []

    for (date, text) in news:
        if date not in dates:
            dates.append(date)

    return dates

def getNews(news, date):

    result = []

    for item in news:
        if item[0] == date:
            result.append(item[1])

    return result

def groupNews(news):

    result = {}
    dates = getDates(news)

    for date in dates:
        result.update({ date : getNews(news,date) })

    return result