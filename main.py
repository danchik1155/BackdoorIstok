import requests
import datetime

import json

from PyQt5 import QtWidgets
import time

from MainIstok import Ui_Istok
from Allcomp import Ui_List
from Istok_relevants import Ui_Istok_relevants
from Favorites import Ui_Favorites
from Search import Ui_Search

def bypercent_key(summ):
    return summ[1][0]

def connection():
    params = {
        'access_key': '2b4183b16afefdf531be92c7fe94e413'
    }
    now = datetime.datetime.now()
    now.strftime("%d-%m-%Y")

    try:
        f = open("names.txt", 'r')
        api_response = json.load(f)
        f.close()
    except FileNotFoundError:
        f = open("names.txt", 'w')
        api_result = requests.get('http://api.marketstack.com/v1/tickers', params)
        api_response = api_result.json()
        json.dump(api_response, f)
        f.close()

    data = ''
    symbols = ''
    i = 0
    for stock_data in api_response['data']:
        data = data + stock_data['name'] + "\n"
        if i == 0:
            symbols = stock_data['symbol']
        if i < 98:
            symbols = symbols + "," + stock_data['symbol']
        i += 1

    params = {
        'access_key': '2b4183b16afefdf531be92c7fe94e413',
        'symbols': symbols
    }

    yesterday = datetime.date.today() - datetime.timedelta(days=1)

    try:
        f = open(yesterday.strftime('%d-%m-%Y') + " eod.txt", 'r')
        f.close()
    except FileNotFoundError:
        f = open(yesterday.strftime('%d-%m-%Y') + " eod.txt", 'w')
        api_result = requests.get('http://api.marketstack.com/v1/eod/latest', params)
        api_response = api_result.json()
        json.dump(api_response, f)
        f.close()

    yesterday = datetime.date.today() - datetime.timedelta(days=2)

    try:
        f = open(yesterday.strftime('%d-%m-%Y') + " eod.txt", 'r')
        f.close()
    except FileNotFoundError:
        f = open(yesterday.strftime('%d-%m-%Y') + " eod.txt", 'w')
        api_result = requests.get('http://api.marketstack.com/v1/eod/' + yesterday.strftime('%Y-%m-%d'), params)
        api_response = api_result.json()
        json.dump(api_response, f)
        f.close()

    return data


class Istok(QtWidgets.QMainWindow):
    def __init__(self):
        super(Istok, self).__init__()
        self.wind = Ui_Istok()
        self.wind.setupUi(self)
        self.page = 1
        self.len_of_relevants = int(4)
        self.initiation()

    def initiation(self):
        self.wind.setupUi(self)

        self.wind.Allcomp.clicked.connect(self.open_Allcomp)  # Все компании
        self.wind.Relevcomp.clicked.connect(self.open_Relevcomp)  # Наиболее релевантные
        self.wind.Detail.clicked.connect(self.open_Detail)  # Детальное отслеживание
        self.data = connection()
        self.now = datetime.date.today() - datetime.timedelta(days=1)
        self.yesterday = datetime.date.today() - datetime.timedelta(days=2)



        try:
            f = open("favorites.txt", 'r')
            self.favorites = f.readlines()
            f.close()
        except FileNotFoundError:
            self.favorites = list()

    def open_Allcomp(self):  # Все компании
        self.dialogAll = Ui_List()
        self.dialogAll.setupUi(self)
        # print(self.data)
        self.dialogAll.textBrowser.setText(self.data)
        self.dialogAll.Back.clicked.connect(self.backbutton)

    def open_Relevcomp(self):  # Наиболее релевантные
        relevants = self.find_relevant(self.len_of_relevants)
        self.dialogRelev = Ui_Istok_relevants()
        self.dialogRelev.setupUi(self)
        self.dialogRelev.PageNo.setText(str(self.page))
        self.dialogRelev.Name1.setText(str(relevants[self.page * 2 - 2][0]))
        self.dialogRelev.Name2.setText(str(relevants[self.page * 2 - 1][0]))
        self.dialogRelev.Discript1.setText(str(relevants[self.page * 2 - 2][1]))
        self.dialogRelev.Discript2.setText(str(relevants[self.page * 2 - 1][1]))
        self.dialogRelev.right.clicked.connect(self.next_page)
        self.dialogRelev.left.clicked.connect(self.prev_page)
        self.dialogRelev.Back.clicked.connect(self.backbutton)

    def find_relevant(self, n: int):
        f = open("names.txt", 'r')
        api_response = json.load(f)
        f.close()
        f = open(self.now.strftime("%d-%m-%Y") + " eod.txt", 'r')
        api_response2 = json.load(f)
        f.close()
        f = open(self.yesterday.strftime('%d-%m-%Y') + " eod.txt", 'r')
        api_response3 = json.load(f)
        f.close()
        symbols = {}
        favlist = {}
        old_favlist = {}
        relevants_keys = []
        i = 0
        for stock_data in api_response['data']:
            symbols.update({stock_data['symbol']: stock_data['name']})
            if i < n:
                relevants_keys.append(stock_data['symbol'])
                i += 1
        for stock_data in api_response2['data']:
            if stock_data != []:
                if stock_data['symbol'] in symbols.keys():
                    old_favlist.update({stock_data['symbol']: stock_data})

        favlist.update(old_favlist)

        for stock_data in api_response3['data']:
            if stock_data != []:
                if stock_data['symbol'] in symbols.keys():
                    x = float(favlist[stock_data['symbol']]['high'])
                    y = float(stock_data['high'])
                    z = x - y
                    open_day = float(old_favlist[stock_data['symbol']]['open'])
                    close_day = float(old_favlist[stock_data['symbol']]['close'])
                    favlist[stock_data['symbol']] = [round(100 * z / x, 3), round(z, 3), round(open_day - close_day, 3)]

        for key in favlist.keys():
            if not isinstance(favlist[key], list):
                favlist[key] = [0.0, 0.0, 0.0]  # первое - проценты, второе - это в деньгах

        for key in favlist.keys():
            if key in relevants_keys:
                continue
            min_key = self.chek_min(relevants_keys, favlist)
            if favlist[key][0] > favlist[min_key][0]:
                relevants_keys[relevants_keys.index(min_key)] = key

        relevants = []

        for i in relevants_keys:
            relevants.append([symbols[i], favlist[i]])

        relevants = sorted(relevants, key=bypercent_key, reverse=True)
        return relevants

    def chek_min(self, relevants_keys, favlist):
        min_value = favlist[relevants_keys[0]][0]
        need_key = favlist[relevants_keys[0]][0]
        for i in range(len(relevants_keys)):
            if favlist[relevants_keys[i]][0] <= min_value:
                need_key = relevants_keys[i]
                min_value = favlist[relevants_keys[i]][0]
        return need_key

    def next_page(self):
        if self.page + 1 <= self.len_of_relevants/2:
            self.page += 1
            self.open_Relevcomp()

    def prev_page(self):
        if self.page - 1 >= 1:
            self.page -= 1
            self.open_Relevcomp()

    def open_Detail(self):  # Детальное отслеживание
        self.dialogDet = Ui_Favorites()
        self.dialogDet.setupUi(self)
        self.schet = 0

        f = open("names.txt", 'r')
        api_response = json.load(f)
        f.close()
        f = open(self.now.strftime("%d-%m-%Y") + " eod.txt", 'r')
        api_response2 = json.load(f)
        f.close()
        f = open(self.yesterday.strftime('%d-%m-%Y') + " eod.txt", 'r')
        api_response3 = json.load(f)
        f.close()
        symbols = {}
        favlist = {}
        oldfavlist = {}
        for stock_data in api_response['data']:
            if stock_data['name'] + "\n" in self.favorites:
                symbols.update({stock_data['symbol']: stock_data['name']})
        for stock_data in api_response2['data']:
            if stock_data != []:
                if stock_data['symbol'] in symbols.keys():
                    oldfavlist.update({symbols[stock_data['symbol']] + "\n": stock_data['high']})

        favlist.update(oldfavlist)

        for stock_data in api_response3['data']:
            if stock_data != []:
                if stock_data['symbol'] in symbols.keys():
                    favlist[symbols[stock_data['symbol']] + "\n"] = favlist[symbols[stock_data['symbol']] + "\n"] - \
                                                                    stock_data['high']

        favlisttext = ''

        for key in favlist.keys():
            if favlist[key] == oldfavlist[key]:
                favlist[key] = 0

        for key in favlist.keys():
            favlisttext = favlisttext + key + "Разница за день: " + str(favlist[key]) + "\n"

        # for word in self.favorites:
        #     favlist = favlist + word + "\n"
        self.dialogDet.Favlist.setText(favlisttext)
        self.dialogDet.Add.clicked.connect(self.open_Add)
        self.dialogDet.Delete.clicked.connect(self.open_Delete)
        self.dialogDet.Back.clicked.connect(self.backbutton)

    def open_Add(self):
        self.dialogAdd = Ui_Search()
        self.dialogAdd.setupUi(self)
        self.dialogAdd.Go.clicked.connect(self.search)
        self.dialogAdd.Back.clicked.connect(self.backbutton)
        self.dialogAdd.Choose.clicked.connect(self.chooseAdd)

    def open_Delete(self):
        self.dialogAdd = Ui_Search()
        self.dialogAdd.setupUi(self)
        self.dialogAdd.Go.clicked.connect(self.search)
        self.dialogAdd.Back.clicked.connect(self.backbutton)
        self.dialogAdd.Choose.clicked.connect(self.chooseDelete)

    def search(self):
        self.schet = 0
        text = self.data.split('\n')
        sub_str = self.dialogAdd.Searchline.text()
        words = ""
        low_sub_str = sub_str.lower()
        for word in text:
            if low_sub_str in word.lower():
                words = words + word + "\n"
                self.schet += 1
        if words != "":
            self.dialogAdd.Result.setText(words)
            self.keyWord = words
        else:
            self.dialogAdd.Result.setText("Такой компании нет")

    def chooseAdd(self):
        if self.schet == 1:
            if self.keyWord in self.favorites:
                print("already in favorites")
            else:
                if self.favorites != [""]:
                    self.favorites.append(self.keyWord)
                    self.writefavs()
                else:
                    self.favorites[0] = self.keyWord
                    self.writefavs()

    def chooseDelete(self):
        if self.schet == 1:
            print('Ok')
            if self.keyWord in self.favorites:
                self.favorites.pop(self.favorites.index(self.keyWord))
                self.writefavs()
            else:
                print("not in favorites")

    def writefavs(self):
        f = open("favorites.txt", "w")
        for word in self.favorites:
            f.write(word)
        f.close()

    def backbutton(self):
        self.initiation()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Istok()
    window.show()
    app.exec_()
