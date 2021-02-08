'''
Created on 7 Şub 2021

@author: user
'''
from Cest_Factory.standart_malzemeler.helper import fieldSQLcondition,fieldSQLtext,\
    translatefromSQLans

class tipler_kodlar_record():
    '''
    classdocs
    '''


    def __init__(self, anapencere,dialog,*,
                 record_id = 0,
                 field1 = '',
                 field2 = ''):
        '''
        tipler_kodlar_record Constructor
        '''
        self.anapencere = anapencere
        self.dialog = dialog
        self.record_id = record_id
        self.field1 = field1
        self.field2 = field2
        
    def checkformatchingrecord(self):
        #returns (if_match,matching_id)
        cmd = ("SELECT " + self.dialog.colnames[0][0] + 
               " FROM " + self.dialog.seçilitablo_dbname +
               " WHERE " + 
               self.dialog.colnames[1][0] + " " + fieldSQLcondition(self.field1)
               )
        msg = self.anapencere.stok_dbm.executeCmd(cmd)
        if len(msg)>1:
            print(__name__,"Aynı özelliklerde birden fazla kayıt !!!!")
            print("Bu database hatasıdır. Barış Kılıçlar'ı arayınız."
                  " Tel: 0532 224 07 31")
        if msg:
            return (True,msg[0][0])
        else:
            return (False,0)
        
    def insertinto_table(self):
        cmd = ("INSERT INTO " + self.dialog.seçilitablo_dbname + " (" +
               self.dialog.colnames[1][0] + "," +
               self.dialog.colnames[2][0] + ") " +
               "VALUES (" + fieldSQLtext(self.field1) + "," +
               fieldSQLtext(self.field2) + ");"
               )
        self.anapencere.stok_dbm.executeCmd(cmd)
        self.anapencere.tableView_Model.setTable(self.dialog.seçilitablo_dbname)  # for tableview refresh
        
    def deletefromtable(self):
        print("------------ deletefromtable giriş")
        cmd = ("DELETE FROM " + self.dialog.seçilitablo_dbname +
               " WHERE " + 
               self.dialog.colnames[0][0] + " = " + str(self.record_id)
               )
        print("-------- cmd:",cmd)
        self.anapencere.stok_dbm.executeCmd(cmd)
        self.anapencere.tableView_Model.setTable(self.dialog.seçilitablo_dbname)  # for tableview refresh

    def setfromtablerowdata(self,rowdata):
        if len(rowdata)<3:
            print(__name__," Eksik table rowdata girişi")
            return
        self.record_id = rowdata[0] # None olamaz, Not Null(NN) özellikli SQL Alanıdır bu.
        self.field1 = translatefromSQLans(rowdata[1])
        self.field2 = translatefromSQLans(rowdata[2])