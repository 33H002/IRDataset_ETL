## IRDataset_ETL 기록용

#### config.py
```
class Base:
  
    SMDB_URL = 
    SMDB_PORT = 
    SMDB_SERVICE = 
    SMDB_USER = 
    SMDB_PASSWORD = 
    SMDB_SCHEMA = 
    SMDB_IR140 = {추출 DB명}
    SMDB_IR180 = {추출 DB명}
    
    MYSQL_URL = 
    MYSQL_PORT = 
    MYSQL_UESR = 
    MYSQL_PASSWORD = 
    MYSQL_DB = 
    
    SENTRY_DSN =
        
        
# oracle        
class SMDBConfig:
    SMDB_LIST = [
        Base.SMDB_URL,
        Base.SMDB_PORT,
        Base.SMDB_SERVICE,
        Base.SMDB_USER,
        Base.SMDB_PASSWORD,
        Base.SMDB_SCHEMA,
        [
            Base.SMDB_IR140,
            Base.SMDB_IR180,
        ]
    ]
    SAVE_PATH = {save_path}
    
    
# mysql
class MYSQLIRConfig:
    DB_LIST = [
        Base.MYSQL_URL,
        Base.MYSQL_PORT,
        Base.MYSQL_UESR,
        Base.MYSQL_PASSWORD,
        Base.MYSQL_DB,
        [
            Base.SMDB_IR140,
            Base.SMDB_IR180,
        ]
    ]
    SAVE_PATH = {save_path}
```
