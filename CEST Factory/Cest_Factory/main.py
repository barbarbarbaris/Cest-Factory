'''
Created on 24 Kas 2020

@author: Barış Kılıçlar
'''
import sys,os

from PyQt5.QtWidgets import QMainWindow,QApplication, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon,QStandardItem

from Cest_Factory.Cest_UI import ui_oluştur,usernamepassDialogOluştur
from Cest_Factory.Cest_Factory_classes import barDBManager


class anaPencere(QMainWindow):
    def __init__(self):
        super().__init__()
        self.anaPencereAyarla()
#         self.doAuthentication()
        self.dontAuthentication()
        ui_oluştur(self)
        self.show()
        
    def anaPencereAyarla(self):
        self.setWindowTitle("Cest İşletme")
        self.setGeometry(100,100,1000,600)
        screenCenter=QApplication.desktop().availableGeometry().center()
        myrect=self.frameGeometry()
        myrect.moveCenter(screenCenter)
        self.move(myrect.topLeft())
            

            
    def closeEvent(self, *args, **kwargs):
        super(QMainWindow, self).closeEvent(*args, **kwargs)
        self.stok_dbm.cursor.commit()
        print("PENCERE Kapandı...")
        #........  YAZ YAZ YAZ -> stok.dbm connection close
    
    def dbmanagerile_userAuthentication(self):        
        self.stok_dbm = barDBManager("cest_stok")
        result = self.stok_dbm.connect("admin", "admin", "localhost")
        if result == -1:
            QMessageBox.information(self,"Uyarı",
                                "Database server bağlantı hatası",
                                 QMessageBox.Ok)
            sys.exit(1)
        cmd = ("SELECT * FROM kullanıcılar " +
               "WHERE Kullanıcı_Adı = '{}' AND ".format(self.username) +
               "Şifre = '{}'".format(self.userpw) 
               )
        msg =self.stok_dbm.executeCmd(cmd)
        #print(msg)
        if not msg:
            QMessageBox.warning(self,"Uyarı",
                    " Kullanıcı adı veya şifre hatalı !!", 
                    QMessageBox.Ok)
            return False
        else:
            self.yetki = msg[0][3].split(',')
            #print(self.yetki)
            return True

    def doAuthentication(self):
        while True:
            result = usernamepassDialogOluştur(self)
            #print(result)
            if not result:
                if hasattr(self, 'stok_dbm'):
                    self.stok_dbm.çıkış()
                sys.exit(1)
            if self.dbmanagerile_userAuthentication():
                break
            
    def dontAuthentication(self):
        self.username = 'barış'
        self.userpw = '19216818'
        self.dbmanagerile_userAuthentication()
        
        
if __name__ == '__main__':
    uygulama = QApplication(sys.argv)
    işlem = anaPencere()
    sys.exit(uygulama.exec_())
