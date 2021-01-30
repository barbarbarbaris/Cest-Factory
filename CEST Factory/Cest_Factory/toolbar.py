'''
Created on 8 Ara 2020

@author: user
'''
from PyQt5.QtWidgets import QToolButton, QButtonGroup, QFrame, QHBoxLayout,\
    QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from PyQt5.Qt import QItemSelection

class MyClass(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        
def toolbaryap(self):
    self.toolbar = self.addToolBar('ToolBar')
    self.toolbar.setFixedHeight(50)
    self.toolbar.setIconSize(QSize(30, 30))
    
    def stokActionCall(s):
        if s:
            self.stoklistframe.show()
            self.ticlistframe.hide()
            #print(self.stokListView.selectionModel().selectedIndexes())
            selIdxs = self.stokListView.selectionModel().selectedIndexes()
            if selIdxs:
                selected = QItemSelection(selIdxs[0],selIdxs[0])
                #print("hello?:",selIdxs[0],selIdxs[0].row(),selIdxs[0].column())
                self.stokListView.selectionModel().selectionChanged.emit(selected,QItemSelection())
            
    def kişilerActionCall(s):
        pass
    
    def ticaretActionCall(s):
        if s:
            self.stoklistframe.hide()
#             self.toolbar.addStokToolButton.setEnabled(False)
            self.ticlistframe.show()
            selIdxs = self.ticListView.selectionModel().selectedIndexes()
            #print(selIdxs)
            if selIdxs:
                selected = QItemSelection(selIdxs[0],selIdxs[0])
                #print("hello?:",selIdxs[0],selIdxs[0].row(),selIdxs[0].column())
                self.ticListView.selectionModel().selectionChanged.emit(selected,QItemSelection())
        
#     stokAction = self.toolbar.addAction(QIcon('images\\people_small'),'Kişiler')
#     stokAction.setCheckable(True)
#     stokAction.triggered.connect(kişilerActionCall)
    
#     kişilerAction = self.toolbar.addAction(QIcon('images\\people_small'),'Kişiler')
#     kişilerAction.setCheckable(True)
#     kişilerAction.triggered.connect(kişilerActionCall)
    
    stokToolButton = QToolButton()
    stokToolButton.setIcon(QIcon('images\\tables küçük'))
    stokToolButton.setCheckable(True)
    stokToolButton.setChecked(True)
    stokToolButton.clicked.connect(stokActionCall)
    self.toolbar.addWidget(stokToolButton)
    
    kişilerToolButton = QToolButton()
    kişilerToolButton.setIcon(QIcon('images\\people_small'))
    kişilerToolButton.setCheckable(True)
    kişilerToolButton.clicked[bool].connect(kişilerActionCall)
    self.toolbar.addWidget(kişilerToolButton)
    
    ticaretToolButton = QToolButton()
    ticaretToolButton.setIcon(QIcon('images\\business kucuk mavi'))
    ticaretToolButton.setCheckable(True)
    ticaretToolButton.clicked[bool].connect(ticaretActionCall)
    self.toolbar.addWidget(ticaretToolButton)

    bg1 = QButtonGroup(self.toolbar)
#     mybutton = QPushButton("Dene")
#     bg1.addButton(mybutton)
    bg1.addButton(stokToolButton)
    bg1.addButton(kişilerToolButton)
    bg1.addButton(ticaretToolButton)
    bg1.setExclusive(True)
    
    self.toolbar.addSeparator()
    
    if any(x in self.yetki for x in ['A','B','C']):
        addrowact = self.toolbar.addAction(QIcon('images\\add-1-icon'),'Kayıt Ekle')
        addrowact.triggered.connect(self.yenikayıtekle_mi.trigger)
        deleterowact = self.toolbar.addAction(QIcon('images\\minus_icon_red_small.png'),'Kayıt Sil')
        deleterowact.triggered.connect(self.kayıtsil_mi.trigger)
#         #---------- Tool buttons (not actşon)
#          
#         self.toolbar.addStokToolButton = QToolButton()
#         self.toolbar.addStokToolButton.setIcon(QIcon('images\\add-1-icon'))
#         self.toolbar.addStokToolButton.clicked.connect(self.yenikayıtekle_mi.trigger)
#         self.toolbar.addWidget(self.toolbar.addStokToolButton)
#           
#         self.toolbar.deleterowWidget = self.toolbar.widgetForAction(deleterowact)

        
    toolbarright = QFrame()
    tbrlo = QHBoxLayout()
    toolbarrighttext = QLabel(self.username)
    tbrlo.addStretch()
    tbrlo.addWidget(toolbarrighttext)
    #tbrlo.addWidget(showprofilAct)
    toolbarright.setLayout(tbrlo)
    self.toolbar.addWidget(toolbarright)
    
    def showprofilActionCall(checked):
        if checked:
            self.yantaraf_fr.hide()
            self.prf.show()
        else:
            self.prf.hide()
            self.yantaraf_fr.show()
    showprofilAct = QToolButton()
    showprofilAct.setIcon(QIcon('images\\profil-1.png'))
    showprofilAct.setCheckable(True)
    #self.toolbar.addWidget(showprofilAct)
    showprofilAct.clicked.connect(showprofilActionCall)
    self.toolbar.addWidget(showprofilAct)