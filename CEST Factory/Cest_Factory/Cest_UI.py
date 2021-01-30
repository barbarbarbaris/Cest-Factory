'''
Created on 27 Kas 2020

@author: Barış Kılıçlar
'''

import sys,os
from PyQt5.QtWidgets import QAction,QFrame,QDialog,QLabel,QLineEdit,QGridLayout,\
        QPushButton,QApplication,QHBoxLayout,QListView,QAbstractItemView,\
        QTableView,QWidget,QSplitter, QGroupBox,QVBoxLayout,QStyledItemDelegate,\
    QCheckBox, QButtonGroup, QToolButton
from PyQt5.QtGui import QIcon,QFont,QStandardItemModel,QPixmap
from PyQt5.QtCore import Qt,QSize

from Cest_Factory.Cest_Factory_classes import barisTableViewModel,differentRow
from Cest_Factory.Kişiler_UI import profilimFrameOluştur
from Cest_Factory.menü import menüyap
from Cest_Factory.toolbar import toolbaryap
from Cest_Factory.solFrame import listeleriOluştur,solFrame_oluştur
from Cest_Factory.Stok_SağFrame import StokFrameOluştur



class MyClass_In_Cest_UI(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''

def ui_oluştur(self):
    menüyap(self)
    toolbaryap(self)
    centralWidget_oluştur(self)
    
def centralWidget_oluştur(self):
    
    listeleriOluştur(self)
    solFrame_oluştur(self)
    StokFrameOluştur(self)
    profilimFrameOluştur(self)
    
    splitter=QSplitter(Qt.Horizontal)
    splitter.addWidget(self.solframe)
    splitter.addWidget(self.yantaraf_fr)
    splitter.addWidget(self.prf)
    splitter.setSizes([80,200,200])
    
    self.mainwidget=QWidget(self)
    
    layout = QHBoxLayout()
    layout.addWidget(splitter)
    self.mainwidget.setLayout(layout)
    
    self.setCentralWidget(self.mainwidget)
    self.setWindowIcon(QIcon(os.path.join('images', 'CestIcon.png')))
    
def bişeyleryap(self):
    #print (self.tableview.itemDelegate())
    #self.tableview.setItemDelegateForRow(3, QStyledItemDelegate())
    pass
def usernamepassDialogOluştur(self):
    usernamepassdialog = QDialog(self)
    usernamepassdialog.setWindowTitle("Kullanıcı Girişi")
    usernamepassdialog.setGeometry(100,100,300,100)
    #╠usernamepassdialog.setWindowModality(Qt.ApplicationModal) # it is default
        
    usernamepassdialog.layout = QGridLayout()
    usernamepassdialog.setLayout(usernamepassdialog.layout)
    
    usernamepassdialog.layout.addWidget(QLabel("Kullanıcı Adı:"),0,0)
    usernamepassdialog.usernameEdit = QLineEdit()
    usernamepassdialog.layout.addWidget(usernamepassdialog.usernameEdit,0,1)
    
    usernamepassdialog.layout.addWidget(QLabel("Şifre:"),1,0)
    usernamepassdialog.userpwEdit = QLineEdit()
    usernamepassdialog.userpwEdit.setEchoMode(QLineEdit.Password)
    usernamepassdialog.layout.addWidget(usernamepassdialog.userpwEdit,1,1)
    
    def pwgösterCall(sondurum):
        if sondurum:
            usernamepassdialog.userpwEdit.setEchoMode(QLineEdit.Normal)
        else:
            usernamepassdialog.userpwEdit.setEchoMode(QLineEdit.Password)
    
    usernamepassdialog.pwgöstercheck = QCheckBox("Şifreyi Göster",usernamepassdialog)
    usernamepassdialog.layout.addWidget(usernamepassdialog.pwgöstercheck,2,1)
    usernamepassdialog.pwgöstercheck.stateChanged.connect(pwgösterCall)
    
    def iptalbtnCall():
        usernamepassdialog.done(QDialog.Rejected)
    
    usernamepassdialog.iptalbtn = QPushButton("İptal")
    usernamepassdialog.layout.addWidget(usernamepassdialog.iptalbtn,3,0)
    usernamepassdialog.iptalbtn.clicked.connect(iptalbtnCall)
    
    
    def girişbtnCall():
        self.username = usernamepassdialog.usernameEdit.text()
        self.userpw = usernamepassdialog.userpwEdit.text()
        usernamepassdialog.done(QDialog.Accepted)
    
    usernamepassdialog.girişbtn = QPushButton("Giriş",usernamepassdialog)
    usernamepassdialog.girişbtn.setDefault(True)   
    #pushButton.setAutoDefaul(True
    usernamepassdialog.layout.addWidget(usernamepassdialog.girişbtn,3,1)
    usernamepassdialog.girişbtn.clicked.connect(girişbtnCall)

    
    screenCenter=QApplication.desktop().availableGeometry().center()
    myrect=usernamepassdialog.frameGeometry()
    myrect.moveCenter(screenCenter)
    usernamepassdialog.move(myrect.topLeft())
    usernamepassdialog.exec_()
    return usernamepassdialog.result()