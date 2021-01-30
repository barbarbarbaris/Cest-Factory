'''
Created on 26 Kas 2020

@author: Barış Kılıçlar
'''
from PyQt5.QtCore import QAbstractTableModel,QModelIndex
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush,QColor
from PyQt5.QtWidgets import QStyledItemDelegate

class barisTableViewModel(QAbstractTableModel):
    '''
    classdocs
    '''
    

    def __init__(self,barParent):
        '''
        Constructor
        '''
        super().__init__()
        self.tablename = ""
        self.barParent = barParent
        self.sqlheader = []
        self.sqldata = []
        self.yellowrow = -1

        
    def setTable(self,tablename):
        self.tablename = tablename        
        self.setSQLHeader()
        self.setSQLData("SELECT * FROM {}".format(self.tablename))
    
    def setSQLHeader(self):
        if not self.tablename:
            self.sqlheader = []
            return
        self.sqlheader = self.barParent.stok_dbm.executeCmd("SHOW COLUMNS FROM {}".
                                                            format(self.tablename))        
        #print("sqlheader:",self.sqlheader)
        
    def setSQLData(self,cmd):
        if not self.tablename:
            self.sqldata = []
            return
        self.sqldata = self.barParent.stok_dbm.executeCmd(cmd)
        self.yellowrow = -1
        #print("SQLData :",self.sqldata)
        self.refreshView()
        
    def refreshView(self):        
        self.headerDataChanged.emit(Qt.Horizontal, 0, self.columnCount())
        self.dataChanged.emit(self.index(0,0), 
                              self.index(self.rowCount(),self.columnCount()),
                              [Qt.DisplayRole]) 
    
    def rowCount(self,parent=QModelIndex()):
        #return 2
        if not self.tablename:
            return 0
#         msg=self.barParent.stok_dbm.executeCmd(
#             'SELECT COUNT(*) FROM {}'.format(self.tablename))
        #print("ROW Msg ***:",msg)
#         num, = msg[0]
#         return num
        if not self.sqldata:
            return 0
        #print("Row Count:",len(self.sqldata))
        return len(self.sqldata)
        
    def columnCount(self,parent=QModelIndex()):
#         print("Column Counttan:",self.sqlheader)
#         return 2
        if not self.tablename:
            return 0
        if not self.sqlheader:
            return 0
        return len(self.sqlheader)
    
    #https://stackoverflow.com/questions/19411101/pyside-qtableview-example
    
    def headerData(self, section, orientation,role=Qt.DisplayRole):
        if not self.tablename:
            return
        if not self.sqlheader:
            return
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            #return "header " + str(section) # SİLLLLLLLLLLLL
            #msg=self.barParent.stok_dbm.executeCmd("SHOW COLUMNS FROM {}".format(self.tablename))
            #print("***msg:",msg)
            #columnname=
            #print("COLUMN NAME İSTENDİ, verilen:",columnname, "tip:",columnname.__class__)
            #print("---- HEADER :",self.sqlheader[section][0])
            return self.sqlheader[section][0]
        return

    
    def data(self,index,role=Qt.DisplayRole):
        if not self.tablename:
            return
        if not self.sqldata:
            return
        if not index.isValid():
            return
        elif role == Qt.DisplayRole:
#             return
            col = index.column()
            row = index.row()
        #return str(row) + ',' +str(col)
#         colname = self.sqlheader[col][0] #self.headerData(col, Qt.Horizontal)
#         print("data 'da colname :",colname)
#         msg=self.barParent.stok_dbm.executeCmd("SELECT {colname} "
#                                                     "FROM {tablename}".format(colname=colname,
#                                                                               tablename=self.tablename))
        #print("DATA MSG for {}** :".format(colname),msg)
#         if not msg: #isEmpty
#             return
#         data,=msg[row]
        #print("Data:***:",data, "** Tip ** :", data.__class__)
#         return data
        #print("** DATA :",self.sqldata[row][col])
            return self.sqldata[row][col]
        elif role == Qt.BackgroundRole:
            row = index.row()
            if row == self.yellowrow:
                return QColor(Qt.yellow)
            
    def setYellowRowFromIdColumnValue(self,idcolvalue):
        ids = [a[0] for a in self.sqldata]
        self.yellowrow = ids.index(idcolvalue)
        pass

import mysql.connector

class barDBManager:
    
    def __init__(self,databasename):
        self.db = databasename
        
    def connect(self,user,passwd,host):

        try:
            self.cnx = mysql.connector.connect(user=user,
                                               password=passwd,
                                               host=host)
            self.cnx.database = self.db
        except mysql.connector.Error as err:            
            print("db bağlantı hatası:",str(err))
            return(-1)
        
        self.cursor = self.cnx.cursor()
        
    def executeCmd(self,cmd):
        try:
            self.cursor.execute(cmd)
        except mysql.connector.Error as err:
            print("Şu komutta hata oldu:",cmd,"--:",str(err))
            return -1
        try:
            msg = self.cursor.fetchall()
        except:
            print("fetchall erroru oldu")
            msg = self.cursor.fetchone()
        self.cnx.commit()
        return msg
    
    def çıkış(self):
        self.cursor.close()
        self.cnx.close()

def denemefun(self):
    print("******* deneme self **********  : ",self.__class__)
    
class differentRow(QStyledItemDelegate):
    def __init__(self, *args, **kwargs):
        QStyledItemDelegate.__init__(self, *args, **kwargs)
        self.row = -1
        
    def paint(self, painter, option, index):
        if index.row()==self.row:
            painter.setBackgroundMode(Qt.OpaqueMode)
            painter.setBackground(QBrush(QColor(Qt.yellow)))
        else:
            painter.setBackgroundMode(Qt.TransparentMode)
            painter.setBackground(QBrush(QColor(Qt.white)))
        return QStyledItemDelegate.paint(self, painter, option, index)
    
    def setRow(self,row):
        self.row = row
        
        #return 
    
#     def sizeHint(self, option, index):
#         return QStyledItemDelegate.sizeHint(self, option, index)
    
        