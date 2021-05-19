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


def connection():
    params = {
        'access_key': '2b4183b16afefdf531be92c7fe94e413'
    }
    now = datetime.datetime.now()
    now.strftime("%d-%m-%Y")

    try:
        f = open(now.strftime("%d-%m-%Y") + " names.txt", 'r')
        api_response = json.load(f)
        f.close()
    except FileNotFoundError:
        f = open(now.strftime("%d-%m-%Y") + " names.txt", 'w')
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

    try:
        f = open(now.strftime("%d-%m-%Y") + " eod.txt", 'r')
        api_response = json.load(f)
        f.close()
    except FileNotFoundError:
        f = open(now.strftime("%d-%m-%Y") + " eod.txt", 'w')
        api_result = requests.get('http://api.marketstack.com/v1/eod/latest', params)
        api_response = api_result.json()
        json.dump(api_response, f)
        f.close()

    return data, api_response


class Istok(QtWidgets.QMainWindow):
    def __init__(self):
        super(Istok, self).__init__()
        self.wind = Ui_Istok()
        self.wind.setupUi(self)
        self.initiation()

    def initiation(self):
        self.wind.setupUi(self)
        self.wind.Allcomp.clicked.connect(self.open_Allcomp)  # Все компании
        self.wind.Relevcomp.clicked.connect(self.open_Relevcomp)  # Наиболее релевантные
        self.wind.Detail.clicked.connect(self.open_Detail)  # Детальное отслеживание
        self.data, self.api_response = connection()

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
        self.dialogRelev = Ui_Istok_relevants()
        self.dialogRelev.setupUi(self)
        self.dialogRelev.Back.clicked.connect(self.backbutton)

    def open_Detail(self):  # Детальное отслеживание
        self.dialogDet = Ui_Favorites()
        self.dialogDet.setupUi(self)
        self.schet = 0

        now = datetime.datetime.now()
        now.strftime("%d-%m-%Y")
        favlist = ""
        f = open(now.strftime("%d-%m-%Y") + " names.txt", 'r')
        api_response = json.load(f)
        f.close()
        f = open(now.strftime("%d-%m-%Y") + " eod.txt", 'r')
        api_response2 = json.load(f)
        f.close()
        symbols = {}
        for stock_data in api_response['data']:
            if stock_data['name']+"\n" in self.favorites:
                symbols.update({stock_data['symbol']: stock_data['name']})
        for stock_data in api_response2['data']:
            if stock_data != []:
                if stock_data['symbol'] in symbols.keys():
                    favlist = favlist + symbols[stock_data['symbol']] + "\n" + str(stock_data) + "\n"


        # for word in self.favorites:
        #     favlist = favlist + word + "\n"
        self.dialogDet.Favlist.setText(favlist)
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
