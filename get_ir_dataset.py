##
 # get_ir_dataset.py
 ##

import os
import logging

import pandas as pd

from config import SMDBConfig as Config
from ir_dataset_generator import IRDatasetGenerator


if __name__ == '__main__':
    
    '''set logger'''
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(message)s')

    stream_hander = logging.StreamHandler()
    stream_hander.setFormatter(formatter)
    logger.addHandler(stream_hander)
    
    '''path'''
    if not os.path.exists(Config.SAVE_PATH):
        os.mkdir(Config.SAVE_PATH)
        logging.info(f'mkdir {Config.SAVE_PATH}')
    
    filenames = Config.SMDB_LIST[-1] # table name -> filename
    
    '''run'''
    data_generator = IRDatasetGenerator(Config)
    for i, x in enumerate(map(lambda raw, filename: True if 
                              data_generator.save_as_pickle(
                              data_generator.transform(pd.DataFrame(raw[1], columns=raw[0])), filename) else False,
                              data_generator.extract(), filenames)):
         
        logging.info(f'{filenames[i]} saved') if x else logging.info(f'{filenames[i]} failed')          
            
    data_generator.close()