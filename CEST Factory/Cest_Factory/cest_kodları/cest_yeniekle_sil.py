'''
Created on 9 Şub 2021

@author: user
'''
from PyQt5.QtWidgets import QDialog, QLabel, QHBoxLayout, QComboBox, QLineEdit,\
    QFormLayout, QPushButton, QVBoxLayout, QMessageBox, QApplication
from PyQt5.QtGui import QPixmap, QFont
import os
from Cest_Factory.cest_kodları.cest_kodu_helper import cest_kodları_record

class cest_yenieklesil_gui(QDialog):
    '''
    classdocs
    '''


    def __init__(self, anapencere, eklesil,*,rowNo=0):
        '''
        Constructor
        '''
        super().__init__()
        self.anapencere = anapencere
        #self.rowNo = index.row()
        self.eklesil = eklesil
        self.rowNo = rowNo
        
        self.changeTexts()
        self.bilgileriAl()
        self.UIoluştur()
        self.dialogMoveCenter()
        self.setStyleSheet("QLabel[field=true] {font-weight: bold; " + 
                           self.başlıkcsstext + " }")
        self.show()
        
    def changeTexts(self):
        
        if self.eklesil == 'ekle':
            self.windowtitletext = "Yeni Kayıt Oluştur - Cest Stok Kodları"
            self.başlıkLabeltext = ("Cest Stok Kodları Tablosunda\n" +
                                    "Yeni Kayıt Oluştur")
            self.başlıkcsstext = 'color: blue;'
            self.kaydetsilbtntext = "Yeni Kayıt Oluştur"
            
        elif self.eklesil == 'sil':
            self.windowtitletext = "Kayıt Sil - Cest Stok Kodları"
            self.başlıkLabeltext = ("Cest Stok Kodları Tablosundan\n" +
                                    "Kayıt Sil")
            self.başlıkcsstext = 'color: tomato;'
            self.kaydetsilbtntext = "Kayıt Sil"
            
        elif self.eklesil == 'kaydısil':
            self.windowtitletext = 'Kaydı Sil - Cest Stok Kodları'
            self.başlıkLabeltext = ("Cest Stok Kodları Tablosundan\n" +
                                    "Kayıt Sil")
            self.başlıkcsstext = 'color: tomato;'
            self.kaydetsilbtntext = "Kaydı Sil"
        else:
            print(__name__,":Hatalı ekle/sil parametresi girilmiş !!!")
            return self.done(QDialog.Rejected)
        
    def bilgileriAl(self):
        cmd = "SELECT Tip_Adı FROM malzeme_tipleri"
        msg = self.anapencere.stok_dbm.executeCmd(cmd)
        self.malzeme_tipleri = [x[0] for x in msg]
        
        cmd = "SELECT tip_kodu_adı FROM tip_kodlari"
        msg = self.anapencere.stok_dbm.executeCmd(cmd)
        self.tip_kodlari = [x[0] for x in msg] #Çok Fazla Sayıda İse ??
        
        cmd = "SELECT Cest_Stok_Kodu FROM cest_stok_kodları"
        msg = self.anapencere.stok_dbm.executeCmd(cmd)
        self.cest_kodlari = [x[0] for x in msg] 

#         cmd = "SHOW COLUMNS FROM standart_malzemeler"
#         msg = self.anapencere.stok_dbm.executeCmd(cmd)
#         self.colnames = [x[0] for x in msg]

        if self.eklesil == 'kaydısil':
            rowdata = self.anapencere.tableView_Model.sqldata[self.rowNo]
            print("Alınan satır bilgisi:",rowdata)
            self.myrecord = cest_kodları_record(self.anapencere)
            self.myrecord.setfromtablerowdata(rowdata)
        
    def UIoluştur(self):
        
        self.setGeometry(100,100,600,300)
        self.setModal(True)
        self.setWindowTitle(self.windowtitletext)
        
        self.cestKoduProper = True
        self.tipKoduProper = True
        self.tipproper = True
        
        def başlıksection():
            resim = QLabel()
            resim.setMaximumHeight(100)
            path = os.path.join('images','CestIcon.png')
            pic = QPixmap(path)
            resim.setPixmap(pic)
            
            self.başlıkLabel = QLabel(self.başlıkLabeltext)
            self.başlıkLabel.setStyleSheet(self.başlıkcsstext)
            self.başlıkLabel.setFont(QFont('Arial', 12,QFont.Bold))
            
            başlıkhbox = QHBoxLayout()
            başlıkhbox.addWidget(resim)
            başlıkhbox.addStretch()
            başlıkhbox.addWidget(self.başlıkLabel)
            başlıkhbox.addStretch()
            return başlıkhbox

        def fieldssection():
            
            self.Cest_Kodu = QLineEdit()
            self.Cest_Kodu.textChanged.connect(
                lambda text: self.CestKoduCheckSlot(text)
                )
            self.Cest_Kodu.textChanged.connect(self.btnsetEnable)
            
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
            self.Açıklama = QLineEdit()
                
            section = QFormLayout()
            if self.eklesil == 'ekle':
                section.addRow(QLabel("Cest Kodu:"), self.Cest_Kodu)
                section.addRow(QLabel("Malzeme Tipi:"), self.Tipi)
                section.addRow(QLabel("Malzeme Tip Kodu:"), self.Tip_Kodu)
                section.addRow(QLabel("Malzeme Boyutları:"), self.Boyutlar)
                section.addRow(QLabel("Açıklama:"), self.Açıklama)
            elif self.eklesil == 'sil':
                section.addRow(QLabel("Cest Kodu:"), self.Cest_Kodu)
            elif self.eklesil == 'kaydısil':
                self.Cest_KoduLabel = QLabel(self.myrecord.Cest_Stok_Kodu)
                self.Cest_KoduLabel.setProperty("field", True)
                self.TipiLabel = QLabel(self.myrecord.Tipi)
                self.TipiLabel.setProperty("field", True)
                self.Tip_KoduLabel = QLabel(self.myrecord.Tip_Kodu)
                self.Tip_KoduLabel.setProperty("field", True)
                self.BoyutlarLabel = QLabel(self.myrecord.Boyutlar)
                self.BoyutlarLabel.setProperty("field", True)
                self.AçıklamaLabel = QLabel(self.myrecord.Açıklama)
                self.AçıklamaLabel.setProperty("field", True)
                section.addRow(QLabel("Cest Kodu:"), self.Cest_KoduLabel)
                section.addRow(QLabel("Malzeme Tipi:"), self.TipiLabel)
                section.addRow(QLabel("Malzeme Tip Kodu:"), self.Tip_KoduLabel)
                section.addRow(QLabel("Malzeme Boyutları:"), self.BoyutlarLabel)
                section.addRow(QLabel("Açıklama:"), self.AçıklamaLabel)
            return section
        
        def buttonsection():
            iptalbtn = QPushButton("İptal")
            iptalbtn.setDefault(True)
            iptalbtn.clicked.connect(self.iptalbtn_call)
            self.kaydetsilbtn = QPushButton(self.kaydetsilbtntext)
            self.kaydetsilbtn.clicked.connect(self.kaydetbtn_call)
            
            if self.eklesil in ('ekle','sil'):
                self.kaydetsilbtn.setEnabled(False)
            elif self.eklesil == 'kaydısil':
                self.kaydetsilbtn.setEnabled(True)
            
            section = QHBoxLayout()
            section.addStretch()
            section.addWidget(iptalbtn)
            section.addWidget(self.kaydetsilbtn)
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
        
        if self.eklesil == 'ekle':
            self.myrecord = cest_kodları_record(self.anapencere,
                                                Cest_Stok_Kodu=self.Cest_Kodu.text(),
                                                Tipi=self.Tipi.currentText(),
                                                Tip_Kodu=self.Tip_Kodu.text(),
                                                Boyutlar=self.Boyutlar.text(),
                                                Açıklama=self.Açıklama.text()
                                                )
            matching = self.myrecord.checkformatchingrecord()
            if not matching[0]:
                self.myrecord.insertinto_table()
                return self.done(QDialog.Accepted)
            else:
                self.error_msgbox("Bu özelliklerde Cest Kodu daha önce verilmiş.")
                return 
        if self.eklesil == 'sil':
            self.myrecord = cest_kodları_record(self.anapencere,
                                                Cest_Stok_Kodu=self.Cest_Kodu.text(),
                                                Tipi=self.Tipi.currentText(),
                                                Tip_Kodu=self.Tip_Kodu.text(),
                                                Boyutlar=self.Boyutlar.text(),
                                                Açıklama=self.Açıklama.text()
                                                )
            matching = self.myrecord.checkformatchingCestKodurecord()
            if matching[0]:
                self.myrecord.record_id = matching[1]
                self.myrecord.delete_tablerecord()
                return self.done(QDialog.Accepted)
            else:
                self.error_msgbox("Bu Cest Kodu bulunamadı")
                return
            
        if self.eklesil == 'kaydısil':
            matching = self.myrecord.checkformatchingCestKodurecord()
            if matching[0]:
                self.myrecord.record_id = matching[1]
                self.myrecord.delete_tablerecord()
                return self.done(QDialog.Accepted)
            else:
                self.error_msgbox("Bu Cest Kodu bulunamadı")
                return

#         return self.done(QDialog.Rejected)
                
    def dialogMoveCenter(self):
        screenCenter=QApplication.desktop().availableGeometry().center()
        myrect=self.frameGeometry()
        myrect.moveCenter(screenCenter)
        self.move(myrect.topLeft())


    def CestKoduCheckSlot(self,text):
        text = text.strip()
        text = text.upper()
        text = text.replace('İ','I')
        self.Cest_Kodu.setText(text)
        if not text:
            self.msgLabel.setText('Cest Kodu Boş Bırakılamaz')
            self.cestKoduProper = False
            return
        if self.eklesil == 'ekle':
            if text in self.cest_kodlari:
                self.msgLabel.setText("'" + text + "'"
                                       " Kaydı Zaten Var")
                self.cestKoduProper = False
            else:
                self.msgLabel.setText('')
                self.cestKoduProper = True
        if self.eklesil == 'sil':
            if text not in self.cest_kodlari:
                self.msgLabel.setText("'" + text + "'"
                                       " Bulunamadı")
                self.cestKoduProper = False
            else:
                self.msgLabel.setText('')
                self.cestKoduProper = True
        
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
        condition = (self.tipKoduProper and
                     self.cestKoduProper and
                     self.tipproper)
        if condition:
            self.kaydetsilbtn.setEnabled(True)
        else:
            self.kaydetsilbtn.setEnabled(False)
        
    
    def error_msgbox(self,errortext):
        msgbox = QMessageBox() 
        msgbox.setIcon(QMessageBox.Critical)
        msgbox.setWindowTitle("Hata")
        msgbox.setText(errortext)
        msgbox.setStandardButtons(QMessageBox.Ok)
        return msgbox.exec_()
