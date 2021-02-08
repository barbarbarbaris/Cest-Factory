'''
Created on 7 Şub 2021

@author: user
'''
from PyQt5.QtWidgets import QDialog, QLabel, QHBoxLayout, QVBoxLayout,\
    QFormLayout, QPushButton, QApplication, QLineEdit, QMessageBox
import os
from PyQt5.QtGui import QPixmap, QFont
from Cest_Factory.tipler_kodlar.tipler_kodlar_helper import tipler_kodlar_record

class tipler_kodlar_yeni_ekle_sil_gui(QDialog):
    '''
    classdocs
    '''


    def __init__(self, anapencere, eklesil,*,rowNo=0):
        '''
        Constructor
        '''
        super().__init__()
        self.anapencere = anapencere
        self.eklesil = eklesil
        self.rowNo = rowNo
        
        self.gerekliBilgileriAl()
        self.changeTexts()
        self.UIoluştur()
        self.dialogMoveCenter()
        self.setStyleSheet("QLabel[field=true] {font-weight: bold; " + 
                           self.başlıkcsstext + " }")
        self.show()
    
    def gerekliBilgileriAl(self):
        tm = self.anapencere.tableView_Model
        seçilen_tablonun_özellikleri = self.anapencere.gösterilecek_tablo_bilgileri[tm.seçimNo]
        #print(seçilen_tablonun_özellikleri)
        self.seçilitablo_showname = seçilen_tablonun_özellikleri[0]
        self.seçilitablo_dbname = seçilen_tablonun_özellikleri[1]
        self.seçilitablo_iconfile =  seçilen_tablonun_özellikleri[2]
        
        self.colnames = tm.sqlheader
        
        cmd = "SELECT {} FROM {}".format(self.colnames[1][0],self.seçilitablo_dbname)
        msg = self.anapencere.stok_dbm.executeCmd(cmd)
        self.field1recordsintable = [x[0] for x in msg] #Çok Fazla Sayıda İse ??
        
        if self.eklesil == 'kaydısil':
            rowdata = self.anapencere.tableView_Model.sqldata[self.rowNo]
            #print("Alınan satır bilgisi:",rowdata)
            self.myrecord = tipler_kodlar_record(self.anapencere,self)
            self.myrecord.setfromtablerowdata(rowdata)
        
    def changeTexts(self):
        
        if self.eklesil == 'ekle':
            self.windowtitletext = 'Yeni Kayıt Oluştur - ' + self.seçilitablo_showname
            self.başlıkLabeltext = (self.seçilitablo_showname + 
                                    " Tablosunda\n" +
                                    "Yeni Kayıt Oluştur")
            self.başlıkcsstext = 'color: blue;'
            self.yenieklesilbtntext = "Yeni Kayıt Oluştur"
        elif self.eklesil == 'sil':
            self.windowtitletext = 'Kayıt Sil - ' + self.seçilitablo_showname
            self.başlıkLabeltext = (self.seçilitablo_showname + 
                                    " Tablosundan\n" +
                                    "Kayıt Sil")
            self.başlıkcsstext = 'color: tomato;'
            self.yenieklesilbtntext = "Kayıt Sil"
        elif self.eklesil == 'kaydısil':
            self.windowtitletext = 'Kaydı Sil - ' + self.seçilitablo_showname
            self.başlıkLabeltext = (self.seçilitablo_showname + 
                                    " Tablosundan\n" +
                                    "Kayıt Sil")
            self.başlıkcsstext = 'color: tomato;'
            self.yenieklesilbtntext = "Kaydı Sil"
        else:
            print(__name__,":Hatalı ekle/sil parametresi girilmiş !!!")
            return self.done(QDialog.Rejected)
        
    def UIoluştur(self):

        self.setWindowTitle(self.windowtitletext)
        self.setGeometry(100,100,200,100)
        self.setModal(True)
        
        self.field1proper = False
        
        def başlıksection():
            resim = QLabel()
            resim.setMaximumHeight(72)
            path = os.path.join('images',self.seçilitablo_iconfile)
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
             
            self.le1 = QLineEdit()
            self.le1.textChanged.connect(
                lambda text: self.le1CheckSlot(text)
                )
            self.le1.textChanged.connect(self.btnsetEnable)
#             
            self.le2 = QLineEdit()
            
                
            section = QFormLayout()
            
            if self.eklesil == 'ekle':
                section.addRow(QLabel(self.colnames[1][0]+":"), self.le1)
                section.addRow(QLabel(self.colnames[2][0]+":"), self.le2)
            elif self.eklesil == 'sil':
                section.addRow(QLabel(self.colnames[1][0]+":"), self.le1)
            elif self.eklesil == 'kaydısil':
                self.field1Label = QLabel(self.myrecord.field1)
                self.field1Label.setProperty("field", True)
                self.field2Label = QLabel(self.myrecord.field2)
                self.field2Label.setProperty("field", True)
                section.addRow(QLabel(self.colnames[1][0]+":"), self.field1Label)
                section.addRow(QLabel(self.colnames[2][0]+":"), self.field2Label)
            return section
        
        def buttonsection():
            iptalbtn = QPushButton("İptal")
            iptalbtn.setDefault(True)
            iptalbtn.clicked.connect(self.iptalbtn_call)
            self.yenieklesilbtn = QPushButton(self.yenieklesilbtntext)
            self.yenieklesilbtn.clicked.connect(self.yenieklesilbtn_call)
            if self.eklesil in ('ekle','sil'):
                self.yenieklesilbtn.setEnabled(False)
            elif self.eklesil == 'kaydısil':
                self.yenieklesilbtn.setEnabled(True)
            
            section = QHBoxLayout()
            section.addStretch()
            section.addWidget(iptalbtn)
            section.addWidget(self.yenieklesilbtn)
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
        
    def dialogMoveCenter(self):
        screenCenter=QApplication.desktop().availableGeometry().center()
        myrect=self.frameGeometry()
        myrect.moveCenter(screenCenter)
        self.move(myrect.topLeft())
        
    def iptalbtn_call(self):
        self.done(QDialog.Rejected)
    
    def yenieklesilbtn_call(self):
        if self.eklesil == 'ekle':
            self.myrecord = tipler_kodlar_record(self.anapencere, self,
                                                 field1 = self.le1.text(),
                                                 field2 = self.le2.text())
            matching = self.myrecord.checkformatchingrecord()
            if not matching[0]:
                self.myrecord.insertinto_table()
                return self.done(QDialog.Accepted)
            else:
                self.error_msgbox("Kayıt Bulundu. Bu bir hatadır.")
                return self.done(QDialog.Rejected)
        if self.eklesil in ('sil','kaydısil'):
            if self.eklesil == 'sil':
                self.myrecord = tipler_kodlar_record(self.anapencere, self,
                                                     field1 = self.le1.text()
                                                     )
            matching = self.myrecord.checkformatchingrecord()
            if matching[0]:
                self.myrecord.record_id = matching[1]
                self.myrecord.deletefromtable()
                return self.done(QDialog.Accepted)
            else:
                self.error_msgbox("Kayıt Bulunamadı. Bu bir hatadır.")
                return self.done(QDialog.Rejected)
            
        self.done(QDialog.Rejected)
        
    def le1CheckSlot(self,text):
        if not self.seçilitablo_dbname == 'malzeme_tipleri': #içinde boşluk olabilir
            text = text.strip()
        text = text.upper()
        text = text.replace('İ','I')
        self.le1.setText(text)
        if not text:
            self.msgLabel.setText(self.colnames[1][0] + ' Boş Bırakılamaz')
            self.field1proper = False
            return
        if self.eklesil == 'ekle':
            if text in self.field1recordsintable:
                self.msgLabel.setText("'" + text + "'"
                                       " Kaydı Zaten Var")
                self.field1proper = False
            else:
                self.msgLabel.setText('')
                self.field1proper = True
        if self.eklesil == 'sil':
            if text not in self.field1recordsintable:
                self.msgLabel.setText("'" + text + "'"
                                       " Bulunamadı")
                self.field1proper = False
            else:
                self.msgLabel.setText('')
                self.field1proper = True

    def btnsetEnable(self):
        if self.field1proper and self.le1.text():
            self.yenieklesilbtn.setEnabled(True)
        else:
            self.yenieklesilbtn.setEnabled(False)
            
    def error_msgbox(self,errortext):
        msgbox = QMessageBox() 
        msgbox.setIcon(QMessageBox.Critical)
        msgbox.setWindowTitle("Hata")
        msgbox.setText(errortext)
        msgbox.setInformativeText("Durumu Barış Kılıçlar'a bildiriniz. "
                                  "Tel: 0532 224 07 31")
        msgbox.setStandardButtons(QMessageBox.Ok)
        return msgbox.exec_()