'''
Created on 8 Şub 2021

@author: user
'''
def civataları_aktar(self):
    cmd = "SELECT COUNT(*) FROM civatalar;"
    msg = self.stok_dbm.executeCmd(cmd)
    print("Count Sonucu - civatalar table :",msg)
    cmd = "SELECT * FROM civatalar LIMIT 1;"
    msg = self.stok_dbm.executeCmd(cmd)
    print("select * limit 1 sonucu - civatalar:",msg)