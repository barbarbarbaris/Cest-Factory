'''
Created on 10 Oca 2021

@author: user
'''
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QHBoxLayout,\
    QApplication, QGridLayout, QLineEdit, QFormLayout, QGroupBox, QTableView,\
    QPushButton, QAbstractItemView
from PyQt5.QtGui import QFont
from Cest_Factory.Cest_Factory_classes import barisTableViewModel
from _operator import le

def openRelatedDialog2(self,index):
#     print(self.ticListView_Model.tablobilgileri)
#     print(self.tableView_Model.seçimNo)    
    seçilitabloname = self.stokListView_Model.tablobilgileri[self.tableView_Model.seçimNo][0]
#     print(self.gösterilecek_tablo_bilgileri[self.tableView_Model.seçimNo])
#     print("ooooooooooooo:",self.tableView_Model.sqlheader[0])
    for alan in [x[0] for x in self.tableView_Model.sqlheader[1:]]:
        print(alan)
    if seçilitabloname in ("Tip Kodları","Stok Bölge Kodları"):
        self.viewDialog = TipStokKodlarıView(self,index,'Tip Kodları')
    elif seçilitabloname:
        pass
#         self.viewDialog = MüşteriTedarikçiView(self,index,'Stok Bölge Kodları')
    
    

class TipStokKodlarıView(QDialog):
    '''
    classdocs
    '''


    def __init__(self, anapencere,index,TipBöl):
        '''
        Constructor
        '''
        
        super().__init__()
        self.anapencere = anapencere
        self.rowNo = index.row()
        self.TipBöl = TipBöl
        #self.bilgileriAl()
        self.dbtablename = self.anapencere.gösterilecek_tablo_bilgileri[
            self.anapencere.tableView_Model.seçimNo][1]
        self.idcolname = self.anapencere.tableView_Model.sqlheader[0][0]
        
        print("eyoooooooooooooooooooooo",self.dbtablename,self.idcolname)
        self.changeTexts()
        self.dialogUIoluştur()
        self.dialogMoveCenter()
        self.fillthefields()
        self.show()
        
    def changeTexts(self):
        if self.TipBöl == 'Tip Kodları':
            self.windowTitleText = "Tip Kodu Düzenle"
            self.başlıkLabel = QLabel("Tip Kodu Düzenle")
            self.başlıkLabel.setStyleSheet('color: green;')
        elif self.TipBöl == 'Stok Bölge Kodları':
            self.windowTitleText = "Stok Bölge Kodu Düzenle"
            self.başlıkLabel = QLabel("Stok Bölge Kodu Düzenle")
            self.başlıkLabel.setStyleSheet('color: blue;')
        else:
            print("<-- Bilinmeyen Liste !!! -->")
            self.close()

    def dialogUIoluştur(self):
        
        self.setGeometry(100,100,400,300)
        self.setModal(True)
        
        self.setWindowTitle(self.windowTitleText)
        
        def başlıksection():
            self.başlıkLabel.setFont(QFont('Arial', 12,QFont.Bold))
            
            başlıkhbox = QHBoxLayout()
            başlıkhbox.addStretch()
            başlıkhbox.addWidget(self.başlıkLabel)
            başlıkhbox.addStretch()
            return başlıkhbox
        
        def alanbilgilerisection():
            
            section = QFormLayout()
            
            self.anapencere.tableView_Model.sqlheader[0][0]
            self.alanadları=[]
            self.alanLineEdits =[]
            for alan in [x[0] for x in self.anapencere.tableView_Model.sqlheader[1:]]:
                self.alanadları.append(alan)
                le = QLineEdit()
                self.alanLineEdits.append(le)
                section.addRow(QLabel(alan), le)
                print(alan)
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
        mainvboxlayout.addLayout(alanbilgilerisection())
        mainvboxlayout.addSpacing(10)
        mainvboxlayout.addStretch()
        mainvboxlayout.addLayout(buttonsection())
            
    def dialogMoveCenter(self):
        screenCenter=QApplication.desktop().availableGeometry().center()
        myrect=self.frameGeometry()
        myrect.moveCenter(screenCenter)
        self.move(myrect.topLeft())
    
    def fillthefields(self):
        print(self.anapencere.tableView_Model.sqldata)
        for i,le in enumerate(self.alanLineEdits):
            le.setText(self.anapencere.tableView_Model.sqldata[self.rowNo][i+1])


    def iptalbtn_call(self):
        self.done(QDialog.Rejected)
    
    def uygulabtn_call(self):
        cmd = "UPDATE {} SET ".format(self.dbtablename)
        alaneşitlikleri=[]
        for i,alan in enumerate(self.alanadları):
            alaneşitlikleri.append("{}='{}'".format(alan,self.alanLineEdits[i].text()))
        cmd += ",".join(alaneşitlikleri)
        cmd += " WHERE {} = {};".format(self.idcolname,
                str(self.anapencere.tableView_Model.sqldata[self.rowNo][0])
                )
#         print("CMD:>>>>>>>>>>>>>:",cmd)
        self.anapencere.stok_dbm.executeCmd(cmd)
        self.anapencere.tableView_Model.setTable(self.dbtablename)
        self.done(QDialog.Accepted)
