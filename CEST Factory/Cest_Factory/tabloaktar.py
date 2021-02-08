'''
Created on 8 Şub 2021

@author: user
'''
from Cest_Factory.standart_malzemeler.helper import standart_malzemeler_record

def setfromOtherTableSQLans_NOT_RULMAN(record,sqlans,Tipi):
    record.record_id = sqlans[0][0]
    record.Tipi=Tipi
    record.Tip_Kodu=sqlans[0][1]
    record.Boyutlar=sqlans[0][2]
    record.Stok_Bölgesi=sqlans[0][4]
    record.Adet=sqlans[0][3]
    
def setfromOtherTableSQLans_FOR_RULMAN(record,sqlans,Tipi):
    record.record_id = sqlans[0][0]
    record.Tipi=Tipi
    record.Tip_Kodu=sqlans[0][1]
    record.Stok_Bölgesi=sqlans[0][3]
    record.Adet=sqlans[0][2]
    
def deletefromtablebyid(self,tablename,idcolname,record_id):
    cmd = ("DELETE FROM " + tablename +
           " WHERE {}={};".format(idcolname,record_id)
           )
    self.stok_dbm.executeCmd(cmd)
    
def standartmalzemeleretabloaktar(self,tablename,idcolname,Tipi):
    
    cmd = "SELECT COUNT(*) FROM {};".format(tablename)
    msg = self.stok_dbm.executeCmd(cmd)
    tablelength = msg[0][0]
    if tablelength == 0:
        print(__name__,tablename,"Tablosunda Kayıt Yok!!")
        return
    for i in range(0,tablelength):
        standartmalzemerecord = standart_malzemeler_record(self)
        cmd = "SELECT * FROM {} LIMIT 1;".format(tablename)
        msg = self.stok_dbm.executeCmd(cmd)
        if tablename == 'rulmanlar':
            setfromOtherTableSQLans_FOR_RULMAN(standartmalzemerecord, msg,Tipi)
        else:
            setfromOtherTableSQLans_NOT_RULMAN(standartmalzemerecord, msg,Tipi)
        standartmalzemerecord.insertinto_table()
        deletefromtablebyid(self,tablename,idcolname,msg[0][0])
        print(tablename,"tablosundan aktarılan kayıtno:",i+1)
    return i==tablelength-1

def civataları_aktar(self,menu,action):
    res = standartmalzemeleretabloaktar(self,"civatalar","idCivatalar",'CIVATA')
    print("civatalar aktarma:",res)
    if res:
        menu.removeAction(action)
    
def alyanları_aktar(self,menu,action):
    res = standartmalzemeleretabloaktar(self,"alyan_civatalar","idAlyan",'ALYAN CIVATA')
    print("Alyanlar aktarma:",res)
    if res:
        menu.removeAction(action)
    
def havşaları_aktar(self,menu,action):
    res = standartmalzemeleretabloaktar(self,"havşa_başlı_civatalar","idHavsa",'HAVŞA BAŞLI CIVATA')
    print("havşa_başlı_civatalar aktarma:",res)
    if res:
        menu.removeAction(action)
    
def setiskurları_aktar(self,menu,action):
    res = standartmalzemeleretabloaktar(self,"setiskurlar","idsetiskurlar",'SETISKUR')
    print("setiskurlar aktarma:",res)
    if res:
        menu.removeAction(action)
    
def somunları_aktar(self,menu,action):
    res = standartmalzemeleretabloaktar(self,"somunlar","idsomunlar",'SOMUN')
    print("somunlar aktarma:",res)
    if res:
        menu.removeAction(action)
    
def rulmanları_aktar(self,menu,action):
    res = standartmalzemeleretabloaktar(self,"rulmanlar","idRulmanlar",'RULMAN')
    print("rulmanlar aktarma:",res)
    if res:
        menu.removeAction(action)

    

    