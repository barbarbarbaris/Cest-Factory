'''
Created on 30 Oca 2021

@author: user
'''
from PyQt5.QtWidgets import QLabel, QLineEdit, QDialog, QHBoxLayout, QFormLayout,\
    QPushButton, QVBoxLayout, QApplication, QComboBox
from PyQt5.QtGui import QFont, QPixmap
import os


class standart_malzemeler_view_edit_gui(QDialog):
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
        
        self.stokBölgesiKoduProper = True
        self.tipKoduProper = True
        self.adetproper = False
        self.tipproper = True

        self.bilgileriAl()
        self.dialogUIoluştur()
        print("dialog ui sonrası")
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
        
    def dialogUIoluştur(self):
        
        self.setGeometry(100,100,600,400)
        self.setModal(True)
        
        self.setWindowTitle("Standart Malzemeler")
        
        def başlıksection():
            resim = QLabel()
            resim.setMaximumHeight(100)
            path = os.path.join('images','letter_S_blue.png')
            pic = QPixmap(path)
            resim.setPixmap(pic)
            
            self.başlıkLabel = QLabel("Standart Malzemeler")
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
        self.done(QDialog.Accepted)
        
    def dialogMoveCenter(self):
        screenCenter=QApplication.desktop().availableGeometry().center()
        myrect=self.frameGeometry()
        myrect.moveCenter(screenCenter)
        self.move(myrect.topLeft())

    
    def stokBölgesiKoduCheckSlot(self,text):
            text = text.strip()
            text = text.upper()
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
            
    def btnsetEnable(self):
        print("btnset enable girişşşşşşşşşşşş")
        if (self.tipKoduProper and
                self.stokBölgesiKoduProper and
                self.adetproper and 
                self.tipproper and 
                self.Adet.text()
                ):
            self.kaydetbtn.setEnabled(True)
        else:
            self.kaydetbtn.setEnabled(False)
        

    def hellorilerdengel(self):
        print("Ule hellorilerden gelirem uleeeooo")
        print("ule ule uleeeee")
        print("ulan alla laaaa")