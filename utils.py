# coding: utf-8
import os 
import texttable

import pandas as pd
import numpy as np

from logging import getLogger

logger = getLogger("__main__").getChild("utility")

def stdout_dataframe(df, title):
    table = texttable.Texttable()
    table.set_deco(texttable.Texttable.HEADER)        
    table.set_cols_dtype(['f' for i in range(len(df.columns))])
    table.set_cols_align(["c" for i in range(len(df.columns))])
    table.set_max_width(0)
    
    cols = [df.columns]
    cols.extend(df.values)
    table.add_rows(cols)

    print ('-------- {} --------'.format(title))
    print (table.draw(),'\n')

def save_csv(save_file, save_dir, save_filename):
    file_score_path = os.path.join(save_dir, save_filename)
    save_file.to_csv(file_score_path)
    logger.debug('{} is saved at {}'.format(save_filename, file_score_path))

def create_dir(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
        logger.debug('{} directory is created'.format(dir_path))

    else:
        logger.debug('{} directory already exists'.format(dir_path))