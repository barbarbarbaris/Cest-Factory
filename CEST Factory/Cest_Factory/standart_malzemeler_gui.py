'''
Created on 30 Oca 2021

@author: user
'''
from PyQt5.QtWidgets import QLabel, QLineEdit


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
        self.rowNo = index.row()

        #self.bilgileriAl()
        self.changeTexts()
        self.dialogUIoluştur()
        self.dialogMoveCenter()
        self.show()
        
    def dialogUIoluştur(self):
        
        self.setGeometry(100,100,600,500)
        self.setModal(True)
        
        self.setWindowTitle("Standart Malzemeler")
        
        def başlıksection():
            self.başlıkLabel = QLabel("Standart Malzemeler")
            self.başlıkLabel.setStyleSheet('color: blue;')
            self.başlıkLabel.setFont(QFont('Arial', 12,QFont.Bold))
            
            başlıkhbox = QHBoxLayout()
            başlıkhbox.addStretch()
            başlıkhbox.addWidget(self.başlıkLabel)
            başlıkhbox.addStretch()
            return başlıkhbox

        def fieldssection():
            self.Tipi = QLineEdit()
            self.Tip_Kodu = QLineEdit()
            self.Boyutlar = QLineEdit()
            self.Adet = QLineEdit()
            self.Stok_Bölgesi = QLineEdit()
            
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
        mainvboxlayout.addLayout(fieldssection())
        mainvboxlayout.addSpacing(10)
        mainvboxlayout.addStretch()
        mainvboxlayout.addLayout(buttonsection())

    def iptalbtn_call(self):
        self.done(QDialog.Rejected)
    
    def uygulabtn_call(self):
        self.done(QDialog.Accepted)
        
    def dialogMoveCenter(self):
        screenCenter=QApplication.desktop().availableGeometry().center()
        myrect=self.frameGeometry()
        myrect.moveCenter(screenCenter)
        self.move(myrect.topLeft())
        
    def hellorilerdengel(self):
        print("Ule hellorilerden gelirem uleeeooo")
        print("ule ule uleeeee")
        print("ulan alla laaaa")