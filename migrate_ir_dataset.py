##
 # migrate_ir_dataset.py
 ##

import sys
import sentry
import logging

import pandas as pd

from config import SMDBConfig as Config
from config import MYSQLIRConfig as MyConfig
from ir_dataset_generator import IRDatasetGenerator


if __name__ == "__main__":

    '''set logger'''
    sentry.init(Config.PROFILE, 'webcrawler')
    logging.basicConfig(level=logging.INFO,
                        stream=sys.stdout,
                        format='%(asctime)s [%(filename)s] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S') 
    
    tablenames = MyConfig.DB_LIST[-1]
    
    '''run'''
    data_generator = IRDatasetGenerator(Config)
    for i, x in enumerate(map(lambda raw, table: True if 
                              data_generator.reload(
                              data_generator.transform(pd.DataFrame(raw[1], columns=raw[0])), table) else False,
                              data_generator.extract(), tablenames)):

        logging.info(f'Succeed to insert {tablenames[i]} into DB') if x else logging.info(f'Failed to insert {tablenames[i]} into DB')
            
    data_generator.close()