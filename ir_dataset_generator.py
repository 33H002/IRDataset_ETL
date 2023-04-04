##
 # ir_dataset_generator.py
 ##

import cx_Oracle

import pandas as pd

from typing import Any, Iterator, List, Tuple


class IRDatasetGenerator:
    def __init__(self, config: Any):
        '''Path'''
        self.save_path = config.SAVE_PATH
        
        '''DB Connection'''
        self.host, self.port, self.service, self.user, self.password, self.schema, self.tables = config.SMDB_LIST
        self.dsn_tns = cx_Oracle.makedsn(self.host, self.port, service_name=self.service)
        self.conn = cx_Oracle.connect(user=self.user, password=self.password, dsn=self.dsn_tns)
        self.conn.current_schema=self.schema 
        
    def extract(self) -> Iterator[Tuple[List, List[Tuple]]]:
        '''Fetch All Table Once'''
        for table in self.tables:
            try:
                cur = self.conn.cursor()
                cur.execute(f'select * from {table}')
                columns = [c[0] for c in cur.description]
                yield (columns, cur.fetchall())
            finally:
                cur.close()
            
    def extract_by_table_name(self, table:str) -> Iterator[Tuple]:
        '''Extract a Specific Table by Name'''
        try:
            cur = self.conn.cursor()
            cur.execute(f'select * from {table}')
            while cur:
                yield cur.fetchone()
        finally:
            cur.close()
        
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        '''Transform'''
        if 'STNAME' in df.columns:
            df.drop(['STNAME'], axis=1, inplace=True)
            df['STNO'] = df['STNO'].apply(lambda x: str(x)[:2])
        return df
    
    def save_as_pickle(self, df:pd.DataFrame, filename: str) -> bool:
        '''DataFrame to Pickle'''
        try:
            df.to_pickle(f'{self.save_path}/{filename}.pkl')
        except:
            return False
        return True
    
    def reload(self, df:pd.DataFrame, tablename: str) -> bool:
        '''DataFrame Insert to DB'''
        import pymysql
        from sqlalchemy import create_engine
        from config import MYSQLIRConfig as MyConfig

        try:
            HOST, PORT, USER, PASSWORD, DB, TABLES = MyConfig.DB_LIST

            db_connection = create_engine(f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DB}')
            df.to_sql(name=tablename, con=db_connection, if_exists='append',index=False, chunksize=1000, method='multi')
        except:
            db_connection.dispose()
            return False
        db_connection.dispose()
        return True

    def close(self):
        '''Close Connection'''
        if self.conn:
            self.conn.close()