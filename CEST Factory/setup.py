'''
Created on 3 Ara 2020

@author: user
'''
from setuptools import setup#, find_packages
setup(
    name="Cest Program",
    version="1.5",
    packages=['Cest_Factory'],
    package_dir={'Cest_Factory': 'Cest_Factory'},
    package_data={'Cest_Factory': ['images\\*.*']},
#     package_dir={'Cest_Factory': 'C:\\Users\\user\\Desktop\\Barış\\bar_dev\\barEclipse\\CEST Factory\\Cest_Factory'},
#     package_data={'': ['C:\\Users\\user\\Desktop\\Barış\\bar_dev\\barEclipse\\CEST Factory\\Cest_Factory\\images\\*.*']},

#     package_data={'': ['C:\\Users\\user\\Desktop\\Barış\\bar_dev\\barEclipse\\CEST Factory\\Cest_Factory\\images\\*.*']},
        
    install_requires=['pyqt5-tools','mysql-connector-python']
    )
#dir_util.copy_tree("Cest_Factory", "images", update=1, preserve_mode=0)
