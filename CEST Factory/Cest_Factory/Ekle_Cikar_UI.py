'''
Created on 1 Ara 2020

@author: Barış Kılıçlar
'''
import os
from PyQt5.QtWidgets import QDialog,QGridLayout,QLabel,QLineEdit,QMessageBox,\
        QPushButton,QFrame,QHBoxLayout,QApplication, QVBoxLayout, QFormLayout,\
    QListView
from PyQt5.QtGui import QPixmap,QFont, QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
from PyQt5.Qt import QWidget

ürün_tabloları = 'rulmanlar', 'civatalar', 'somunlar','setiskurlar'
kod_tabloları = 'tip_kodlari','stok_bölgesi_kodlari'
non_Null_fields = 'Boyutlar','Adet','tip_kodu_adı','stok_bölgesi_kodu'
equality_check_fields = 'Tip_Kodu','Boyutlar','Stok_Bölgesi'

class MalzemeEkleÇıkarDailog(QDialog):
    '''
    classdocs
    '''

    def __init__(self, anapencere,eklecikar):
        '''
        Constructor
        '''
        super().__init__()
        self.anapencere = anapencere
        self.eklecikar = eklecikar
                
#         print("self:",self)
#         print("self tipi:",self.__class__)

        self.gerekliBilgileriAl()        
        
        self.dialogUIoluştur()
        
        self.show()
        
    def gerekliBilgileriAl(self):
        tm = self.anapencere.tableView_Model
        seçilen_tablonun_özellikleri = self.anapencere.gösterilecek_tablo_bilgileri[tm.seçimNo]
        #print(seçilen_tablonun_özellikleri)
        self.seçilitablo_showname = seçilen_tablonun_özellikleri[0]
        self.seçilitablo_dbname = seçilen_tablonun_özellikleri[1]
        self.seçilitablo_iconfile =  seçilen_tablonun_özellikleri[2]
        cmd= "SHOW COLUMNS FROM {}".format(self.seçilitablo_dbname)
        #print(cmd)
        self.seçilitablo_sqlcolumndata = self.anapencere.stok_dbm.executeCmd(cmd)
        #print("self.seçilitablo_sqlcolumndata:",self.seçilitablo_sqlcolumndata)
        self.colnames = [a[0] for a in self.seçilitablo_sqlcolumndata[1:]]
        #print("self.colnames:",self.colnames)
        self.coltypes = [a[1].decode() for a in self.seçilitablo_sqlcolumndata[1:]]
        #print("self.coltypes:",self.coltypes)
        self.idcolname = self.seçilitablo_sqlcolumndata[0][0]
        #print("id_column_name________:",id_column_name)
        cmd = 'SELECT tip_kodu_adı FROM tip_kodlari'
        sqlans = self.anapencere.stok_dbm.executeCmd(cmd)
        self.tipkodları = [a[0] for a in sqlans]
        #print("self.tipkodları:",self.tipkodları)
        cmd = 'SELECT stok_bölgesi_kodu FROM stok_bölgesi_kodlari'
        sqlans = self.anapencere.stok_dbm.executeCmd(cmd)
        self.stokbölgesikodları = [a[0] for a in sqlans]
        #print("self.stokbölgesikodları:",self.stokbölgesikodları)
        
    def dialogUIoluştur(self):
        if self.eklecikar == 'ekle':
            self.setWindowTitle("Ekle")
            #self.setStyleSheet("background-color: green;") 
        elif self.eklecikar == 'çıkar':
            self.setWindowTitle("Çıkar")
            #self.setStyleSheet("background-color: red;") 
            
        self.setGeometry(100,100,200,100)
        self.setModal(True)
        
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        
        self.dialogResminiEkle()
        
        self.dialogBaşlığınıEkle()
        
        self.dialogLabelveLineEditleriEkle()
        
        self.dialogButtonlarıEkle()
        
        self.dialogMoveCenter()
        
    def dialogResminiEkle(self):
        resim = QLabel()
        resim.setMaximumHeight(72)
        path = os.path.join('images',self.seçilitablo_iconfile)
        pic = QPixmap(path)
        resim.setPixmap(pic)
        self.layout.addWidget(resim,0,0)
        
    def dialogBaşlığınıEkle(self):
        if self.eklecikar == 'ekle':
            changetext = " TABLOSUNA EKLE"
        elif self.eklecikar == 'çıkar':
            changetext = " TABLOSUNDAN ÇIKAR"
        başlık = QLabel(self.seçilitablo_showname+changetext)
        başlık.setStyleSheet('color: darkblue;')
        başlık.setFont(QFont('Arial', 10,QFont.Bold))
        self.layout.addWidget(başlık,0,1,Qt.AlignHCenter)
        
    def dialogLabelveLineEditleriEkle(self):
        self.lineEdits = []
        for ind,colname in enumerate(self.colnames):
            self.layout.addWidget(QLabel(colname),ind+1,0)
            lineEdit = QLineEdit()
            self.layout.addWidget(lineEdit,ind+1,1)
            self.lineEdits.append(lineEdit)
        self.message = QLabel("")
        self.message.setStyleSheet('color: red;')
        self.layout.addWidget(self.message,ind+2,0,1,2)
        self.layout.lastrowindex = ind+2    #new variable attach to object (layout)
        if self.eklecikar == 'ekle':
            self.lineEditSlotsAndConnectionsforEkle()
        elif self.eklecikar == 'çıkar':
            self.lineEditSlotsAndConnectionsforÇıkar()
        
    def dialogButtonlarıEkle(self):
        iptalbtn = QPushButton("İptal")
        iptalbtn.clicked.connect(self.iptalbtn_call)
        
        self.kaydetbtn = QPushButton()
        if self.eklecikar == 'ekle':
            self.kaydetbtn.setText("Ekle")
            #self.kaydetbtn.setStyleSheet("color:white;background-color: green;") 
        elif self.eklecikar == 'çıkar':
            self.kaydetbtn.setText("Çıkar")
            #self.kaydetbtn.setStyleSheet("color:white;background-color: red;")        
        self.kaydetbtn.setEnabled(False)
        self.kaydetbtn.clicked.connect(self.kaydetbtn_call)
        gb=QFrame()
        #gb.setFrameStyle(QFrame.NoFrame)
        gblo = QHBoxLayout()
        gb.setLayout(gblo)
        gblo.addWidget(iptalbtn)
        gblo.addWidget(self.kaydetbtn)
        self.layout.addWidget(gb,self.layout.lastrowindex+1,1)
        
    def dialogMoveCenter(self):
        screenCenter=QApplication.desktop().availableGeometry().center()
        myrect=self.frameGeometry()
        myrect.moveCenter(screenCenter)
        self.move(myrect.topLeft())
        
    def lineEditSlotsAndConnectionsforEkle(self):
        
        self.tipKoduProper = True
        def TipKoduCheckSlot(text):
            #print("TipKoduCheckSlot")
            
            text = text.strip()
            text = text.upper()
            #print(text)
            if text and text not in self.tipkodları:
                #print("Yok:",text) 
                self.message.setText("'" + text + "'"
                                       " Tip Kodu Bulunamadı")
                self.tipKoduProper = False
            else:
                #print("Var:",text)
                self.message.setText('')
                self.tipKoduProper = True
            #print("tipKoduProper",tipKoduProper)
            multipleEditscheckSlot(text)
        
        self.stokBölgesiProper = True
        def StokBölgesiCheckSlot(text):            
            text = text.strip()
            text = text.upper()
            if text and text not in self.stokbölgesikodları:
                #print("Yok:",text) 
                self.message.setText("'" + text + "'"
                                       " Stok Bölgesi Kodu Bulunamadı")
                self.stokBölgesiProper = False
            else:
                #print("Var:",text)
                self.message.setText('')
                self.stokBölgesiProper = True
            multipleEditscheckSlot(text)
        
        self.tipKoduAdıProper = True
        def tipKoduAdıCheckSlot(text):
            text = text.strip()
            text = text.upper()
            if not text:
                self.message.setText('')
                self.tipKoduAdıProper = False
            elif text in self.tipkodları:
                self.message.setText("'" + text + "'"
                                       " Tip Kodu Zaten Var")
                self.tipKoduAdıProper = False
            else:
                self.message.setText('')
                self.tipKoduAdıProper = True
            multipleEditscheckSlot(text)
            
        self.stokBölgesiKoduProper = True  # False ??
        def stokBölgesiKoduCheckSlot(text):
            
            text = text.strip()
            text = text.upper()
            if not text:
                self.message.setText('')
                self.stokBölgesiKoduProper = False
            elif text in self.stokbölgesikodları:
                self.message.setText("'" + text + "'"
                                       " Stok Bölgesi Kodu Zaten Var")
                self.stokBölgesiKoduProper = False
            else:
                self.message.setText('')
                self.stokBölgesiKoduProper = True
            multipleEditscheckSlot(text)
            
        def multipleEditscheckSlot(text):
            self.kaydetbtn.setEnabled(self.areLineEditContentsProper())
            
#         def areLineEditContentsProper():
#     #         print("areLineEditContentsProper tipKoduProper:",tipKoduProper)
#     #         print("areLineEditContentsProper stokBölgesiProper:",stokBölgesiProper)
#     #         print("areLineEditContentsProper tipKoduAdıProper:",tipKoduAdıProper)
#     #         print("areLineEditContentsProper stokBölgesiKoduProper:",stokBölgesiKoduProper)
#             if not(self.tipKoduProper and 
#                    self.stokBölgesiProper and 
#                    self.tipKoduAdıProper and 
#                    self.stokBölgesiKoduProper):
#                 return False
#             for idx,le in enumerate(self.lineEdits):
#                 colname = self.colnames[idx]
#                 #check Non-null-ness >>>>>>>>>>>>>
#                 if colname in non_Null_fields:
#                     if not le.text():
#                         return False
#             return True
        
        for ind,colname in enumerate(self.colnames):
        
            if colname == 'Tip_Kodu':
                self.lineEdits[ind].textChanged.connect(TipKoduCheckSlot)
            elif colname == 'Stok_Bölgesi':
                self.lineEdits[ind].textChanged.connect(StokBölgesiCheckSlot)
            elif colname == 'tip_kodu_adı':
                self.lineEdits[ind].textChanged.connect(tipKoduAdıCheckSlot)
            elif colname == 'stok_bölgesi_kodu':
                self.lineEdits[ind].textChanged.connect(stokBölgesiKoduCheckSlot)
            else:
                self.lineEdits[ind].textChanged.connect(multipleEditscheckSlot)
                #Kaydet butonunu enable/disable için

        
        
    def lineEditSlotsAndConnectionsforÇıkar(self):
        
        if self.seçilitablo_dbname in ürün_tabloları:
            cmd = "SELECT DISTINCT Tip_Kodu FROM {} ".format(self.seçilitablo_dbname)
            msg = self.anapencere.stok_dbm.executeCmd(cmd)
            print("select distinct tip_kodu:",msg)
            seçilitablodakitipkodları = [a[0] for a in msg]
            print("seçilitablodakitipkodları:",seçilitablodakitipkodları)
            
            cmd = "SELECT DISTINCT Stok_Bölgesi FROM {} ".format(self.seçilitablo_dbname)
            msg = self.anapencere.stok_dbm.executeCmd(cmd)
            print("select distinct stok_bölgesi:",msg)
            seçilitablodakistokbölgeleri = [a[0] for a in msg]
            print("seçilitablodakistokbölgeleri:",seçilitablodakistokbölgeleri)
        
        self.tipKoduProper = True
        def TipKoduCheckSlot(text):
            #print("TipKoduCheckSlot")
            
            text = text.strip()
            text = text.upper()
            #print(text)
            if text and text not in seçilitablodakitipkodları:
                #print("Yok:",text) 
                self.message.setText("'" + text + "'"
                                       " Tip Kodu Bulunamadı")
                self.tipKoduProper = False
            else:
                #print("Var:",text)
                self.message.setText('')
                self.tipKoduProper = True
            #print("tipKoduProper",tipKoduProper)
            multipleEditscheckSlot(text)
        
        self.stokBölgesiProper = True
        def StokBölgesiCheckSlot(text):            
            text = text.strip()
            text = text.upper()
            if text and text not in seçilitablodakistokbölgeleri:
                #print("Yok:",text) 
                self.message.setText("'" + text + "'"
                                       " Stok Bölgesi Kodu Bulunamadı")
                self.stokBölgesiProper = False
            else:
                #print("Var:",text)
                self.message.setText('')
                self.stokBölgesiProper = True
            multipleEditscheckSlot(text)
        
        self.tipKoduAdıProper = True
        def tipKoduAdıCheckSlot(text):
            text = text.strip()
            text = text.upper()
            if not text:
                self.message.setText('')
                self.tipKoduAdıProper = False
            elif text in self.tipkodları:
                self.message.setText('')
                self.tipKoduAdıProper = True
            else:
                self.message.setText("'" + text + "'"
                                       " Tip Kodu Bulunamadı")                
                self.tipKoduAdıProper = False
            multipleEditscheckSlot(text)
            
        self.stokBölgesiKoduProper = True
        def stokBölgesiKoduCheckSlot(text):
            
            text = text.strip()
            text = text.upper()
            if not text:
                self.message.setText('')
                self.stokBölgesiKoduProper = False

            elif text in self.stokbölgesikodları:
                self.message.setText('')
                self.stokBölgesiKoduProper = True
                
            else:
                self.message.setText("'" + text + "'"
                                       " Stok Bölgesi Kodu Bulunamadı")
                self.stokBölgesiKoduProper = False
            multipleEditscheckSlot(text)
            
        def multipleEditscheckSlot(text):
            self.kaydetbtn.setEnabled(self.areLineEditContentsProper())
            
        for ind,colname in enumerate(self.colnames):
        
            if colname == 'Tip_Kodu':
                self.lineEdits[ind].textChanged.connect(TipKoduCheckSlot)
            elif colname == 'Stok_Bölgesi':
                self.lineEdits[ind].textChanged.connect(StokBölgesiCheckSlot)
            elif colname == 'tip_kodu_adı':
                self.lineEdits[ind].textChanged.connect(tipKoduAdıCheckSlot)
            elif colname == 'stok_bölgesi_kodu':
                self.lineEdits[ind].textChanged.connect(stokBölgesiKoduCheckSlot)
            else:
                self.lineEdits[ind].textChanged.connect(multipleEditscheckSlot)
                #Kaydet butonunu enable/disable için
            
    def areLineEditContentsProper(self):
#         print("areLineEditContentsProper tipKoduProper:",tipKoduProper)
#         print("areLineEditContentsProper stokBölgesiProper:",stokBölgesiProper)
#         print("areLineEditContentsProper tipKoduAdıProper:",tipKoduAdıProper)
#         print("areLineEditContentsProper stokBölgesiKoduProper:",stokBölgesiKoduProper)
        if not(self.tipKoduProper and 
               self.stokBölgesiProper and 
               self.tipKoduAdıProper and 
               self.stokBölgesiKoduProper):
            return False
        for idx,le in enumerate(self.lineEdits):
            colname = self.colnames[idx]
            #check Non-null-ness >>>>>>>>>>>>>
            if colname in non_Null_fields:
                if not le.text():
                    return False
        return True
        

        
    def iptalbtn_call(self):
        self.done(QDialog.Rejected)

    def kaydetbtn_call(self):

        def checkLineEditsforNonNullFields():
            #print("İşte, burdaa")
            for ind,col in enumerate(self.colnames):
                if col in non_Null_fields:
                    if not vals[ind]: #isEmpty - Check !!
                        QMessageBox.warning(self,"Uyarı",
                                            col + " boş bırakılamaz !!", 
                                            QMessageBox.Ok)
                        print(col,"boş bırakılamaz !!")
                        return False
            return True
        
        def convertToSQLValues():            
            def makeUniformSQLTableText(text):
                result = text.strip()
                result = result.upper()
                result = "'" + result + "'"
                return result
            #print("convertToSQLValues vals_______________:",vals)
            for i,v in enumerate(vals):
                #print("self.coltypes[i] :",self.coltypes[i])
                if self.coltypes[i].startswith('varchar'):
                    vals[i]=makeUniformSQLTableText(v)
                if v:
                    existing_values.append(vals[i])
                    existing_colnames.append(self.colnames[i])
                    #existing_coltypes.append(addDlg.columnTypes[i].decode())
#             print("<<< vals >>>:",vals)
            #print("/// existing_values \\\:",existing_values) 
#                     #Görüntülemek Önemli !!! yanlış olabilir
            #print("/// existing_colnames \\\:",existing_colnames)


        def insertInto():
            cmd = "INSERT INTO {} (".format(self.seçilitablo_dbname)
            cmd += ",".join(existing_colnames)
            cmd += ") VALUES ("                
            cmd += ",".join(existing_values) + ")"
            self.anapencere.stok_dbm.executeCmd(cmd)
            self.anapencere.tableView_Model.setTable(self.seçilitablo_dbname)  # for tableview refresh
            
            
        def checkForMatchingRecord():
            cmd = "SELECT * FROM {} WHERE ".format(self.seçilitablo_dbname)
            #     SELECT Adet FROM .... ?  (id gerekebilir ve her tabloda id adı ayrı)
            cond = ''
            for i,coln in enumerate(self.colnames):#existing_colnames):
                                    # Bu yukardaki Cestte uygulamada değişebilecek bi seçim
                if coln in ('Adet','Açıklama'):
                    continue
                if cond:
                    cond += ' AND '
                if vals[i] == "''":             # Bu Cestte uygulamada değişebilecek bi seçim
                    cond += coln + " IS NULL"
                else:
                    cond += coln + " = " + vals[i] #existing_values[i]
            cmd += cond
            #print("**** cmd:",cmd)
            msg = self.anapencere.stok_dbm.executeCmd(cmd)
            #print("SQL reply:",msg)
            return msg
        
        def increaseAdetofMatchingRecord(matchingRecord):
            ai = self.colnames.index('Adet') # arrayindex for adet index
            varolanadet = matchingRecord[ai+1] # +1, id column'u atlamak için..
            print("Adet şu mu:", varolanadet, "   --tipi:",varolanadet.__class__)
            cmd = ("UPDATE {} ".format(self.seçilitablo_dbname) +
                   "SET Adet = {} ".format(varolanadet + int(vals[ai])) +
                   "WHERE {id_column_name} = {id}". format(
                        id_column_name = self.idcolname,
                        id = matchingRecord[0]))
            print("**** update cmd:",cmd)
            self.anapencere.stok_dbm.executeCmd(cmd)
            self.anapencere.tableView_Model.setTable(self.seçilitablo_dbname)  # for tableview refresh
            self.anapencere.tableView_Model.setYellowRowFromIdColumnValue(matchingRecord[0])
            
        def deleteWhereID(idnum):
            cmd = "DELETE FROM {} ".format(self.seçilitablo_dbname)
            cmd += "WHERE {0} = {1}".format(self.idcolname,idnum)
            self.anapencere.stok_dbm.executeCmd(cmd)
            self.anapencere.tableView_Model.setTable(self.seçilitablo_dbname)  # for tableview refresh
            
        def decreaseAdetofMatchingRecord(matchingRecord):
            ai = self.colnames.index('Adet') # ai for adet index
            varolanadet = matchingRecord[ai+1] # +1, id column'u atlamak için..
            print("Adet şu mu:", varolanadet, "   --tipi:",varolanadet.__class__)
            çıkarAdet = int(vals[ai])
            if varolanadet == çıkarAdet:
                deleteWhereID(matchingRecord[0])
            else:
                cmd = ("UPDATE {} ".format(self.seçilitablo_dbname) +
                       "SET Adet = {} ".format(varolanadet - int(vals[ai])) +  # - işareti
                       "WHERE {id_column_name} = {id}". format(
                            id_column_name = self.idcolname,
                            id = matchingRecord[0]))
                print("**** update cmd:",cmd)
                self.anapencere.stok_dbm.executeCmd(cmd)
                self.anapencere.tableView_Model.setTable(self.seçilitablo_dbname)  # for tableview refresh
                self.anapencere.tableView_Model.setYellowRowFromIdColumnValue(matchingRecord[0])
            
        def ekle():            
            if self.seçilitablo_dbname in kod_tabloları:
                insertInto()
            elif self.seçilitablo_dbname in ürün_tabloları:
                matchingRecords = checkForMatchingRecord()
                if not matchingRecords:
                    insertInto()
                else:
                    increaseAdetofMatchingRecord(matchingRecords[0]) #add to first matching record
            else:
                insertInto() # Müşteriler, Tedarikçiler, Kişiler

        def çıkar():
            if self.seçilitablo_dbname in kod_tabloları:
#                 cmd = ('SELECT * FROM {tablename} '.format(tablename = self.seçilitablo_dbname) +
#                        'WHERE '
#                        )
                matchingRecords =checkForMatchingRecord()
                deleteWhereID(matchingRecords[0][0]) #delete first found record (Tüm Kayıtları?)
                
            elif self.seçilitablo_dbname in ürün_tabloları:
                matchingRecords = checkForMatchingRecord()
                if not matchingRecords:
                    print("Böyle Bir Kayıt Bulunamadı !!! QMessageBox")
                    QMessageBox.warning(self,"Uyarı",
                                            "Böyle Bir Kayıt Bulunamadı !!!", 
                                            QMessageBox.Ok)
                else:
                    decreaseAdetofMatchingRecord(matchingRecords[0])


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                button call burada başlıyor
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        vals = [le.text() for le in self.lineEdits]
        #print(vals)
        if not checkLineEditsforNonNullFields():
            return
        
        existing_values = []
        existing_colnames =[]
        convertToSQLValues()
        #print("--- SQL Vals ---:",vals)
        
        if not existing_values:
            return   #----------------- (bi şekilde) hiç değer girilmemişse, çık git
        
        if self.eklecikar == 'ekle':
            ekle()
        elif self.eklecikar == 'çıkar':
            çıkar()
        

        
        self.done(QDialog.Accepted)
    
    def alanlarıDoldur(self,alanlar):
        print(self.lineEdits)
        print(alanlar)
        for i,arg in enumerate(alanlar):
            if self.colnames[i] != 'Adet':
                self.lineEdits[i].setText(arg)
            else:
                self.lineEdits[i].setFocus()

class TicListEkleDialog(QDialog):
    def __init__(self, anapencere, **kwargs):
        '''
        Constructor
        '''
        super().__init__()
        self.anapencere = anapencere
        self.kwargs = kwargs
        self.bilgileriAl()
        self.dialogUIoluştur()
        self.dialogMoveCenter()
        if 'called_from' in kwargs:
            if kwargs['called_from']=='ticdialogs_müşdzn_kşekle':
                self.alanlarıdoldur(kwargs['firma_adı'])
        self.show()
        
    def bilgileriAl(self):
        tm = self.anapencere.tableView_Model            
        if 'called_from' in self.kwargs:
            if self.kwargs['called_from']=='ticdialogs_müşdzn_kşekle':
                seçilitablobilgileri = self.anapencere.gösterilecek_tablo_bilgileri[2] #2= Kişiler
        else:
            seçilitablobilgileri = self.anapencere.gösterilecek_tablo_bilgileri[tm.seçimNo]
        self.seçilitablo_gösterilenAd = seçilitablobilgileri[0]
        self.seçilitablo_dbTableName = seçilitablobilgileri[1]
        self.seçilitablo_iconfilename = seçilitablobilgileri[2]
        cmd= "SHOW COLUMNS FROM {}".format(self.seçilitablo_dbTableName)
        #print(cmd)
        self.seçilitablo_sqlcolumndata = self.anapencere.stok_dbm.executeCmd(cmd)
        #print("self.seçilitablo_sqlcolumndata:",self.seçilitablo_sqlcolumndata)
        self.colnames = [a[0] for a in self.seçilitablo_sqlcolumndata[1:]]
        #print("self.colnames:",self.colnames)
        self.coltypes = [a[1].decode() for a in self.seçilitablo_sqlcolumndata[1:]]
        #print("self.coltypes:",self.coltypes)
        self.idcolname = self.seçilitablo_sqlcolumndata[0][0]
        #print("id_column_name________:",self.idcolname)
        
        self.adlar = [data[1] for data in self.anapencere.tableView_Model.sqldata]
        #print(self.adlar)
        
    def dialogUIoluştur(self):
        if self.seçilitablo_gösterilenAd == "Müşteriler":
            self.setWindowTitle("Yeni Müşteri Ekle")
            başlıkLabel = QLabel("YENİ MÜŞTERİ EKLE")
        elif self.seçilitablo_gösterilenAd == "Tedarikçiler":
            self.setWindowTitle("Yeni Tedarikçi Ekle")
            başlıkLabel = QLabel("YENİ TEDARİKÇİ EKLE")
        elif self.seçilitablo_gösterilenAd == "Kişiler":
            self.setWindowTitle("Yeni Kişi Ekle")
            başlıkLabel = QLabel("YENİ KİŞİ EKLE")
        
        
        self.setGeometry(100,100,400,350)
        self.setModal(True)
        
        başlıkLabel.setStyleSheet('color: green;')
        başlıkLabel.setFont(QFont('Arial', 12,QFont.Bold))
        
        mainvboxlayout = QVBoxLayout()
        self.setLayout(mainvboxlayout)
        
        başlıkhbox = QHBoxLayout()
        başlıkhbox.addWidget(self.dialogResimLabelOluştur())
        başlıkhbox.addStretch()
        başlıkhbox.addWidget(başlıkLabel)
        başlıkhbox.addStretch()
        
        mainvboxlayout.addLayout(başlıkhbox)
        
        mainvboxlayout.addSpacing(20)
        
        layout = QFormLayout()
        
        self.lineEdits=[]
        for i,col in enumerate(self.colnames):
            label = QLabel(col)
            lineEdit = QLineEdit()
            if i==0:
                lineEdit.textChanged.connect(self.AdCheckSlot)
            layout.addRow(label, lineEdit)
            self.lineEdits.append(lineEdit)
        
#         firmaAdıLabel = QLabel("Firma Adı:")
#         layout.addWidget(firmaAdıLabel)
#         self.firmaAdıLineEdit = QLineEdit()
#         layout.addWidget(self.firmaAdıLineEdit,lineNo,1)
#         self.firmaAdıLineEdit.textChanged.connect(self.firmaAdiCheckSlot)
        
                
        mainvboxlayout.addLayout(layout)
        mainvboxlayout.addStretch()
        
        hboxlayout = QHBoxLayout()
        hboxlayout.addStretch()
        
        iptalbtn = QPushButton("İptal")
        iptalbtn.clicked.connect(self.iptalbtn_call)
        hboxlayout.addWidget(iptalbtn)
        
        self.eklebtn = QPushButton("Ekle")
        self.eklebtn.clicked.connect(self.eklebtn_call)
        self.eklebtn.setEnabled(False)
        hboxlayout.addWidget(self.eklebtn)
        
        mainvboxlayout.addLayout(hboxlayout)
        
        self.hataLabel = QLabel()
        self.hataLabel.setStyleSheet('color: red;')
        mainvboxlayout.addWidget(self.hataLabel)
    
    def AdCheckSlot(self,text):
        if not text:
            self.hataLabel.setText("Ad Boş Bırakılamaz !!")
            self.eklebtn.setEnabled(False)
        elif text.strip().upper() in self.adlar:
            self.hataLabel.setText("Bu adda kayıt zaten var !!")
            self.eklebtn.setEnabled(False)
        else:
            self.hataLabel.setText("")
            self.eklebtn.setEnabled(True)
            
    def dialogResimLabelOluştur(self):
        resim = QLabel()
        resim.setMaximumHeight(72)
        path = os.path.join('images', self.seçilitablo_iconfilename)
        pic = QPixmap(path)
        resim.setPixmap(pic)
        return resim
        
    def dialogMoveCenter(self):
        screenCenter=QApplication.desktop().availableGeometry().center()
        myrect=self.frameGeometry()
        myrect.moveCenter(screenCenter)
        self.move(myrect.topLeft())
        
    def iptalbtn_call(self):
        self.done(QDialog.Rejected)
        
    def eklebtn_call(self):        
        values = []
        for i,le in enumerate(self.lineEdits):
            if i==0:
                values.append("'"+le.text().strip().upper()+"'")
            else:
                values.append("'"+le.text().strip()+"'")
        
        cmd = "INSERT INTO {} (".format(self.seçilitablo_dbTableName)
        cmd += ",".join(self.colnames)
        cmd += ") VALUES ("
        cmd += ",".join(values) + ")"
        #print(cmd)
        self.anapencere.stok_dbm.executeCmd(cmd)
        if 'called_from' not in self.kwargs: #Müşteri düzenle'den 
                                                    #kişi ekleniyorsa tablo değişmesin
            self.anapencere.tableView_Model.setTable(self.seçilitablo_dbTableName)
        self.done(QDialog.Accepted)
        
    def alanlarıdoldur(self,firmaadı):
        self.lineEdits[2].setText(firmaadı)
        
class TicListSilDialog(QDialog):
    def __init__(self, anapencere):
        '''
        Constructor
        '''
        super().__init__()
        self.anapencere = anapencere

        self.bilgileriAl()        
        self.dialogUIoluştur()        
        self.dialogMoveCenter()

        self.show()
        
    def bilgileriAl(self):
        tm = self.anapencere.tableView_Model
        seçilitablobilgileri = self.anapencere.gösterilecek_tablo_bilgileri[tm.seçimNo]
        self.seçilitablo_gösterilenAd = seçilitablobilgileri[0]
        self.seçilitablo_dbTableName = seçilitablobilgileri[1]
        self.seçilitablo_iconfilename = seçilitablobilgileri[2]
        cmd= "SHOW COLUMNS FROM {}".format(self.seçilitablo_dbTableName)
        #print(cmd)
        self.seçilitablo_sqlcolumndata = self.anapencere.stok_dbm.executeCmd(cmd)
        #print("self.seçilitablo_sqlcolumndata:",self.seçilitablo_sqlcolumndata)
        self.colnames = [a[0] for a in self.seçilitablo_sqlcolumndata[1:]]
        #print("self.colnames:",self.colnames)
        self.coltypes = [a[1].decode() for a in self.seçilitablo_sqlcolumndata[1:]]
        #print("self.coltypes:",self.coltypes)
        self.idcolname = self.seçilitablo_sqlcolumndata[0][0]
        #print("id_column_name________:",self.idcolname)
        
    def dialogUIoluştur(self):
        if self.seçilitablo_gösterilenAd == "Müşteriler":
            self.setWindowTitle("Müşteri Sil")
            başlıkLabel = QLabel("MÜŞTERİ SİL")
        elif self.seçilitablo_gösterilenAd == "Tedarikçiler":
            self.setWindowTitle("Tedarikçi Sil")
            başlıkLabel = QLabel("TEDARİKÇİ SİL")
        elif self.seçilitablo_gösterilenAd == "Kişiler":
            self.setWindowTitle("Kişi Sil")
            başlıkLabel = QLabel("KİŞİ SİL")
        
        
        self.setGeometry(100,100,400,350)
        self.setModal(True)
        
        başlıkLabel.setStyleSheet('color: green;')
        başlıkLabel.setFont(QFont('Arial', 12,QFont.Bold))
        
        mainvboxlayout = QVBoxLayout()
        self.setLayout(mainvboxlayout)
        
        başlıkhbox = QHBoxLayout()
        başlıkhbox.addWidget(self.dialogResimLabelOluştur())
        başlıkhbox.addStretch()
        başlıkhbox.addWidget(başlıkLabel)
        başlıkhbox.addStretch()
        
        mainvboxlayout.addLayout(başlıkhbox)
        
        mainvboxlayout.addSpacing(20)
        
        self.menüden_silForm()
        
        mainvboxlayout.addWidget(self.form)
        
    def menüden_silForm(self):
        self.form = QWidget()        
        flo = QVBoxLayout()
        self.form.setLayout(flo)
        
        layout = QFormLayout()
        
        def letextchangedslot(text):
            self.lw.model().clear()
            self.lw.selectionModel().clearSelection()
            self.silbtn.setEnabled(False)
            if not text:
                return
            cmd = "SELECT {},{} ".format(self.idcolname, self.colnames[0])
            cmd += "FROM {}".format(self.seçilitablo_dbTableName)
            cmd += " WHERE {} LIKE '%{}%'".format(self.colnames[0],text.strip().upper())
            cmd += " LIMIT 10"
            #print(cmd)
            self.sqlans = self.anapencere.stok_dbm.executeCmd(cmd)
            print(self.sqlans)
            if self.sqlans:
                adlar = [kayit[1] for kayit in self.sqlans]
                for ad in adlar:
                    item = QStandardItem(ad)
                    self.lw.model().appendRow(item)
        
        label = QLabel(self.colnames[0])
        le = QLineEdit()
        le.textChanged.connect(letextchangedslot)
        
        layout.addRow(label, le)
        
        flo.addLayout(layout)
        
        flo.addStretch()
        
        def lwselectionChangedSlot(selected,deselected):
            selIdxs = selected.indexes()
            if not selIdxs:
                print("yooooeeeekk")
                self.silbtn.setEnabled(False)
                return
            index = selected.indexes()[0]
            self.silbtn.setEnabled(True)
#             print("seçilen satır:",index.row())
#             print("Seçilen id no:",self.idcolname,"=",self.sqlans[index.row()][0])
            self.seçilen_id= self.sqlans[index.row()][0]
        self.lw = QListView(self)
        self.lw.setModel(QStandardItemModel())
        self.lw.selectionModel().selectionChanged.connect(lwselectionChangedSlot)
        
        flo.addWidget(self.lw)
        
        hboxlayout = QHBoxLayout()
        hboxlayout.addStretch()
        
        iptalbtn = QPushButton("İptal")
        iptalbtn.clicked.connect(self.iptalbtn_call)
        hboxlayout.addWidget(iptalbtn)
        
        self.silbtn = QPushButton("Sil")
        self.silbtn.clicked.connect(self.silbtn_call)
        self.silbtn.setEnabled(False)
        hboxlayout.addWidget(self.silbtn)
        
        flo.addLayout(hboxlayout)
        
        self.hataLabel = QLabel()
        self.hataLabel.setStyleSheet('color: red;')
        flo.addWidget(self.hataLabel)
        
    def dialogMoveCenter(self):
        screenCenter=QApplication.desktop().availableGeometry().center()
        myrect=self.frameGeometry()
        myrect.moveCenter(screenCenter)
        self.move(myrect.topLeft())

    def dialogResimLabelOluştur(self):
        resim = QLabel()
        resim.setMaximumHeight(72)
        path = os.path.join('images', self.seçilitablo_iconfilename)
        pic = QPixmap(path)
        resim.setPixmap(pic)
        return resim
    
    def iptalbtn_call(self):
        self.done(QDialog.Rejected)
        
    def silbtn_call(self):
        #print("Seçilen id no:",self.idcolname,"=",self.seçilen_id)
        self.deleteWhereID()
        self.done(QDialog.Accepted)
        
    def deleteWhereID(self):
        cmd = "DELETE FROM {} ".format(self.seçilitablo_dbTableName)
        cmd += "WHERE {0} = {1}".format(self.idcolname,self.seçilen_id)
        self.anapencere.stok_dbm.executeCmd(cmd)
        self.anapencere.tableView_Model.setTable(self.seçilitablo_dbTableName)  # for tableview refresh
        
        
class Tableviewdan_sildialog(QDialog):
    def __init__(self, anapencere,rowNo):
        '''
        Constructor
        '''
        super().__init__()
        self.anapencere = anapencere
        self.rowNo = rowNo

        self.bilgileriAl()        
        self.dialogUIoluştur()        
        self.dialogMoveCenter()

        self.show()
        
    def bilgileriAl(self):
        tm = self.anapencere.tableView_Model
        seçilitablobilgileri = self.anapencere.gösterilecek_tablo_bilgileri[tm.seçimNo]
        self.seçilitablo_gösterilenAd = seçilitablobilgileri[0]
        self.seçilitablo_dbTableName = seçilitablobilgileri[1]
        self.seçilitablo_iconfilename = seçilitablobilgileri[2]
        self.seçilen_adı = self.anapencere.tableView_Model.sqldata[self.rowNo][1]
        self.seçilen_id = self.anapencere.tableView_Model.sqldata[self.rowNo][0]
        self.idcolname = self.anapencere.tableView_Model.sqlheader[0][0]
        
    def dialogUIoluştur(self):
        
        if self.seçilitablo_gösterilenAd == "Müşteriler":
            self.değişenText = "Müşteri"
        elif self.seçilitablo_gösterilenAd == "Tedarikçiler":
            self.değişenText = "Tedarikçi"
        elif self.seçilitablo_gösterilenAd == "Kişiler":
            self.değişenText = "Kişi"
        else:
            self.değişenText = "Bulunamadı"
        
        self.setWindowTitle(self.değişenText + " Sil")
        self.setGeometry(100,100,300,200)
        self.setModal(True)
        
        başlıkLabel = QLabel(self.değişenText.upper() + " SİL")
        başlıkLabel.setStyleSheet('color: green;')
        başlıkLabel.setFont(QFont('Arial', 12,QFont.Bold))
        
        mainvboxlayout = QVBoxLayout()
        self.setLayout(mainvboxlayout)
        
        başlıkhbox = QHBoxLayout()
        başlıkhbox.addWidget(self.dialogResimLabelOluştur())
        başlıkhbox.addStretch()
        başlıkhbox.addWidget(başlıkLabel)
        başlıkhbox.addStretch()
        
        mainvboxlayout.addLayout(başlıkhbox)
        
        mainvboxlayout.addSpacing(20)
        
        self.tableViewdan_silForm()
        #self.menüden_silForm()
        
        mainvboxlayout.addWidget(self.form)
        
    def dialogMoveCenter(self):
        screenCenter=QApplication.desktop().availableGeometry().center()
        myrect=self.frameGeometry()
        myrect.moveCenter(screenCenter)
        self.move(myrect.topLeft())
        
    def dialogResimLabelOluştur(self):
        resim = QLabel()
        resim.setMaximumHeight(72)
        path = os.path.join('images', self.seçilitablo_iconfilename)
        pic = QPixmap(path)
        resim.setPixmap(pic)
        return resim
    
    def deleteWhereID(self):
        cmd = "DELETE FROM {} ".format(self.seçilitablo_dbTableName)
        cmd += "WHERE {0} = {1}".format(self.idcolname,self.seçilen_id)
        self.anapencere.stok_dbm.executeCmd(cmd)
        self.anapencere.tableView_Model.setTable(self.seçilitablo_dbTableName)  # for tableview refresh
    
        
    def tableViewdan_silForm(self):
        self.form = QWidget()        
        flo = QVBoxLayout()
        self.form.setLayout(flo)
        
        uyarıhbox = QHBoxLayout()
        uyarıdakiAdLabel = QLabel(self.seçilen_adı) 
        uyarıdakiAdLabel.setStyleSheet('color: red;')
        uyarıdakiAdLabel.setFont(QFont('Arial', 12,QFont.Bold))
        
        uyarıdakiTextLabel = QLabel(" Adlı " + self.değişenText + " Silinecek !!")
        uyarıhbox.addStretch()
        uyarıhbox.addWidget(uyarıdakiAdLabel)
        uyarıhbox.addWidget(uyarıdakiTextLabel)
        uyarıhbox.addStretch()
        flo.addLayout(uyarıhbox)
        
        flo.addStretch()
        
        btnshbox = QHBoxLayout()
        btnshbox.addStretch()
        
        def iptalbtn_call():
            self.done(QDialog.Rejected)
        
        def silbtn_call():
            self.deleteWhereID()
            self.done(QDialog.Accepted)
        
        iptalbtn = QPushButton("İptal")
        iptalbtn.clicked.connect(iptalbtn_call)
        btnshbox.addWidget(iptalbtn)
        
        silbtn = QPushButton("Sil")
        silbtn.clicked.connect(silbtn_call)
        btnshbox.addWidget(silbtn)

        flo.addLayout(btnshbox)
        
    def menüden_silForm(self):
        self.form = QWidget()        
        flo = QVBoxLayout()
        self.form.setLayout(flo)
        
        layout = QFormLayout()
        
        def letextchangedslot(text):
            self.lw.model().clear()
            self.lw.selectionModel().clearSelection()
            self.silbtn.setEnabled(False)
            if not text:
                return
            cmd = "SELECT {},{} ".format(self.idcolname, self.colnames[0])
            cmd += "FROM {}".format(self.seçilitablo_dbTableName)
            cmd += " WHERE {} LIKE '%{}%'".format(self.colnames[0],text.strip().upper())
            cmd += " LIMIT 10"
            #print(cmd)
            self.sqlans = self.anapencere.stok_dbm.executeCmd(cmd)
            print(self.sqlans)
            if self.sqlans:
                adlar = [kayit[1] for kayit in self.sqlans]
                for ad in adlar:
                    item = QStandardItem(ad)
                    self.lw.model().appendRow(item)
        
        label = QLabel(self.colnames[0])
        le = QLineEdit()
        le.textChanged.connect(letextchangedslot)
        
        layout.addRow(label, le)
        
        flo.addLayout(layout)
        
        flo.addStretch()
        
        def lwselectionChangedSlot(selected,deselected):
            selIdxs = selected.indexes()
            if not selIdxs:
                print("yooooeeeekk")
                self.silbtn.setEnabled(False)
                return
            index = selected.indexes()[0]
            self.silbtn.setEnabled(True)
#             print("seçilen satır:",index.row())
#             print("Seçilen id no:",self.idcolname,"=",self.sqlans[index.row()][0])
            self.seçilen_id= self.sqlans[index.row()][0]
        self.lw = QListView(self)
        self.lw.setModel(QStandardItemModel())
        self.lw.selectionModel().selectionChanged.connect(lwselectionChangedSlot)
        
        flo.addWidget(self.lw)
        
        hboxlayout = QHBoxLayout()
        hboxlayout.addStretch()
        
        iptalbtn = QPushButton("İptal")
        iptalbtn.clicked.connect(self.iptalbtn_call)
        hboxlayout.addWidget(iptalbtn)
        
        self.silbtn = QPushButton("Sil")
        self.silbtn.clicked.connect(self.silbtn_call)
        self.silbtn.setEnabled(False)
        hboxlayout.addWidget(self.silbtn)
        
        flo.addLayout(hboxlayout)
        
        self.hataLabel = QLabel()
        self.hataLabel.setStyleSheet('color: red;')
        flo.addWidget(self.hataLabel)
#********************************************************************

    