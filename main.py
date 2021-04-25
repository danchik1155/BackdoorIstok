import requests
import json

from PyQt5 import QtWidgets
import time

from MainIstok import Ui_Istok
from Allcomp import Ui_List
from Istok_relevants import  Ui_Istok_relevants
from Favorites import  Ui_Favorites


def connection():
    params = {
        'access_key': '2b4183b16afefdf531be92c7fe94e413'
    }
    # api_result = requests.get('http://api.marketstack.com/v1/tickers/aapl/eod', params)
    api_result = requests.get('http://api.marketstack.com/v1/tickers', params)
    api_response = api_result.json()

    data = ''
    symbols = ''
    i = 0
    for stock_data in api_response['data']:
        data = data + stock_data['name'] + "\n"
        if i == 0:
            symbols = stock_data['symbol']
        if i < 97:
            symbols = symbols + "," + stock_data['symbol']
        i += 1

    params = {
        'access_key': '2b4183b16afefdf531be92c7fe94e413',
        'symbols': symbols
    }

    api_result = requests.get('http://api.marketstack.com/v1/eod/latest', params)

    api_response = api_result.json()

    return data, api_response


class Istok(QtWidgets.QMainWindow):
    def __init__(self):
        super(Istok, self).__init__()
        self.wind = Ui_Istok()
        self.wind.setupUi(self)
        self.initiation()

    def initiation(self):
        self.wind.setupUi(self)
        self.wind.Allcomp.clicked.connect(self.open_Allcomp)
        self.wind.Relevcomp.clicked.connect(self.open_Relevcomp)
        self.wind.Detail.clicked.connect(self.open_Detail)

    def open_Allcomp(self):
        self.dialogAll = Ui_List()
        self.dialogAll.setupUi(self)
        self.dialgAll.Back.clicked.connect(self.backbutton)
        #data, api_response = connection()

        data = "*-*"

        print(data)
        self.dialogAll.textBrowser.setText(data)

    def open_Relevcomp(self):
        self.dialgRelev = Ui_Istok_relevants()
        self.dialgRelev.setupUi(self)
        self.dialgRelev.Back.clicked.connect(self.backbutton)

    def open_Detail(self):
        self.dialgDet = Ui_Favorites()
        self.dialgDet.setupUi(self)
        self.dialgDet.Back.clicked.connect(self.backbutton)

    def backbutton(self):
        self.ininiation()

#
#     def initiation(self):
#         self.tryes = 3
#         self.wind.setupUi(self)
#         try:
#             self.readall()
#         except FileNotFoundError:
#             self.iffileerror()
#             self.readall()
#         except ValueError:
#             self.iffileerror()
#             self.readall()
#         except SyntaxError:
#             self.iffileerror()
#             self.readall()
#         #print("Вход " + str(self.users.items()))
#         for self.user in self.users:
#             if self.users[self.user][5]:
#                 self.wind.Userslist.addItem(self.user)
#
#
#     def entering(self):
#         if self.tryes != 1:
#             if self.wind.Userslist.currentText() == "Admin" and \
#                     self.users[self.wind.Userslist.currentText()][0] == self.wind.Passwordform.text():
#                 self.wind = Ui_Adminmenu_2()
#                 self.wind.show()
#                 self.close()
#
#             elif self.users[self.wind.Userslist.currentText()][0] == self.wind.Passwordform.text():
#                 self.name = self.wind.Userslist.currentText()
#                 self.openuserspacedialog()
#             else:
#                 self.message('Not correct pass, you have ' + str(self.tryes - 1) + ' tryes')
#                 self.tryes = self.tryes - 1
#         else:
#             self.message('A lot of not correct passwords. Good bye!')
#             self.close()
#
#     def openuserspacedialog(self):
#         self.readall()
#         self.dialog = Ui_Userspace()
#         self.dialog.setupUi(self)
#         self.dialog.Username.setText(self.name)
#         self.dialog.Exit.clicked.connect(self.exitbutton)
#         self.dialog.ChangepassButton.clicked.connect(self.opennewpassformdialog)
#         self.checkingpass()
#
#         wmi = win32com.client.GetObject("winmgmts:")
#         for objItem in wmi.InstancesOf("CIM_DiskDrive"):
#             if objItem.Caption != None and objItem.MediaType == "Removable Media":
#                 if objItem.PNPDeviceID not in self.users[self.name][6]:
#                     self.messagetoadmin()
#                 else:
#                     pass
#
#     def opennewpassformdialog(self):
#         self.dialognp = Ui_Newpassform()
#         self.dialognp.setupUi(self)
#         self.dialognp.Back.clicked.connect(self.backtouserspacedialog)
#         self.dialognp.Newpasssubmit.clicked.connect(self.createnewpass)
#
#     def createnewpass(self):
#         self.oldpass = self.dialognp.Olduserpass.text()
#         if self.oldpass == self.users[self.name][0]:
#             self.newpass = self.dialognp.Newuserpass.text()
#             if time.time() - self.users[self.name][1] < self.users[self.name][3]:
#                 self.message('You mast wait ' + str(
#                     self.users[self.name][3] - int(time.time() - self.users[self.name][1])) + ' seconds')
#                 self.backtouserspacedialog()
#             elif self.newpass[len(self.newpass)-1] == ' ':
#                 self.message('The space (" ") can\'t be used as a last symbol of pass')
#             elif len(self.newpass) > 25:
#                 self.message('Max len of all passwords in system is 25')
#             elif len(self.dialognp.Newuserpass.text()) < self.users[self.name][2]:
#                 self.message('Pass is so short, min length is ' + str(self.users[self.name][2]))
#             elif self.users[self.name][4]:
#                 if set(".,:;!_*-+()/#¤%&)").isdisjoint(self.newpass) or \
#                         set("ABCDEFGHIJKLMNOPQRSTUVWXYZ".rstrip()).isdisjoint(self.newpass) or \
#                         set("abcdefghijklmnopqrstuvwxyz").isdisjoint(self.newpass) or \
#                         set("1234567890").isdisjoint(self.newpass):
#                     self.message('You must use special symbols, numbers and letters of different registers')
#                 else:
#                     self.users[self.name][0] = self.newpass
#                     self.users[self.name][1] = time.time()
#                     self.writeall()
#                     self.message('Successful new pass')
#                     self.backtouserspacedialog()
#             else:
#                 self.users[self.name][0] = self.newpass
#                 self.users[self.name][1] = time.time()
#                 self.writeall()
#                 self.message('Successful new pass')
#                 self.backtouserspacedialog()
#         else:
#             self.message('Old pass is not correct')
#
#     def checkingpass(self):
#         if self.users[self.name][4]:
#             if set(".,:;!_*-+()/#¤%&)").isdisjoint(self.users[self.name][0]) or \
#                     set("ABCDEFGHIJKLMNOPQRSTUVWXYZ".rstrip()).isdisjoint(self.users[self.name][0]) or \
#                     set("abcdefghijklmnopqrstuvwxyz").isdisjoint(self.users[self.name][0]) or \
#                     set("1234567890").isdisjoint(self.users[self.name][0]):
#                 self.message('You must use special symbols, numbers and letters of different registers in your pass!')
#                 self.opennewpassformdialog()
#         if len(self.users[self.name][0]) < self.users[self.name][2]:
#             self.message('Your pass is so short, min length is ' + str(self.users[self.name][2]))
#             self.opennewpassformdialog()
#
#     def readall(self):
#         self.users = {}
#         self.f = open('users.txt', 'r')
#         self.users = dict(eval(self.f.readline().rstrip()))
#         self.key = list(eval(self.f.readline().rstrip()))
#         self.f.close()
#         for user in self.users:
#             self.users[user][0] = self.deshifr(self.users[user][0])
#         if len(self.users) < 1:
#             self.iffileerror()
#         #print(self.users.items())
#         #print(self.key)
#
#     def iffileerror(self):
#         self.users = {'Admin': ['Admin', time.time(), 1, 5, False, True, []]}
#         self.key = [25, 13, 1, 19, 7, 16, 9, 22, 15, 3, 12, 5, 18, 6, 24, 8, 21, 14, 2, 20, 4, 17, 10, 23, 11]
#         self.writeall()
#
#     def writeall(self):
#         for user in self.users:
#             self.users[user][0] = self.shifr(self.users[user][0])
#         self.f = open('users.txt', 'w')
#         self.f.write(str(self.users))
#         self.f.write('\n')
#         self.f.write(str(self.key))
#         self.f.close()
#         for user in self.users:
#             self.users[user][0] = self.deshifr(self.users[user][0])
#
#     def backtouserspacedialog(self):
#         if self.name != 'Admin':
#             self.openuserspacedialog()
#
#     def exitbutton(self):
#         self.wind = Ui_Entering()
#         self.initiation()
#         self.wind.Enter.clicked.connect(self.entering)
#
#     def message(self, needstext):
#         error = Error()
#         error.wind.textBrowser.setText(needstext)
#         error.exec_()
#
#     def messagetoadmin(self):
#         if self.name not in self.users['Admin'][6]:
#             self.users['Admin'][6].append(self.name)
#             self.writeall()
#
#     def shifr(self, needs):
#         new = ""
#         for i in range(len(self.key)):
#             if len(needs) < self.key[i]:
#                 new = new + " "
#             else:
#                 new = new + needs[self.key[i]-1]
#         return new
#
#     def deshifr(self, needs):
#         new = ""
#         for i in range(1, len(self.key)+1):
#             new = new + needs[self.key.index(i)]
#         while new[len(new)-1] == " ":
#             new = new[0:len(new)-1]
#         return new
#
# class Ui_Adminmenu_2(Tokb):
#     def __init__(self):
#         super(Ui_Adminmenu_2, self).__init__()
#         self.admin = Ui_Adminmenu()
#         self.initiationad()
#
#     def initiationad(self):
#         self.name = 'Admin'
#         self.user = 'Admin'
#         print(str(self.users.items()))
#         self.readall()
#         self.admin.setupUi(self)  # Инициализация GUI
#         self.admin.NewuserButton.clicked.connect(self.opennewuserformdialog)  # Кнопка New user
#         self.admin.ListofusersButton.clicked.connect(self.openlistofusersdialog)  # Кнопка List of users
#         self.admin.ChangepassButton.clicked.connect(self.opennewpassformdialogad)  # Кнопка Change pass
#         self.admin.MagicsquareButton.clicked.connect(self.openmagicsquaredialogad)
#         self.admin.ChooseoptionsButton.clicked.connect(self.openchooseoptionsformdialog)  # Кнопка Choose options
#         self.admin.AboutButton.clicked.connect(self.about)
#         self.admin.Exit.clicked.connect(self.openexitdialog)  # Кнопка Exit
#         self.checkingpassad()
#         self.badnews()
#         self.readall()
#
#     # дублируем функции пароля для админа чтобы исключить баг мгновенного подтверждения пароля без ожидания времени
#
#     def checkingpassad(self):
#         if self.users[self.name][4]:
#             if set(".,:;!_*-+()/#¤%&)").isdisjoint(self.users[self.name][0]) or \
#                     set("ABCDEFGHIJKLMNOPQRSTUVWXYZ".rstrip()).isdisjoint(self.users[self.name][0]) or \
#                     set("abcdefghijklmnopqrstuvwxyz").isdisjoint(self.users[self.name][0]) or \
#                     set("1234567890").isdisjoint(self.users[self.name][0]):
#                 self.message('You must use special symbols, numbers and letters of different registers in your pass!')
#                 self.opennewpassformdialogad()
#         if len(self.users[self.name][0]) < self.users[self.name][2]:
#             self.message('Your pass is so short, min length is ' + str(self.users[self.name][2]))
#             self.opennewpassformdialogad()
#
#     def opennewpassformdialogad(self):
#         self.dialognp = Ui_Newpassform()
#         self.dialognp.setupUi(self)
#         self.dialognp.Back.clicked.connect(self.backbutton)
#         self.dialognp.Newpasssubmit.clicked.connect(self.createnewpassad)
#
#     def createnewpassad(self):
#         self.oldpass = self.dialognp.Olduserpass.text()
#         if self.oldpass == self.users[self.name][0]:
#             self.newpass = self.dialognp.Newuserpass.text()
#             if time.time() - self.users[self.name][1] < self.users[self.name][3]:
#                 self.message('You mast wait ' + str(
#                     self.users[self.name][3] - int(time.time() - self.users[self.name][1])) + ' seconds')
#                 self.backbutton()
#             elif self.newpass[len(self.newpass)-1] == ' ':
#                 self.message('The space (" ") can\'t be used as a last symbol of pass')
#             elif len(self.newpass) > 25:
#                 self.message('Max len of all passwords in system is 25')
#             elif len(self.dialognp.Newuserpass.text()) < self.users[self.name][2]:
#                 self.message('Pass is so short, min length is ' + str(self.users[self.name][2]))
#             elif self.users[self.name][4]:
#                 if set(".,:;!_*-+()/#¤%&)").isdisjoint(self.newpass) or \
#                         set("ABCDEFGHIJKLMNOPQRSTUVWXYZ".rstrip()).isdisjoint(self.newpass) or \
#                         set("abcdefghijklmnopqrstuvwxyz").isdisjoint(self.newpass) or \
#                         set("1234567890").isdisjoint(self.newpass):
#                     self.message('You must use special symbols, numbers and letters of different registers')
#                 else:
#                     self.users[self.name][0] = self.newpass
#                     self.users[self.name][1] = time.time()
#                     self.writeall()
#                     self.message('Successful new pass')
#                     self.backbutton()
#             else:
#                 self.users[self.name][0] = self.newpass
#                 self.users[self.name][1] = time.time()
#                 self.writeall()
#                 self.message('Successful new pass')
#                 self.backbutton()
#         else:
#             self.message('Old pass is not correct')
#
#     def opennewuserformdialog(self):
#         self.dialognu = Ui_Newuserform()
#         self.dialognu.setupUi(self)
#         self.dialognu.Back.clicked.connect(self.backbutton)
#         self.dialognu.Newusersubmit.clicked.connect(self.newusersubmit)
#
#     def newusersubmit(self):
#         if self.dialognu.Newusername.text() in self.users:
#             self.message('You are already have this user')
#         elif self.dialognu.Newusername.text() == '':
#             self.message('The field is empty')
#         elif self.dialognu.Newusername.text().isspace():
#             self.message('The field is only spaces')
#         else:
#             self.users.update({self.dialognu.Newusername.text(): ["Qwerty1", time.time(), 1, 5, False, True, []]})
#             self.writeall()
#             self.message('User \"' + self.dialognu.Newusername.text() + '\" is created')
#             self.backbutton()
#
#     def openlistofusersdialog(self):
#         self.readall()
#         self.ables = {}
#         self.dialog = Ui_Listofusers()
#         self.dialog.setupUi(self)
#         r = 0
#         for self.user in self.users:
#             if self.user == 'Admin':
#                 pass
#             else:
#                 if self.users[self.user][5]:
#                     self.dialog.Userslist.addItem(self.user)
#                 else:
#                     self.dialog.Userslist.addItem(self.user + ' (Disabled)')
#                 self.ables.update({r: self.user})
#                 r = r + 1
#         self.dialog.deleteuserButton.clicked.connect(self.deletinguser)
#         self.dialog.Options.clicked.connect(self.usersoptions)
#         self.dialog.Back.clicked.connect(self.backbutton)
#         self.dialog.USB.clicked.connect(self.usbdialog)
#
#     def usersoptions(self):
#         if self.dialog.Userslist.count() < 1:
#             self.message('List of users is empty')
#         else:
#             self.user = self.ables[self.dialog.Userslist.currentIndex()]
#             self.openchooseoptionsformdialog()
#
#     def usbdialog(self):
#         if self.dialog.Userslist.count() < 1:
#             self.message('List of users is empty')
#         else:
#             self.user = self.ables[self.dialog.Userslist.currentIndex()]
#             self.userusb = UsbAccess()
#             r = 0
#             self.ablesusb = {}
#             wmi = win32com.client.GetObject("winmgmts:")
#             for objItem in wmi.InstancesOf("CIM_DiskDrive"):
#                 if objItem.Caption != None and objItem.MediaType == "Removable Media":
#                     if objItem.PNPDeviceID not in self.users[self.user][6]:
#                         self.userusb.wind.USBlist.addItem(objItem.Caption)
#                     else:
#                         self.userusb.wind.USBlist.addItem("(✔)" + objItem.Caption)
#                     self.ablesusb.update({r: objItem})
#                     r = r + 1
#
#             self.userusb.wind.Back.clicked.connect(self.usbclose)
#             self.userusb.wind.GiveaccessButton.clicked.connect(self.usbaccess)
#             self.userusb.wind.DenyaccessButton.clicked.connect(self.usbdenya)
#             self.userusb.exec_()
#
#
#     def usbaccess(self):
#         if  self.userusb.wind.USBlist.count() < 1:
#             self.message('List of users is empty')
#         else:
#             self.selectedusb = self.ablesusb[self.userusb.wind.USBlist.currentIndex()]
#             if self.selectedusb.PNPDeviceID not in self.users[self.user][6]:
#                 self.users[self.user][6].append(self.selectedusb.PNPDeviceID)
#                 self.writeall()
#                 self.usbclose()
#                 self.usbdialog()
#
#     def usbdenya(self):
#         if  self.userusb.wind.USBlist.count() < 1:
#             self.message('List of users is empty')
#         else:
#             self.selectedusb = self.ablesusb[self.userusb.wind.USBlist.currentIndex()]
#             if self.selectedusb.PNPDeviceID in self.users[self.user][6]:
#                 self.users[self.user][6].pop(self.users[self.user][6].index(self.selectedusb.PNPDeviceID))
#                 self.writeall()
#                 self.usbclose()
#                 self.usbdialog()
#
#     def usbclose(self):
#         self.userusb.close()
#
#     def deletinguser(self):
#         if self.dialog.Userslist.count() < 1:
#             self.message('List of users is empty')
#         else:
#             self.user = self.ables[self.dialog.Userslist.currentIndex()]
#             if self.user == 'Admin':
#                 self.message('Admin can\'t be deleted!')
#             else:
#                 self.users.pop(self.user)
#                 self.writeall()
#                 self.message('User \"' + self.user + '\" deleted')
#                 self.openlistofusersdialog()
#
#     def openmagicsquaredialogad(self):
#         self.dialogms = Ui_MagicSquare()
#         self.dialogms.setupUi(self)
#         for i in range(1, 26):
#             nn = 'No_' + str(i)
#             exec("self.dialogms." + nn + ".setValue(self.key[" + str(i-1) + "])")
#         self.dialogms.Submit.clicked.connect(self.submitms)
#
#     def submitms(self):
#         sumleft = self.dialogms.No_1.value()+self.dialogms.No_7.value()+self.dialogms.No_13.value()+self.dialogms.No_19.value()+self.dialogms.No_25.value()
#         sumright = self.dialogms.No_5.value()+self.dialogms.No_9.value()+self.dialogms.No_13.value()+self.dialogms.No_17.value()+self.dialogms.No_21.value()
#         stroks = [0, 0, 0, 0, 0]
#         stolbs = [0, 0, 0, 0, 0]
#         vrem = 1
#         for i in range(5):
#             for j in range(5):
#                 nn = 'No_' + str(vrem)
#                 vrem = vrem + 1
#                 exec("stroks[" + str(i) + "] = stroks[" + str(i) + "] + self.dialogms." + nn + ".value()")
#         vrem = 1
#         for i in range(5):
#             for j in range(5):
#                 nn = 'No_' + str(vrem)
#                 vrem = vrem + 5
#                 exec("stolbs[" + str(i) + "] = stolbs[" + str(i) + "] + self.dialogms." + nn + ".value()")
#             vrem = (vrem % 25) + 1
#         itog = True
#         for i in stroks:
#             if i != 65:
#                 itog = False
#         for i in stolbs:
#             if i != 65:
#                 itog = False
#         if (sumleft != 65) or (sumright != 65):
#             itog = False
#         vrem=[]
#         for i in range(1, 26):
#             nn = 'No_' + str(i)
#             exec("vrem.append(self.dialogms." + nn + ".value())")
#         vvrem = set(vrem)
#         if len(vrem) != len(vvrem):
#             itog = False
#         if itog:
#             for i in range(1, 26):
#                 nn = 'No_' + str(i)
#                 exec("self.key[" + str(i - 1) + "] = self.dialogms." + nn + ".value()")
#             self.writeall()
#             self.backbutton()
#         else:
#             print('It\'s not magic square')
#
#
#     def openchooseoptionsformdialog(self):
#         self.dialogop = Ui_Chooseoptionsform()
#         self.dialogop.setupUi(self)
#         self.dialogop.Mindlin.setValue(self.users[self.user][2])
#         self.dialogop.Mindlin.setMaximum(25)
#         self.dialogop.Mintime.setValue(self.users[self.user][3])
#         self.dialogop.checsimvol.setChecked(self.users[self.user][4])
#         self.dialogop.Submit.clicked.connect(self.submitoptions)
#         self.dialogop.Activate.clicked.connect(self.activation)
#         self.dialogop.Deactivate.clicked.connect(self.deactivation)
#
#     def activation(self):
#         self.users[self.user][5] = True
#         self.writeall()
#         self.backbutton()
#
#     def deactivation(self):
#         if self.user == 'Admin':
#             self.message('Admin can\'t be deactivated!')
#         else:
#             self.users[self.user][5] = False
#             self.writeall()
#         self.backbutton()
#
#     def submitoptions(self):
#         self.users[self.user][2] = self.dialogop.Mindlin.value()
#         self.users[self.user][3] = self.dialogop.Mintime.value()
#         self.users[self.user][4] = self.dialogop.checsimvol.isChecked()
#         self.writeall()
#         self.backbutton()
#
#     def about(self):
#         self.message('Created by student Danila Urvantsev')
#
#     def openexitdialog(self):
#         self.admin = Tokb()
#         self.admin.show()
#         self.close()
#
#     def backbutton(self):
#         self.initiationad()
#
#     def badnews(self):
#         badguys = ""
#         if len(self.users[self.user][6]) != 0:
#             for i in self.users[self.user][6]:
#                 badguys = badguys + ' ' + i
#             self.message(badguys + ' tried get access to the USB')
#         self.users[self.user][6] = []
#         self.writeall()
#
#
# class Error(QtWidgets.QDialog):
#     def __init__(self):
#         super(Error, self).__init__()
#         self.wind = Ui_Outputform()
#         self.wind.setupUi(self)
#         self.wind.textBrowser.setText('-*-')

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Istok()
    window.show()
    app.exec_()
