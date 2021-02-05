'''
Created on 30 Oca 2021

@author: user
'''
from PyQt5.QtWidgets import QLabel, QLineEdit, QDialog, QHBoxLayout, QFormLayout,\
    QPushButton, QVBoxLayout, QApplication, QComboBox, QMessageBox
from PyQt5.QtGui import QFont, QPixmap
import os


class standart_malzemeler_gui(QDialog):
    '''
    classdocs
    '''

    def __init__(self, anapencere):
        '''
        Constructor
        '''
        super().__init__()
        self.anapencere = anapencere
        #self.rowNo = index.row()
        

        self.bilgileriAl()
        self.yeni_kayıt_ekle_UI()
        self.dialogMoveCenter()
        self.show()
        
    def bilgileriAl(self):
        cmd = "SELECT Tip_Adı FROM malzeme_tipleri"
        msg = self.anapencere.stok_dbm.executeCmd(cmd)
        self.malzeme_tipleri = [x[0] for x in msg]
        
        cmd = "SELECT tip_kodu_adı FROM tip_kodlari"
        msg = self.anapencere.stok_dbm.executeCmd(cmd)
        self.tip_kodlari = [x[0] for x in msg] #Çok Fazla Sayıda İse ??
        
        cmd = "SELECT stok_bölgesi_kodu FROM stok_bölgesi_kodlari"
        msg = self.anapencere.stok_dbm.executeCmd(cmd)
        self.stok_bölgesi_kodlari = [x[0] for x in msg] #Çok Fazla Sayıda İse ??
        
#         cmd = "SHOW COLUMNS FROM standart_malzemeler"
#         msg = self.anapencere.stok_dbm.executeCmd(cmd)
#         self.colnames = [x[0] for x in msg]
        
    def yeni_kayıt_ekle_UI(self):
        
        self.setGeometry(100,100,600,300)
        self.setModal(True)
        self.setWindowTitle("Ekle - Standart Malzemeler")
        
        self.stokBölgesiKoduProper = True
        self.tipKoduProper = True
        self.adetproper = False
        self.tipproper = True
        
        def başlıksection():
            resim = QLabel()
            resim.setMaximumHeight(100)
            path = os.path.join('images','letter_S_blue.png')
            pic = QPixmap(path)
            resim.setPixmap(pic)
            
            self.başlıkLabel = QLabel("Standart Malzemeler Tablosuna\nEkle")
            self.başlıkLabel.setStyleSheet('color: blue;')
            self.başlıkLabel.setFont(QFont('Arial', 12,QFont.Bold))
            
            başlıkhbox = QHBoxLayout()
            başlıkhbox.addWidget(resim)
            başlıkhbox.addStretch()
            başlıkhbox.addWidget(self.başlıkLabel)
            başlıkhbox.addStretch()
            return başlıkhbox

        def fieldssection():
            self.Tipi = QComboBox()
            self.Tipi.addItems(self.malzeme_tipleri)
            self.Tipi.currentTextChanged.connect(
                lambda text: self.tipcheckslot(text)
                )
            self.Tipi.currentTextChanged.connect(self.btnsetEnable)
            
            self.Tip_Kodu = QLineEdit()
            self.Tip_Kodu.textChanged.connect(
                lambda text: self.TipKoduCheckSlot(text)
                )
            self.Tip_Kodu.textChanged.connect(self.btnsetEnable)
            
            self.Boyutlar = QLineEdit()
            self.Boyutlar.textChanged.connect(
                lambda text: self.boyutlarslot(text)
                )
            
            self.Adet = QLineEdit()
            self.Adet.textChanged.connect(
                lambda text: self.AdetCheckSlot(text)
                )
            self.Adet.textChanged.connect(self.btnsetEnable)
            
            self.Stok_Bölgesi = QLineEdit()
            self.Stok_Bölgesi.textChanged.connect(
                lambda text: self.stokBölgesiKoduCheckSlot(text)
                )
            self.Stok_Bölgesi.textChanged.connect(self.btnsetEnable)
                
            section = QFormLayout()
            section.addRow(QLabel("Malzeme Tipi:"), self.Tipi)
            section.addRow(QLabel("Malzeme Tip Kodu:"), self.Tip_Kodu)
            section.addRow(QLabel("Malzeme Boyutları:"), self.Boyutlar)
            section.addRow(QLabel("Adet:"), self.Adet)
            section.addRow(QLabel("Stok Bölgesi Kodu:"), self.Stok_Bölgesi)
            return section

        
        def buttonsection():
            iptalbtn = QPushButton("İptal")
            iptalbtn.setDefault(True)
            iptalbtn.clicked.connect(self.iptalbtn_call)
            self.kaydetbtn = QPushButton("Kaydet")
            self.kaydetbtn.clicked.connect(self.kaydetbtn_call)
            self.kaydetbtn.setEnabled(False)
            
            section = QHBoxLayout()
            section.addStretch()
            section.addWidget(iptalbtn)
            section.addWidget(self.kaydetbtn)
            return section

        self.msgLabel = QLabel("")
        self.msgLabel.setStyleSheet('color: red;')
        
        mainvboxlayout = QVBoxLayout()
        self.setLayout(mainvboxlayout)
        
        mainvboxlayout.addLayout(başlıksection())
        mainvboxlayout.addSpacing(10)
        mainvboxlayout.addLayout(fieldssection())
        mainvboxlayout.addSpacing(10)
        mainvboxlayout.addWidget(self.msgLabel)
        mainvboxlayout.addStretch()
        mainvboxlayout.addLayout(buttonsection())

    def iptalbtn_call(self):
        self.done(QDialog.Rejected)
    
    def kaydetbtn_call(self):
        matching = self.checkformatchingrecord()
        if not matching[0]:
            self.insertnewrecord()
            self.done(QDialog.Accepted)
        else:
            üzerine_ekle = self.üzerine_ekle_msgbox(matching)
            if üzerine_ekle ==  QMessageBox.Yes:
                newadet = matching[2] + int(self.Adet.text())
                record_id = matching[1]
                self.update_adet_of_record(newadet, record_id)
                return self.done(QDialog.Accepted)
            elif üzerine_ekle == QMessageBox.No:
                return self.done(QDialog.Rejected)
        return self.done(QDialog.Rejected)
                
    def dialogMoveCenter(self):
        screenCenter=QApplication.desktop().availableGeometry().center()
        myrect=self.frameGeometry()
        myrect.moveCenter(screenCenter)
        self.move(myrect.topLeft())

    
    def stokBölgesiKoduCheckSlot(self,text):
        text = text.strip()
        text = text.upper()
        text = text.replace('İ','I')
        self.Stok_Bölgesi.setText(text)
        if not text:
            self.msgLabel.setText('')
            self.stokBölgesiKoduProper = False

        elif text in self.stok_bölgesi_kodlari:
            self.msgLabel.setText('')
            self.stokBölgesiKoduProper = True
            
        else:
            self.msgLabel.setText("'" + text + "'"
                                   " Stok Bölgesi Kodu Bulunamadı")
            self.stokBölgesiKoduProper = False
                
        
    def TipKoduCheckSlot(self,text):
        text = text.strip()
        text = text.upper()
        text = text.replace('İ','I')
        self.Tip_Kodu.setText(text)
        if text and text not in self.tip_kodlari:
            self.msgLabel.setText("'" + text + "'"
                                   " Tip Kodu Bulunamadı")
            self.tipKoduProper = False
        else:
            self.msgLabel.setText('')
            self.tipKoduProper = True
            
    def AdetCheckSlot(self,text):
        text = text.strip()
        if not text:
            self.msgLabel.setText("Adet Boş Bırakılamaz !")
            self.adetproper = False
        else:
            try:
                int(text)
                self.msgLabel.setText("")
                self.adetproper = True
            except:
                self.msgLabel.setText("Sayı girişi yanlış !")
                self.adetproper = False
                return
            
    def tipcheckslot(self,text):
        if not text:
            self.msgLabel.setText("Malzeme Tipi Boş Bırakılamaz !")
            self.tipproper = False
        elif text not in self.malzeme_tipleri:
            self.msgLabel.setText("Malzeme Tipi Bulunamadı !")
            self.tipproper = False
        else:
            self.msgLabel.setText("")
            self.tipproper = True
            
    def boyutlarslot(self,text):
        text = text.strip()
        text = text.upper()
        text = text.replace('İ','I')
        self.Boyutlar.setText(text)
            
    def btnsetEnable(self):
        if (self.tipKoduProper and
                self.stokBölgesiKoduProper and
                self.adetproper and 
                self.tipproper and 
                self.Adet.text()
                ):
            self.kaydetbtn.setEnabled(True)
        else:
            self.kaydetbtn.setEnabled(False)
            
    def checkformatchingrecord(self):
        #returns (match,matching_id,matching_records_Adet)
        
        cmd = ("SELECT idstandart_malzemeler,Adet " +
               "FROM standart_malzemeler WHERE " +
               "Tipi " + self.fieldSQLcondition(self.Tipi.currentText()) + " AND " +
               "Tip_Kodu " + self.fieldSQLcondition(self.Tip_Kodu.text()) + " AND " +
               "Boyutlar " + self.fieldSQLcondition(self.Boyutlar.text()) + " AND " +
               "Stok_Bölgesi " + self.fieldSQLcondition(self.Stok_Bölgesi.text()) + ";"
               )
        msg = self.anapencere.stok_dbm.executeCmd(cmd)
        print(msg)
        if msg:
            return (True,msg[0][0],msg[0][1])
        else:
            return (False,0,0)
    
    def insertnewrecord(self):
        cmd = ("INSERT INTO standart_malzemeler " +
               "(Tipi,Tip_Kodu,Boyutlar,Adet,Stok_Bölgesi) " +
               "VALUES (" + self.fieldSQLtext(self.Tipi.currentText()) + "," +
               self.fieldSQLtext(self.Tip_Kodu.text()) + "," +
               self.fieldSQLtext(self.Boyutlar.text()) + "," +
               self.fieldSQLtext(self.Adet.text()) + "," +
               self.fieldSQLtext(self.Stok_Bölgesi.text()) + ");"
               )
        self.anapencere.stok_dbm.executeCmd(cmd)
        self.anapencere.tableView_Model.setTable("standart_malzemeler")  # for tableview refresh
        
    def update_adet_of_record(self,newadet,record_id):
        cmd = ("UPDATE standart_malzemeler " +
               "SET Adet = {} ".format(newadet) +
               "WHERE idstandart_malzemeler = {}".format(record_id)
               )
        print(cmd)
        self.anapencere.stok_dbm.executeCmd(cmd)
        self.anapencere.tableView_Model.setTable("standart_malzemeler")  # for tableview refresh
        self.anapencere.tableView_Model.setYellowRowFromIdColumnValue(record_id)
        
    def üzerine_ekle_msgbox(self,matching):
        msgbox = QMessageBox()
        msgbox.setIcon(QMessageBox.Question)
        msgbox.setWindowTitle("Malzeme Bulundu")
        msgbox.setText(self.Stok_Bölgesi.text() +
                       " Bölgesinde bu malzemeden " +
                       str(matching[2]) +
                       " Adet bulundu")
        msgbox.setInformativeText("Üzerine " + 
                               self.Adet.text() +
                               " Adet eklemek istiyor musunuz?")
        msgbox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        return msgbox.exec_()
            
    def fieldSQLtext(self,text):
        if text:
            return "'" + text + "'"
        else:
            return 'NULL'
        
    def fieldSQLcondition(self,text):
        if text:
            return "='" + text + "'"
        else:
            return "IS NULL"
        
    def hellorilerdengel(self):
        print("Ule hellorilerden gelirem uleeeooo")
        print("ule ule uleeeee")
        print("ulan alla laaaa")