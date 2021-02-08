'''
Created on 8 Ara 2020

@author: user
'''
from PyQt5.QtWidgets import QAction
import sys
from Cest_Factory.Ekle_Cikar_UI import MalzemeEkleÇıkarDailog,\
                TicListEkleDialog,TicListSilDialog
from Cest_Factory.standart_malzemeler.yeni_ekle import yeni_ekle_sil_gui
from Cest_Factory.tipler_kodlar.tipler_kodlar_yeni_ekle_sil import tipler_kodlar_yeni_ekle_sil_gui
from Cest_Factory.tabloaktar import civataları_aktar, alyanları_aktar,\
    havşaları_aktar, setiskurları_aktar, somunları_aktar, rulmanları_aktar


class MyClass(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        
def menüyap(self):
    self.anamenü=self.menuBar()
    menu_dosya = self.anamenü.addMenu("Dosya")
    menu_düzenle = self.anamenü.addMenu("Düzenle")
    menu_araçlar = self.anamenü.addMenu("Araçlar")
    menu_yardım = self.anamenü.addMenu("Yardım")
    
    def çıkış_menuAction():
        print("Programdan menü vasıtasıyla çıkıldı...")
        if self.db.isOpen():
            self.db.close()
        sys.exit()
    çıkış_menu_item=QAction('Çıkış',self)
    çıkış_menu_item.triggered.connect(çıkış_menuAction)
    menu_dosya.addAction(çıkış_menu_item)
    
    def profilim_menuAction():
        self.yantaraf_fr.hide()
        self.prf.show()
    self.profilim_menu_item=QAction('Profilim',self)
    self.profilim_menu_item.triggered.connect(profilim_menuAction)
    menu_düzenle.addAction(self.profilim_menu_item)

    def ekle_menuAction():
        tablename = self.tableView_Model.tablename
        if not tablename:# type(model).__name__=='QSqlTableModel':
            #print("Tablo yooook")
            self.statusBar().showMessage('Tablo Seçilmedi')
        else:
            if self.stoklistframe.isVisible():
                if not 'B' in self.yetki:
                    self.statusBar().showMessage('Bu işlem için yetkiniz yok')
                    return
                #print("TabloListFrame'den seçildi")
#                 selidxs = self.stokListView.selectionModel().selectedIndexes()
#                 if not selidxs:# type(model).__name__=='QSqlTableModel':
#                     #print("Tablo yooook")
#                     self.statusBar().showMessage('Tablo Seçilmedi')
#                     return
#                 row = selidxs[0].row()
#                 seçilenListItemName = self.stokListView_Model.tablobilgileri[row][0]
                if self.secilentabloadı =='standart_malzemeler':
                    self.standart_malzeme_gui = yeni_ekle_sil_gui(self,'ekle')
                elif self.secilentabloadı in ('malzeme_tipleri','tip_kodlari',
                                              'stok_bölgesi_kodlari'):
                    self.tipler_kodlar_gui = tipler_kodlar_yeni_ekle_sil_gui(self,'ekle')
                else:
                    self.EkleCikardialog = MalzemeEkleÇıkarDailog(self,'ekle')
                    
            elif self.ticlistframe.isVisible():
                if not 'C' in self.yetki:
                    self.statusBar().showMessage('Bu işlem için yetkiniz yok')
                    return
                #print("Ticlistframe'den seçildi")
                selidxs = self.ticListView.selectionModel().selectedIndexes()
                if not selidxs:# type(model).__name__=='QSqlTableModel':
                    #print("Tablo yooook")
                    self.statusBar().showMessage('Tablo Seçilmedi')
                    return
                row = selidxs[0].row()
                seçilenListItemName = self.ticListView_Model.tablobilgileri[row][0]
                #print(row,seçilenListItemName)
                if seçilenListItemName in ('Müşteriler','Tedarikçiler','Kişiler'):
                    self.ticlistekledialog = TicListEkleDialog(self)

    def sil_menuaction():
        tablename = self.tableView_Model.tablename
        if not tablename:# type(model).__name__=='QSqlTableModel':
            #print("Tablo yooook")
            self.statusBar().showMessage('Tablo Seçilmedi')
        else:
            if self.stoklistframe.isVisible():
                if not 'B' in self.yetki:
                    self.statusBar().showMessage('Bu işlem için yetkiniz yok')
                    return
                #print("TabloListFrame'den seçildi")
#                 selidxs = self.stokListView.selectionModel().selectedIndexes()
#                 row = selidxs[0].row()
#                 seçilenListItemName = self.stokListView_Model.tablobilgileri[row][0]

                if self.secilentabloadı =='standart_malzemeler':
                    self.standart_malzeme_gui = yeni_ekle_sil_gui(self,'sil')
                elif self.secilentabloadı in ('malzeme_tipleri','tip_kodlari',
                                              'stok_bölgesi_kodlari'):
                    self.tipler_kodlar_gui = tipler_kodlar_yeni_ekle_sil_gui(self,'sil')
                else:
                    self.EkleCikardialog = MalzemeEkleÇıkarDailog(self,'çıkar')
            elif self.ticlistframe.isVisible():
                if not 'C' in self.yetki:
                    self.statusBar().showMessage('Bu işlem için yetkiniz yok')
                    return
                selidxs = self.ticListView.selectionModel().selectedIndexes()
                if not selidxs:# type(model).__name__=='QSqlTableModel':
                    #print("Tablo yooook")
                    self.statusBar().showMessage('Tablo Seçilmedi')
                    return
                row = selidxs[0].row()
                seçilenListItemName = self.ticListView_Model.tablobilgileri[row][0]
                #print(row,seçilenListItemName)
                if seçilenListItemName in ('Müşteriler','Tedarikçiler','Kişiler'):
                    self.ticlistsildialog = TicListSilDialog(self)

    if any(x in self.yetki for x in ['A','B','C']):
        self.yenikayıtekle_mi=QAction('Seçilen Tabloya Kayıt Ekle',self)
        self.yenikayıtekle_mi.triggered.connect(ekle_menuAction)
        menu_düzenle.addAction(self.yenikayıtekle_mi)
        self.kayıtsil_mi= QAction('Seçilen Tablodan Kayıt Sil',self)
        self.kayıtsil_mi.triggered.connect(sil_menuaction)
        menu_düzenle.addAction(self.kayıtsil_mi)
        
    if 'A' in self.yetki:
        civatalaraktar=QAction('Civatalar Aktar',self)
        civatalaraktar.triggered.connect(lambda : civataları_aktar(self,menu_araçlar,civatalaraktar))
        menu_araçlar.addAction(civatalaraktar)
        
        alyanlaraktar=QAction('Alyan Civatalar Aktar',self)
        alyanlaraktar.triggered.connect(lambda : alyanları_aktar(self,menu_araçlar,alyanlaraktar))
        menu_araçlar.addAction(alyanlaraktar)
        
        havşalaraktar=QAction('Havşa Civatalar Aktar',self)
        havşalaraktar.triggered.connect(lambda : havşaları_aktar(self,menu_araçlar,havşalaraktar))
        menu_araçlar.addAction(havşalaraktar)
        
        setiskuraktar=QAction('setiskurları Aktar',self)
        setiskuraktar.triggered.connect(lambda : setiskurları_aktar(self,menu_araçlar,setiskuraktar))
        menu_araçlar.addAction(setiskuraktar)
        
        somunlaraktar=QAction('somunları Aktar',self)
        somunlaraktar.triggered.connect(lambda : somunları_aktar(self,menu_araçlar,somunlaraktar))
        menu_araçlar.addAction(somunlaraktar)
        
        rulmanlarıaktar=QAction('rulmanları Aktar',self)
        rulmanlarıaktar.triggered.connect(lambda : rulmanları_aktar(self,menu_araçlar,rulmanlarıaktar))
        menu_araçlar.addAction(rulmanlarıaktar)
