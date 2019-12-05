"""
Title: main.py
By: M5DS1
    Purpose:

"""

import os
from data_parser import *


''' Only Change This!! '''
json_dir = 'Decrypted/Intel/'
# json_dir = 'Decrypted/Viper/'
# json_dir = 'Decrypted/Solo/'

for json_file in os.listdir(json_dir):
    if json_file.endswith(".json"):
        data_parser(json_dir,os.path.splitext(json_file)[0])


