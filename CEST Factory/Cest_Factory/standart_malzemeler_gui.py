'''
Created on 30 Oca 2021

@author: user
'''

class standart_malzemeler_view_edit_gui(QDialog):
    '''
    classdocs
    '''


    def __init__(self, anapencere):
        '''
        Constructor
        '''
        super().__init__()
        self.anapencere = anapencere
        self.rowNo = index.row()

        #self.bilgileriAl()
        self.changeTexts()
        self.dialogUIoluştur()
        self.dialogMoveCenter()
        self.fillthefields()
        self.show()
    def hellorilerdengel(self):
        print("Ule hellorilerden gelirem uleeeooo")
        print("ule ule uleeeee")
        print("ulan alla laaaa")