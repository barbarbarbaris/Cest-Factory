'''
Created on 22 Oca 2021

@author: user
'''
from PyQt5.QtWidgets import QApplication
from Cest_Factory.main import anaPencere
import sys
import os

if __name__ == '__main__':
    os.chdir(os.path.join(os.getcwd(), 'Cest_Factory'))
    uygulama = QApplication(sys.argv)
    işlem = anaPencere()
    sys.exit(uygulama.exec_())