'''
Created on 10 Oca 2021

@author: user
'''
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QHBoxLayout,\
    QApplication, QGridLayout, QLineEdit, QFormLayout, QGroupBox, QTableView,\
    QPushButton, QAbstractItemView
from PyQt5.QtGui import QFont
from Cest_Factory.Cest_Factory_classes import barisTableViewModel
from Cest_Factory.Ekle_Cikar_UI import TicListEkleDialog

def openRelatedDialog(self,index):
#     print(self.ticListView_Model.tablobilgileri)
#     print(self.tableView_Model.seçimNo)    
    seçilitabloname = self.ticListView_Model.tablobilgileri[self.tableView_Model.seçimNo][0]    
    if seçilitabloname == "Müşteriler":
        self.viewDialog = MüşteriTedarikçiView(self,index,'Müşteriler')
    elif seçilitabloname == "Tedarikçiler":
        self.viewDialog = MüşteriTedarikçiView(self,index,'Tedarikçiler')
    
    

class MüşteriTedarikçiView(QDialog):
    '''
    classdocs
    '''


    def __init__(self, anapencere,index,müşTed):
        '''
        Constructor
        '''
        
        super().__init__()
        self.anapencere = anapencere
        self.rowNo = index.row()
        self.MüşTed = müşTed
        #self.bilgileriAl()
        self.changeTexts()
        self.dialogUIoluştur()
        self.dialogMoveCenter()
        self.fillthefields()
        self.show()
        
    def changeTexts(self):
        if self.MüşTed == 'Müşteriler':
            self.windowTitleText = "Müşteri Düzenle"
            self.başlıkLabel = QLabel("Müşteri Düzenle")
            self.başlıkLabel.setStyleSheet('color: green;')
            self.dbtablename = "müşteriler"
            self.idcolname = "idMüşteriler"
        elif self.MüşTed == 'Tedarikçiler':
            self.windowTitleText = "Tedarikçi Düzenle"
            self.başlıkLabel = QLabel("Tedarikçi Düzenle")
            self.başlıkLabel.setStyleSheet('color: blue;')
            self.dbtablename = "tedarikçiler"
            self.idcolname = "idtedarikçiler"
        else:
            print("<-- Bilinmeyen Liste !!! -->")
            self.close()

    def dialogUIoluştur(self):
        
        self.setGeometry(100,100,600,500)
        self.setModal(True)
        
        self.setWindowTitle(self.windowTitleText)
        
        def başlıksection():
            self.başlıkLabel.setFont(QFont('Arial', 12,QFont.Bold))
            
            başlıkhbox = QHBoxLayout()
            başlıkhbox.addStretch()
            başlıkhbox.addWidget(self.başlıkLabel)
            başlıkhbox.addStretch()
            return başlıkhbox
        
        def müşterikimlikbilgilerisection():            
            self.logo = QLabel()
            self.logo.setStyleSheet(
                #"background-color: rgb(100,100,100); "+
                "margin:5px; "+
                "border:1px solid rgb(50,50,50); ")
            self.logo.setMinimumSize(100, 100)
            self.Firma_Adı = QLineEdit()
            self.Firma_Adı.setFont(QFont('Arial', 12,QFont.Bold))            
            self.Adres = QLineEdit()
            self.Açıklama = QLineEdit()
            
            section = QGridLayout()
            section.addWidget(self.logo,0,0,3,1)
            section.addWidget(QLabel("Firma_Adı:"),0,1)
            section.addWidget(self.Firma_Adı,0,2)
            section.addWidget(QLabel("Firma_Adresi:"),1,1)
            section.addWidget(self.Adres,1,2)
            section.addWidget(QLabel("Açıklama:"),2,1)
            section.addWidget(self.Açıklama,2,2)
            return section
    
        def otherfieldssection():
            self.Telefon_No = QLineEdit()
            self.webSite = QLineEdit()
            self.email = QLineEdit()
            
            section = QFormLayout()
            section.addRow(QLabel("Telefon_No:"), self.Telefon_No)
            section.addRow(QLabel("Web_Sitesi:"), self.webSite)
            section.addRow(QLabel("e-mail_Adresi:"), self.email)
            return section
        
        def kişilersection():
            self.kişilertableview = QTableView(self)
            self.kişilertableview.setAlternatingRowColors(True)
            self.kişilertableview.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.kişilertablemodel = barisTableViewModel(self.anapencere)
            self.kişilertableview.setModel(self.kişilertablemodel)
            
            
            kişieklebtn = QPushButton("Kişi Ekle")
            kişieklebtn.clicked.connect(self.kisieklebtn_call)
            btnlo = QHBoxLayout()
            btnlo.addStretch()
            btnlo.addWidget(kişieklebtn)
            
            sectionlo = QVBoxLayout()
            sectionlo.addWidget(self.kişilertableview)
            sectionlo.addLayout(btnlo)
            section = QGroupBox("Bu Firma Adıyla Kayıtlı Kişiler")
            section.setLayout(sectionlo)
            return section
        
        def buttonsection():
            iptalbtn = QPushButton("İptal")
            iptalbtn.setDefault(True)
            iptalbtn.clicked.connect(self.iptalbtn_call)
            uygulabtn = QPushButton("Uygula")
            uygulabtn.clicked.connect(self.uygulabtn_call)
            
            section = QHBoxLayout()
            section.addStretch()
            section.addWidget(iptalbtn)
            section.addWidget(uygulabtn)
            return section

        mainvboxlayout = QVBoxLayout()
        self.setLayout(mainvboxlayout)
        
        mainvboxlayout.addLayout(başlıksection())
        mainvboxlayout.addSpacing(10)
        mainvboxlayout.addLayout(müşterikimlikbilgilerisection())
        mainvboxlayout.addSpacing(10)
        mainvboxlayout.addLayout(otherfieldssection())
        mainvboxlayout.addSpacing(10)
        self.kişilerGB = kişilersection()
        mainvboxlayout.addWidget(self.kişilerGB)
        mainvboxlayout.addStretch()
        mainvboxlayout.addLayout(buttonsection())
            
    def dialogMoveCenter(self):
        screenCenter=QApplication.desktop().availableGeometry().center()
        myrect=self.frameGeometry()
        myrect.moveCenter(screenCenter)
        self.move(myrect.topLeft())
    
    def fillthefields(self):
        print(self.anapencere.tableView_Model.sqldata)
        self.Firma_Adı.setText(self.anapencere.tableView_Model.sqldata[self.rowNo][1])
        self.Adres.setText(self.anapencere.tableView_Model.sqldata[self.rowNo][3])
        self.Açıklama.setText(self.anapencere.tableView_Model.sqldata[self.rowNo][2])
        self.Telefon_No.setText(self.anapencere.tableView_Model.sqldata[self.rowNo][4])
        self.webSite.setText(self.anapencere.tableView_Model.sqldata[self.rowNo][5])
        self.email.setText(self.anapencere.tableView_Model.sqldata[self.rowNo][6])
        
        self.kişilerGB.setTitle("'{}' ".format(self.Firma_Adı.text()) +
                                "Firma Adıyla Kayıtlı Kişiler")
        
        self.kişilertablemodel.setTable("kişiler")
        self.kişilertablemodel.setSQLData("SELECT * FROM kişiler WHERE Firma_Adı='{}'".
                                          format(self.Firma_Adı.text()))
    
    def kisieklebtn_call(self):
        self.kişiekledialog = TicListEkleDialog(self.anapencere,
                                                called_from = 'ticdialogs_müşdzn_kşekle',
                                                firma_adı = self.Firma_Adı.text())
        def kişiekleaccepted(*args):
            print("Slottan sesleniyom <<<<<<<<<<<<<<<<<<<<<<",args)
            self.kişilertablemodel.setTable("kişiler")
            self.kişilertablemodel.setSQLData("SELECT * FROM kişiler WHERE Firma_Adı='{}'".
                                              format(self.Firma_Adı.text()))
        print(type(self.kişiekledialog.accepted))
        self.kişiekledialog.accepted.connect(kişiekleaccepted)
#         self.kişiekledialog.exec_()
#         if self.kişiekledialog.result() == QDialog.Accepted:
#             self.kişilertablemodel.setTable("kişiler")
#             self.kişilertablemodel.setSQLData("SELECT * FROM kişiler WHERE Firma_Adı='{}'".
#                                               format(self.Firma_Adı.text()))
    
    def iptalbtn_call(self):
        self.done(QDialog.Rejected)
    
    def uygulabtn_call(self):
        cmd = ("UPDATE {} ".format(self.dbtablename) +
            "SET Firma_Adı='{}', ".format(self.Firma_Adı.text()) +
            "Açıklama='{}', ".format(self.Açıklama.text()) +
            "Firma_Adresi='{}', ".format(self.Adres.text()) +
            "Telefon_No='{}', ".format(self.Telefon_No.text()) +
            "Web_Sitesi='{}', ".format(self.webSite.text()) +
            "e_mail_adresi='{}' ".format(self.email.text()) +
            "WHERE {} = {};".format(self.idcolname,
                str(self.anapencere.tableView_Model.sqldata[self.rowNo][0]))
            )
        self.anapencere.stok_dbm.executeCmd(cmd)
        self.anapencere.tableView_Model.setTable(self.dbtablename)
        self.done(QDialog.Accepted)
