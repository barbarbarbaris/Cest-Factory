'''
Created on 9 Şub 2021

@author: user
'''
from Cest_Factory.standart_malzemeler.helper import fieldSQLcondition,\
    fieldSQLtext, translatefromSQLans
class cest_kodları_record():
    
    def __init__(self,anapencere,*,
                 record_id=0,
                 Cest_Stok_Kodu='',
                 Tipi='',
                 Tip_Kodu='',
                 Boyutlar='',
                 Açıklama=''
                 ):
        self.anapencere = anapencere
        self.record_id = record_id
        self.Cest_Stok_Kodu = Cest_Stok_Kodu
        self.Tipi = Tipi
        self.Tip_Kodu = Tip_Kodu
        self.Boyutlar = Boyutlar
        self.Açıklama = Açıklama
        
    def checkformatchingrecord(self):
        #returns (if_match,matching_id)
        
        cmd = ("SELECT idcest_stok_kodları " +
               "FROM cest_stok_kodları WHERE " +
               "Tipi " + fieldSQLcondition(self.Tipi) + " AND " +
               "Tip_Kodu " + fieldSQLcondition(self.Tip_Kodu) + " AND " +
               "Boyutlar " + fieldSQLcondition(self.Boyutlar) + ";"
               )
        msg = self.anapencere.stok_dbm.executeCmd(cmd)
        print(msg)
        if len(msg)>1:
            print(__name__,"Aynı özelliklerde birden fazla kayıt !!!!")
            print("Bu database hatasıdır. Barış Kılıçlar'ı arayınız."
                  " Tel: 0532 224 07 31")
        if msg:
            return (True,msg[0][0])
        else:
            return (False,0)
        
    def checkformatchingCestKodurecord(self):
        #returns (if_match,matching_id)
        
        cmd = ("SELECT idcest_stok_kodları " +
               "FROM cest_stok_kodları WHERE " +
               "Cest_Stok_Kodu " + fieldSQLcondition(self.Cest_Stok_Kodu) + ";"
               )
        msg = self.anapencere.stok_dbm.executeCmd(cmd)
        print(msg)
        if len(msg)>1:
            print(__name__,"Aynı özelliklerde birden fazla kayıt !!!!")
            print("Bu database hatasıdır. Barış Kılıçlar'ı arayınız."
                  " Tel: 0532 224 07 31")
        if msg:
            return (True,msg[0][0])
        else:
            return (False,0)
        
    def insertinto_table(self):
        cmd = ("INSERT INTO cest_stok_kodları " +
               "(Cest_Stok_Kodu,Tipi,Tip_Kodu,Boyutlar,Açıklama) " +
               "VALUES (" + fieldSQLtext(self.Cest_Stok_Kodu) + "," +
               fieldSQLtext(self.Tipi) + "," +
               fieldSQLtext(self.Tip_Kodu) + "," +
               fieldSQLtext(self.Boyutlar) + "," +
               fieldSQLtext(self.Açıklama) + ");"
               )
        self.anapencere.stok_dbm.executeCmd(cmd)
        self.anapencere.tableView_Model.setTable("cest_stok_kodları")  # for tableview refresh
        
    def delete_tablerecord(self):
        cmd = ("DELETE FROM cest_stok_kodları "+
               "WHERE idcest_stok_kodları = {}".format(self.record_id))
        self.anapencere.stok_dbm.executeCmd(cmd)
        self.anapencere.tableView_Model.setTable("cest_stok_kodları")  # for tableview refresh
        
    def setfromtablerowdata(self,rowdata):
        if len(rowdata)<6:
            print(__name__," Eksik table rowdata girişi")
            return
        self.record_id = rowdata[0] # None olamaz, Not Null(NN) özellikli SQL Alanıdır bu.
        self.Cest_Stok_Kodu = translatefromSQLans(rowdata[1])
        self.Tipi = translatefromSQLans(rowdata[2])
        self.Tip_Kodu = translatefromSQLans(rowdata[3])
        self.Boyutlar = translatefromSQLans(rowdata[4])
        self.Açıklama = translatefromSQLans(rowdata[5])