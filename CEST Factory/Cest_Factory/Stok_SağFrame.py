'''
Created on 8 Ara 2020

@author: user
'''
from PyQt5.QtWidgets import QGroupBox, QGridLayout, QTableView, QFrame,\
    QVBoxLayout, QSplitter, QHBoxLayout, QLabel, QLineEdit, QAction,\
    QAbstractItemView, QMenu
from Cest_Factory.Cest_Factory_classes import barisTableViewModel
from Cest_Factory.Ekle_Cikar_UI import MalzemeEkleÇıkarDailog,Tableviewdan_sildialog
from PyQt5.Qt import Qt
import os
from PyQt5.QtGui import QIcon
from Cest_Factory.TicTablesEditGUI import openRelatedDialog
from Cest_Factory.StokTablesEditGUI import openRelatedDialog2
from Cest_Factory.standart_malzemeler.üzerine_ekle_çıkar import uzerine_ekle_cikar_gui
from Cest_Factory.standart_malzemeler.yeni_ekle import yeni_ekle_sil_gui

class MyClass(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''

def StokFrameOluştur(self):
    self.tableview = QTableView(self)
    self.tableview.setAlternatingRowColors(True)
    self.tableview.setSelectionBehavior(QAbstractItemView.SelectRows)
    #self.tableview.setItemDelegate(differentRow())
    self.tableheader = self.tableview.horizontalHeader()
    self.tableheader.sectionClicked.connect(self.tableview.sortByColumn) # ??
    
#         self.tableView_Model = QSqlTableModel()
#         self.tableview.setModel(self.tableView_Model)

    self.tableView_Model = barisTableViewModel(self)
    self.tableview.setModel(self.tableView_Model)
    
#-----------------  Context menü oluştur ---------------------------
    def tableviewdan_ekleactionslot_XX():
        selIdxs = self.tableview.selectionModel().selectedIndexes()        
        if self.stoklistframe.isVisible():
            if not selIdxs:
                self.yenikayıtekle_mi.trigger()
                return
            if not 'B' in self.yetki:
                self.statusBar().showMessage('Bu işlem için yetkiniz yok')
                return
            selIdx = selIdxs[0]
            if self.secilentabloadı == 'standart_malzemeler':
                self.uzerine_gui = uzerine_ekle_cikar_gui(self,selIdx.row(),'ekle')
            else:
                self.malzemeekleçıkardialog = MalzemeEkleÇıkarDailog(self,'ekle')
                print(self.tableView_Model.sqldata[selIdx.row()])
                self.malzemeekleçıkardialog.alanlarıDoldur(
                    self.tableView_Model.sqldata[selIdx.row()][1:])
            #self.tableView_Model.sqldata[self.rowNo][1:]
        elif self.ticlistframe.isVisible():
            self.yenikayıtekle_mi.trigger()
            
    def yeniekle_ctx_slot():
        self.standart_malzeme_gui = yeni_ekle_sil_gui(self,'ekle')
        
    def sil_ctx_slot():
        self.standart_malzeme_gui = yeni_ekle_sil_gui(self,'sil')
        
    def ekle_ctx_slot():
        selIdxs = self.tableview.selectionModel().selectedIndexes()
        selIdx = selIdxs[0]
        self.uzerine_gui = uzerine_ekle_cikar_gui(self,selIdx.row(),'ekle')
        
    def çıkar_ctx_slot():
        selIdxs = self.tableview.selectionModel().selectedIndexes()
        selIdx = selIdxs[0]
        self.uzerine_gui = uzerine_ekle_cikar_gui(self,selIdx.row(),'çıkar')
            
    def tableviewdan_silactionslot_XX():
        selIdxs = self.tableview.selectionModel().selectedIndexes()
        if self.stoklistframe.isVisible():
            if not selIdxs:
                self.kayıtsil_mi.trigger()
                return
            if not 'B' in self.yetki:
                self.statusBar().showMessage('Bu işlem için yetkiniz yok')
                return
            selIdx = selIdxs[0]
            if self.secilentabloadı == 'standart_malzemeler':
                self.uzerine_gui = uzerine_ekle_cikar_gui(self,selIdx.row(),'çıkar')
            else:
                self.malzemeekleçıkardialog = MalzemeEkleÇıkarDailog(self,'çıkar')
                print(self.tableView_Model.sqldata[selIdx.row()])
                self.malzemeekleçıkardialog.alanlarıDoldur(
                    self.tableView_Model.sqldata[selIdx.row()][1:])
        elif self.ticlistframe.isVisible():
            if not 'C' in self.yetki:
                self.statusBar().showMessage('Bu işlem için yetkiniz yok')
                return
            #print("Ticlistframe'den seçildi")
            self.tableviewdansil_dialog = Tableviewdan_sildialog(self,selIdx.row())
            
    def tableviewdan_silactionslot():
        selIdxs = self.tableview.selectionModel().selectedIndexes()
        if self.stoklistframe.isVisible():
            if not selIdxs:
                self.kayıtsil_mi.trigger()
                return
            if not 'B' in self.yetki:
                self.statusBar().showMessage('Bu işlem için yetkiniz yok')
                return
            selIdx = selIdxs[0]
            if self.secilentabloadı == 'standart_malzemeler':
                self.uzerine_gui = uzerine_ekle_cikar_gui(self,selIdx.row(),'çıkar')
            else:
                self.malzemeekleçıkardialog = MalzemeEkleÇıkarDailog(self,'çıkar')
                print(self.tableView_Model.sqldata[selIdx.row()])
                self.malzemeekleçıkardialog.alanlarıDoldur(
                    self.tableView_Model.sqldata[selIdx.row()][1:])
        elif self.ticlistframe.isVisible():
            if not 'C' in self.yetki:
                self.statusBar().showMessage('Bu işlem için yetkiniz yok')
                return
            #print("Ticlistframe'den seçildi")
            self.tableviewdansil_dialog = Tableviewdan_sildialog(self,selIdx.row())
            
    def table_customContextMenu(position):
        selIdxs = self.tableview.selectionModel().selectedIndexes()
        cmenu = QMenu()
        if self.stoklistframe.isVisible():
            if not 'B' in self.yetki:
                return
            if self.secilentabloadı == 'standart_malzemeler':
                if selIdxs:
                    cmenu.addAction(tableview_ekle_ctx_men_it)
                    cmenu.addAction(tableview_çıkar_ctx_men_it)
                    cmenu.addSeparator()
                cmenu.addAction(tableview_yeniekle_ctx_men_it)
                cmenu.addAction(tableview_sil_ctx_men_it)
            
        action = cmenu.exec_(self.tableview.mapToGlobal(position))
        print(__name__,"action:",action)
            
    def doubleClickedSlot(index):
        if self.ticlistframe.isVisible():
            openRelatedDialog(self,index)
        elif self.stoklistframe.isVisible():
            openRelatedDialog2(self,index)
        
    if any(x in self.yetki for x in ['A','B','C']):
        
        tableview_ekle_ctx_men_it = QAction("Bu kayıda ekle")
        tableview_ekle_ctx_men_it.triggered.connect(ekle_ctx_slot)
        
        tableview_çıkar_ctx_men_it = QAction("Bu kayıttan çıkar")
        tableview_çıkar_ctx_men_it.triggered.connect(çıkar_ctx_slot)
        
        tableview_yeniekle_ctx_men_it=QAction('Yeni Kayıt Ekle',self)
        tableview_yeniekle_ctx_men_it.triggered.connect(yeniekle_ctx_slot)
        #self.tableview.addAction(tableview_yeniekle_ctx_men_it)
        
        tableview_sil_ctx_men_it=QAction('Kayıt Sil',self)
        tableview_sil_ctx_men_it.triggered.connect(sil_ctx_slot)
        #self.tableview.addAction(tableview_sil_ctx_men_it)
        
        self.tableview.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableview.customContextMenuRequested.connect(table_customContextMenu)
        
        self.tableview.doubleClicked.connect(doubleClickedSlot)
        
        
    
#----------------------------------------------------------------------
    
    filterBoxYap(self)
    
    self.yantaraf_fr = QFrame()
    yantaraf_frlo = QVBoxLayout()
    yantaraf_frlo.addWidget(self.filterbox)
    yantaraf_frlo.addWidget(self.tableview)
    self.yantaraf_fr.setLayout(yantaraf_frlo)    
    

# def yeniKodEkle(self):
#     kodAddDlg = QDialog()
#     kodAddDlg.setWindowTitle("Kod Ekle")
#     kodAddDlg.setGeometry(100,100,200,100)
#     kodAddDlg.setModal(True)
#     layout = QGridLayout()
#     kodAddDlg.setLayout(layout)
#     
#     tm = self.tableView_Model
#     seçilen_tablonun_özellikleri = self.gösterilecek_tablo_bilgileri[tm.seçimNo]
# 
#     
#     resim = QLabel()
#     resim.setMaximumHeight(72)
#     path = os.path.join('images', seçilen_tablonun_özellikleri[2])
#     pic = QPixmap(path)
#     resim.setPixmap(pic)
#     layout.addWidget(resim,0,0)
#     kodAddDlg.show()
def filterBoxYap(self):
    self.filterbox = QGroupBox("Filtreler")
    #self.filterbox.setMinimumHeight(100)
    self.filterbox.filterFields = ('Tipi','Tip_Kodu','Boyutlar','Stok_Bölgesi',
                                   'stok_bölgesi_kodu','tip_kodu_adı',
                                   'Firma_Adı','Ad_Soyad')
    self.filterbox.fblo = QGridLayout()
    self.filterbox.setLayout(self.filterbox.fblo)
#     for i in range(3):
#         self.filterbox.fblo.addWidget(QLabel(str(i)+".LAbel:"),i,0)
#         self.filterbox.fblo.addWidget(QLineEdit(),i,1)
    
    
def addFilters(self):
    #----------- clear old widgets in filterbox -----------------
    widgetsayisi = self.filterbox.fblo.count()
    #print("widgetsayisi:",widgetsayisi)
    items = [self.filterbox.fblo.itemAt(i) for i in range(widgetsayisi)]
    #print("items's type:",items.__class__)
    for w in items:
        widget = w.widget()
        #print(widget)
        self.filterbox.fblo.removeWidget(widget)
        widget.hide()
        del widget
        del w
    self.filterbox.edits = {}
    #-------------------------------------------------------------
    tm = self.tableView_Model
    seçilen_tablonun_özellikleri = self.gösterilecek_tablo_bilgileri[tm.seçimNo]
    seçilen_tablo_dbAdı = seçilen_tablonun_özellikleri[1]
    
    column_bilgileri = tm.sqlheader.copy()  # HATA ENGELLENDİ !!! (CRASH !!!)
    #print("Seçilen Tablo:",seçilen_tablonun_özellikleri[1])
    
    #print(column_bilgileri)
    del column_bilgileri[0] # remove the id column attributes from here (not later)
    columnNames = [a[0] for a in column_bilgileri]
    #print("columnNames:",columnNames)
    #addDlg.columnLineEdits = [];
    columnTypes = [a[1] for a in column_bilgileri]  #hepsi varchar olduğu için şimdilik
                                                        #kullanmıyoruz
    #print("TYPEEEES:",columnTypes)
    
    def filterTextChangedSlot(text):
        sqlcolumnnames=[]
        sqllikevals=[]
#         print("*************** filterboxslot**************",len(self.filterbox.edits))
#         print("seçilen_tablo_dbAdı:",seçilen_tablo_dbAdı)
        for k,v in self.filterbox.edits.items():
            #print("key,value:",k,v.text())
            if v.text():
                sqlcolumnnames.append(k)
                liketext = v.text().strip()
                liketext = liketext.upper()
                sqllikevals.append("%"+ liketext +"%")
        if not sqlcolumnnames:
            tm.setTable(seçilen_tablo_dbAdı)
            return
        cmd="SELECT * FROM {} WHERE ".format(seçilen_tablo_dbAdı)
        cond=''
        for i,col in enumerate(sqlcolumnnames):
            if cond:
                cond += " AND "
            cond += col + " LIKE '" + sqllikevals[i] + "'"
        cmd += cond
        #print("*** SQL Clause :",cmd)
        tm.setSQLData(cmd)
        
            
    ind = 0
    for colname in columnNames:
        #print("ind,colname:",ind,colname)
        if colname in self.filterbox.filterFields:            
            self.filterbox.fblo.addWidget(QLabel(colname),ind,0)
            #print("colname in if:",colname,"ind:",ind)
            colfltedit = QLineEdit()
            colfltedit.textChanged.connect(filterTextChangedSlot)
            self.filterbox.fblo.addWidget(colfltedit,ind,1)
            self.filterbox.edits[colname]=colfltedit
            ind += 1