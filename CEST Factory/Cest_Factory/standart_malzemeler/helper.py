'''
Created on 6 Şub 2021

@author: user
'''
class standart_malzemeler_record():
    
    def __init__(self,anapencere,*,
                 record_id=0, 
                 Tipi='',
                 Tip_Kodu='',
                 Boyutlar='',
                 Stok_Bölgesi='',
                 Adet=0):
        self.anapencere = anapencere
        self.record_id = record_id
        self.Tipi = Tipi
        self.Tip_Kodu = Tip_Kodu
        self.Boyutlar = Boyutlar
        self.Stok_Bölgesi = Stok_Bölgesi
        self.Adet = Adet
        
    def checkformatchingrecord(self):
        #returns (match,matching_id,matching_records_Adet)
        
        cmd = ("SELECT idstandart_malzemeler,Adet " +
               "FROM standart_malzemeler WHERE " +
               "Tipi " + self.fieldSQLcondition(self.Tipi) + " AND " +
               "Tip_Kodu " + self.fieldSQLcondition(self.Tip_Kodu) + " AND " +
               "Boyutlar " + self.fieldSQLcondition(self.Boyutlar) + " AND " +
               "Stok_Bölgesi " + self.fieldSQLcondition(self.Stok_Bölgesi) + ";"
               )
        msg = self.anapencere.stok_dbm.executeCmd(cmd)
        print(msg)
        if len(msg)>1:
            print("Aynı özelliklerde birden fazla kayıt !!!!")
            print("Bu database hatasıdır. Barış Kılıçlar'ı arayınız."
                  " Tel: 0532 224 07 31")
        if msg:
            return (True,msg[0][0],msg[0][1])
        else:
            return (False,0,0)
        
    def insertinto_table(self):
        cmd = ("INSERT INTO standart_malzemeler " +
               "(Tipi,Tip_Kodu,Boyutlar,Adet,Stok_Bölgesi) " +
               "VALUES (" + self.fieldSQLtext(self.Tipi) + "," +
               self.fieldSQLtext(self.Tip_Kodu) + "," +
               self.fieldSQLtext(self.Boyutlar) + "," +
               str(self.Adet) + "," +
               self.fieldSQLtext(self.Stok_Bölgesi) + ");"
               )
        self.anapencere.stok_dbm.executeCmd(cmd)
        self.anapencere.tableView_Model.setTable("standart_malzemeler")  # for tableview refresh
        
    def update_adet_of_tablerecord(self,newadet):
        cmd = ("UPDATE standart_malzemeler " +
               "SET Adet = {} ".format(newadet) + #int or string but int
               "WHERE idstandart_malzemeler = {}".format(self.record_id)
               )
        print(cmd)
        self.anapencere.stok_dbm.executeCmd(cmd)
        self.anapencere.tableView_Model.setTable("standart_malzemeler")  # for tableview refresh
        self.anapencere.tableView_Model.setYellowRowFromIdColumnValue(self.record_id)
        
    def setfromtablerowdata(self,rowdata):
        if len(rowdata)<6:
            print(__name__," Eksik table rowdata girişi")
            return
        self.record_id = rowdata[0] # None olamaz, Not Null(NN) özellikli SQL Alanıdır bu.
        self.Tipi = self.translatefromSQLans(rowdata[1])
        self.Tip_Kodu = self.translatefromSQLans(rowdata[2])
        self.Boyutlar = self.translatefromSQLans(rowdata[3])
        self.Stok_Bölgesi = self.translatefromSQLans(rowdata[5])
        self.Adet = self.translatefromSQLans(rowdata[4])

    def fieldSQLtext(self,text):
        if text:
            return "'" + text + "'"
        else:
            return 'NULL'
        
    def fieldSQLcondition(self,text):
        if text:
            return "='" + text + "'"
        else:
            return "IS NULL"
        
    def translatefromSQLans(self,text):
        if text == None:
            return '' 
        else:
            return text