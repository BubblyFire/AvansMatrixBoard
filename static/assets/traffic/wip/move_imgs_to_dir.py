#################################################################################################
#
# Run as script
#
# name.py json_config_file 
#
# json_config_file: file format json style
# {
#     "dir" : "Categorie C - Gesloten verklaring", # Target directory
#     "desc": "Categorie C - Gesloten verklaring", # Category description - Not used in this context
#     "imgs": # list of images
# [
# {"src":"C01.jpg", # file name
#  "alt": "C01",    # alternative, if file does not exist - not used here
#  "desc": "item description"}, # item description - not used here
#  {...}
# ]}
#
#################################################################################################
#
# (C) JSC 2024
#
#################################################################################################

import os
import sys
import json

def js_r(filename):
   with open(filename) as f_in:
       return(json.load(f_in))
   
def try_mv_fl(filename, targetdir):
    try:
        to = os.path.join(targetdir,filename)
        os.rename(filename, to)
        print( 'Moved: "'+filename+'" to "'+to+'"')
    except Exception as e:
        print(e)

def mv_imgs(dct):
    tgt_dir = dct['dir']
    for img in dct['imgs']:
        try_mv_fl(img['src'], tgt_dir)

if __name__ == "__main__":
    try:
        my_data = js_r(sys.argv[1])
        mv_imgs(my_data)
    except Exception as e:
        print(e)
        
