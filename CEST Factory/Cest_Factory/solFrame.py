'''
Created on 8 Ara 2020

@author: user
'''
from PyQt5.QtWidgets import QListView, QAbstractItemView, QFrame, QHBoxLayout,\
    QSplitter, QVBoxLayout, QPushButton, QAction
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
from PyQt5.QtCore import QSize
from Cest_Factory.Stok_SağFrame import addFilters
import os
from PyQt5.Qt import Qt
from Cest_Factory.Ekle_Cikar_UI import MalzemeEkleÇıkarDailog


class MyClass(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        
def listeleriOluştur(self):
    
    self.stokListView = QListView()#self.mainwidget) 
    self.stokListView_Model = QStandardItemModel()
    self.stokListView.setModel(self.stokListView_Model)
    self.stokListView.setSelectionBehavior(QAbstractItemView.SelectRows)
    self.stokListView.setEditTriggers(QAbstractItemView.NoEditTriggers)
    self.stokListView.setIconSize(QSize(50, 50))
#     butindex = self.stokListView_Model.createIndex(1,2)
#     listwbut = QPushButton("halo")
#     self.stokListView.setIndexWidget(butindex, listwbut)
    def selectionChanged(selected,deselected):
        self.gösterilecek_tablo_bilgileri = self.stokListView_Model.tablobilgileri
        #print(self.gösterilecek_tablo_bilgileri)
        self.statusBar().showMessage('')
        index = selected.indexes()[0]
        #print("QModelIndex.row():",index.row())
        self.secilentabloadı = self.gösterilecek_tablo_bilgileri[index.row()][1]
        self.tableView_Model.setTable(self.secilentabloadı)
        self.tableView_Model.seçimNo = index.row()   # new variable attach
        #self.tableview.itemDelegate().setRow(-1)
        self.tableview.resizeColumnsToContents()
        addFilters(self)
        #print(deselected,deselected.indexes())
    self.stokListView.selectionModel().selectionChanged.connect(selectionChanged)
    
    msg =self.stok_dbm.executeCmd('SELECT gösterilen_tablo_adı, '
                                  'db_tablo_adı, icon_filename '
                                  'FROM gösterilecek_tablolar')
    #print(msg)

    self.stokListView_Model.tablobilgileri = msg
    rowsize = QSize()
    #rowsize.setWidth(50)
    rowsize.setHeight(50)
    for tablodegerleri in self.stokListView_Model.tablobilgileri:
        #print("Val:",text)
        item = QStandardItem(tablodegerleri[0])
        path = os.path.join('images', tablodegerleri[2])
        item.setData(QIcon(path),Qt.DecorationRole)
        item.setData(rowsize,Qt.SizeHintRole)
        self.stokListView_Model.appendRow(item)
        
#-----------------  Context menü oluştur ---------------------------
    if 'B' in self.yetki:
        stokList_yeniekle_ctx_men_it=QAction('Yeni Kayıt Ekle',self)
        stokList_yeniekle_ctx_men_it.triggered.connect(self.yenikayıtekle_mi.trigger)
        self.stokListView.addAction(stokList_yeniekle_ctx_men_it)
    
        stokList_sil_ctx_men_it=QAction('Kayıt Sil',self)
        stokList_sil_ctx_men_it.triggered.connect(self.kayıtsil_mi.trigger)
        self.stokListView.addAction(stokList_sil_ctx_men_it)
    
        
        self.stokListView.setContextMenuPolicy(Qt.ActionsContextMenu)
        
#=================================================================================
    
    self.ticListView = QListView()#self.mainwidget) 
    self.ticListView_Model = QStandardItemModel()
    self.ticListView.setModel(self.ticListView_Model)
    self.ticListView.setSelectionBehavior(QAbstractItemView.SelectRows)
    self.ticListView.setEditTriggers(QAbstractItemView.NoEditTriggers)
    self.ticListView.setIconSize(QSize(50, 50))
    
    def ticaretselectionChanged(selected,deselected):
        self.gösterilecek_tablo_bilgileri = self.ticListView_Model.tablobilgileri
        self.statusBar().showMessage('')
        index = selected.indexes()[0]
        #print("QModelIndex.row():",index.row())
        self.secilentabloadı = self.gösterilecek_tablo_bilgileri[index.row()][1]
        self.tableView_Model.setTable(self.secilentabloadı)
        self.tableView_Model.seçimNo = index.row()   # new variable attach
        #self.tableview.itemDelegate().setRow(-1)
        self.tableview.resizeColumnsToContents()
        addFilters(self)
    self.ticListView.selectionModel().selectionChanged.connect(ticaretselectionChanged)
    
    msg =self.stok_dbm.executeCmd('SELECT gösterilen_tablo_adı, '
                                  'db_tablo_adı, icon_filename '
                                  'FROM ticaretlist_tables')
    #print(msg)

    self.ticListView_Model.tablobilgileri = msg
    for tablodegerleri in self.ticListView_Model.tablobilgileri:
        #print("Val:",text)
        item = QStandardItem(tablodegerleri[0])
        path = os.path.join('images', tablodegerleri[2])
        item.setData(QIcon(path),Qt.DecorationRole)
        self.ticListView_Model.appendRow(item)

#-----------------  Context menü oluştur ---------------------------
    if 'C' in self.yetki:
        ticlist_yeniekle_ctx_men_it=QAction('Yeni Kayıt Ekle',self)
        ticlist_yeniekle_ctx_men_it.triggered.connect(self.yenikayıtekle_mi.trigger)
        self.ticListView.addAction(ticlist_yeniekle_ctx_men_it)
    
        ticlist_sil_ctx_men_it=QAction('Kayıt Sil',self)
        ticlist_sil_ctx_men_it.triggered.connect(self.kayıtsil_mi.trigger)
        self.ticListView.addAction(ticlist_sil_ctx_men_it)
    
        
        self.ticListView.setContextMenuPolicy(Qt.ActionsContextMenu)
        
def solFrame_oluştur(self):
    self.solframe = QFrame()
    sflo = QVBoxLayout()
    
    self.stoklistframe = QFrame()
    tlflo = QVBoxLayout()
    tlflo.addWidget(self.stokListView)
    self.stoklistframe.setLayout(tlflo)
    
    self.ticlistframe = QFrame()
    ticlistfrlo = QVBoxLayout()
    ticlistfrlo.addWidget(self.ticListView)
    self.ticlistframe.setLayout(ticlistfrlo)
    self.ticlistframe.hide() #--------------------------------
    
    splitter=QSplitter(Qt.Horizontal)
    
    splitter.addWidget(self.stoklistframe)
    splitter.addWidget(self.ticlistframe)
    splitter.setSizes([80,80])
    
    sflo.addWidget(splitter)
    
    self.solframe.setLayout(sflo)
    
    self.gösterilecek_tablo_bilgileri = self.stokListView_Model.tablobilgileri
    
    