'''
Created on 8 Ara 2020

@author: user
'''
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLineEdit, QPushButton
from PyQt5.Qt import QLabel, Qt

class MyClass(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        
def profilimFrameOluştur(self):
    self.prf = QFrame()
    layout = QVBoxLayout()
    

    
    profilresmiLabel = QLabel()
    profilresmiLabel.setStyleSheet(
        #"background-color: rgb(100,100,100); "+
        "margin:5px; "+
        "border:1px solid rgb(50,50,50); ")
    profilresmiLabel.setMinimumSize(100, 150)
    #profilresmiLabel.setPixmap()
    usernameLabel = QLabel("Kullanıcı Adı")    
    usernameLabel.setMaximumWidth(150)
    usernameField = QLineEdit()
    usernameField.setMaximumWidth(150)
    usernameField.setText(self.username)
    usernameField.setEnabled(False)
    
    def şifreTextChangedSlot():
        if şifreEdit.text() and şifreEdit.text() == şifreTekrarEdit.text():
            şifreDeğiştirBtn.setEnabled(True)
        else:
            şifreDeğiştirBtn.setEnabled(False)
    
    şifreLabel = QLabel("Yeni Şifre")
    şifreLabel.setMaximumWidth(150)
    şifreEdit = QLineEdit()
    şifreEdit.setEchoMode(QLineEdit.Password)
    şifreEdit.textChanged.connect(şifreTextChangedSlot)
    şifreEdit.setMaximumWidth(150)
    
    şifreTekrarLabel = QLabel("Yeni Şifre tekrar")
    şifreTekrarLabel.setMaximumWidth(150)
    şifreTekrarEdit = QLineEdit()
    şifreTekrarEdit.setEchoMode(QLineEdit.Password)
    şifreTekrarEdit.textChanged.connect(şifreTextChangedSlot)
    şifreTekrarEdit.setMaximumWidth(150)
    
    def şifreDeğiştirBtnCall():
        if şifreEdit.text() and şifreEdit.text() == şifreTekrarEdit.text():
            cmd = (
                "UPDATE kullanıcılar SET Şifre = '{}' ".format(şifreEdit.text()) +
                "WHERE Kullanıcı_Adı = '{}'".format(self.username)
                )
            msg =self.stok_dbm.executeCmd(cmd)
            if not msg:
                self.statusBar().showMessage('Şifre değişti')
                şifreEdit.setText('')
                şifreTekrarEdit.setText('')
            else:
                self.statusBar().showMessage('Hata oluştu. Şifre değişmedi')
    
    şifreDeğiştirBtn = QPushButton("Şifre Değiştir")
    #şifreDeğiştirBtn.setMaximumWidth(150)
    şifreDeğiştirBtn.setMinimumWidth(150)
    şifreDeğiştirBtn.setEnabled(False)
    şifreDeğiştirBtn.clicked.connect(şifreDeğiştirBtnCall)
    
    layout.addWidget(profilresmiLabel)
    layout.setAlignment(profilresmiLabel, Qt.AlignHCenter)
    layout.addStretch()
    layout.addWidget(usernameLabel)
    layout.setAlignment(usernameLabel, Qt.AlignHCenter)
    layout.addWidget(usernameField)
    layout.setAlignment(usernameField, Qt.AlignHCenter)
    layout.addStretch()
    layout.addWidget(şifreLabel)
    layout.setAlignment(şifreLabel, Qt.AlignHCenter)
    layout.addWidget(şifreEdit)
    layout.setAlignment(şifreEdit, Qt.AlignHCenter)
    #layout.addStretch()
    layout.addWidget(şifreTekrarLabel)
    layout.setAlignment(şifreTekrarLabel, Qt.AlignHCenter)
    layout.addWidget(şifreTekrarEdit)
    layout.setAlignment(şifreTekrarEdit, Qt.AlignHCenter)
    #layout.addStretch()
    layout.addWidget(şifreDeğiştirBtn)
    layout.setAlignment(şifreDeğiştirBtn, Qt.AlignHCenter)
    layout.addStretch()
    
    self.prf.setLayout(layout)
    self.prf.hide()
    