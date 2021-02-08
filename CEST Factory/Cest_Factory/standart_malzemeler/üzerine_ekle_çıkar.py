'''
Created on 5 Şub 2021

@author: user
'''
from PyQt5.QtWidgets import QDialog, QLabel, QHBoxLayout, QLineEdit, QFormLayout,\
    QPushButton, QVBoxLayout, QApplication, QMessageBox
from PyQt5.QtGui import QPixmap, QFont
import os
from Cest_Factory.standart_malzemeler.helper import standart_malzemeler_record

class uzerine_ekle_cikar_gui(QDialog):
    '''
    classdocs
    '''


    def __init__(self, anapencere,rowNo,ekleçıkar):
        '''
        Constructor
        '''
        super().__init__()
        self.anapencere = anapencere
        self.rowNo = rowNo
        self.ekleçıkar = ekleçıkar
        
        self.changeTexts()
        self.bilgileriAl()
        self.UIoluştur()
        self.dialogMoveCenter()
        self.setStyleSheet("QLabel[field=true] {font-weight: bold; " + 
                           self.başlıkcsstext + " }")
        self.show()
        
    def changeTexts(self):
        if self.ekleçıkar == 'ekle':
            self.windowtitletext = "Ekle - Standart Malzemeler"
            self.başlıkLabeltext = ("Standart Malzemeler Tablosunda\n" +
                                    "Stok Bölgesine Ekle")
            self.başlıkcsstext = 'color: green;'
            self.ekleçıkaradettext = 'Eklenecek Adet:'
            self.ekleçıkarbtntext = 'Ekle'
            
        elif self.ekleçıkar == 'çıkar':
            self.windowtitletext = "Çıkar - Standart Malzemeler"
            self.başlıkLabeltext = ("Standart Malzemeler Tablosunda\n" +
                                    "Stok Bölgesinden Çıkar")
            self.başlıkcsstext = 'color: purple;'
            self.ekleçıkaradettext = 'Çıkarılacak Adet:'
            self.ekleçıkarbtntext = 'Çıkar'
            
        elif self.ekleçıkar == 'sil':
            self.windowtitletext = "Kaydı Sil - Standart Malzemeler"
            self.başlıkLabeltext = ("Standart Malzemeler Tablosunda\n" +
                                    "Kaydı Sil")
            self.başlıkcsstext = 'color: tomato;'
            self.ekleçıkaradettext = 'Sil Adet Kullanılmayacak:'
            self.ekleçıkarbtntext = 'Kaydı Sil'
            
        else:
            print(__name__,":Hatalı ekle/çıkar parametresi girilmiş !!!")
            return self.done(QDialog.Rejected)
        
    def bilgileriAl(self):
        rowdata = self.anapencere.tableView_Model.sqldata[self.rowNo]
        #print("Alınan satır bilgisi:",rowdata)
        self.myrecord = standart_malzemeler_record(self.anapencere)
        self.myrecord.setfromtablerowdata(rowdata)
        
    def UIoluştur(self):
        
        self.setGeometry(100,100,300,300)
        self.setModal(True)
        self.setWindowTitle(self.windowtitletext)
        
        self.adetproper = False
        
        def başlıksection():
            resim = QLabel()
            resim.setMaximumHeight(100)
            path = os.path.join('images','letter_S_blue.png')
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
            
            self.Tipi = QLabel(self.myrecord.Tipi)
            self.Tipi.setProperty("field", True)
            
            self.Tip_Kodu = QLabel(self.myrecord.Tip_Kodu)
            self.Tip_Kodu.setProperty("field", True)
            
            
            self.Boyutlar = QLabel(self.myrecord.Boyutlar)
            self.Boyutlar.setProperty("field", True)
            
            self.Stok_Bölgesi = QLabel(self.myrecord.Stok_Bölgesi)
            self.Stok_Bölgesi.setProperty("field", True)
            
            self.Adet = QLabel(str(self.myrecord.Adet))
            self.Adet.setProperty("field", True)
            
            self.EkleÇıkarAdet = QLineEdit()
            self.EkleÇıkarAdet.textChanged.connect(
                lambda text: self.AdetCheckSlot(text)
                )
            self.EkleÇıkarAdet.textChanged.connect(self.btnsetEnable)
                
            section = QFormLayout()
            section.addRow(QLabel("Malzeme Tipi:"), self.Tipi)
            section.addRow(QLabel("Malzeme Tip Kodu:"), self.Tip_Kodu)
            section.addRow(QLabel("Malzeme Boyutları:"), self.Boyutlar)
            section.addRow(QLabel("Stok Bölgesi Kodu:"), self.Stok_Bölgesi)
            section.addRow(QLabel("Bulunan Adet:"), self.Adet)
            if self.ekleçıkar in ('ekle','çıkar'):
                section.addRow(QLabel(self.ekleçıkaradettext), self.EkleÇıkarAdet)
            return section

        def buttonsection():
            iptalbtn = QPushButton("İptal")
            iptalbtn.setDefault(True)
            iptalbtn.clicked.connect(self.iptalbtn_call)
            self.ekleçıkarbtn = QPushButton(self.ekleçıkarbtntext)
            self.ekleçıkarbtn.clicked.connect(self.eklecikarbtn_call)
            if self.ekleçıkar in ('ekle','çıkar'):
                self.ekleçıkarbtn.setEnabled(False)
            
            section = QHBoxLayout()
            section.addStretch()
            section.addWidget(iptalbtn)
            section.addWidget(self.ekleçıkarbtn)
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
    
    def eklecikarbtn_call(self):
        matching = self.myrecord.checkformatchingrecord()
        if not matching[0]:
            self.error_msgbox("İlgili Kayıt Bulunamadı. Bu bir hatadır.")
            return self.done(QDialog.Rejected)
        if self.myrecord.record_id != matching[1]:
            self.error_msgbox("Kayıtlar Eşleşmedi. Bu bir hatadır.")
            return self.done(QDialog.Rejected)
        if self.ekleçıkar == 'ekle':
            newadet = self.myrecord.Adet + int(self.EkleÇıkarAdet.text())
        elif self.ekleçıkar == 'çıkar':
            newadet = self.myrecord.Adet - int(self.EkleÇıkarAdet.text())
            if newadet<0:
                self.msgLabel.setText("Çıkarılacak Adet Bulunan Adet'ten Büyük Olamaz !")
                return
        if self.ekleçıkar in ('ekle','çıkar'):
            self.myrecord.update_adet_of_tablerecord(newadet)
        elif self.ekleçıkar == 'sil':
            self.myrecord.delete_tablerecord()
        return self.done(QDialog.Accepted)
                
    def dialogMoveCenter(self):
        screenCenter=QApplication.desktop().availableGeometry().center()
        myrect=self.frameGeometry()
        myrect.moveCenter(screenCenter)
        self.move(myrect.topLeft())

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
        
            
    def btnsetEnable(self):
        if self.adetproper and self.Adet.text():
            self.ekleçıkarbtn.setEnabled(True)
        else:
            self.ekleçıkarbtn.setEnabled(False)
            
    def error_msgbox(self,errortext):
        msgbox = QMessageBox() 
        msgbox.setIcon(QMessageBox.Critical)
        msgbox.setWindowTitle("Hata")
        msgbox.setText(errortext)
        msgbox.setInformativeText("Durumu Barış Kılıçlar'a bildiriniz. "
                                  "Tel: 0532 224 07 31")
        msgbox.setStandardButtons(QMessageBox.Ok)
        return msgbox.exec_()
    