from .dbconn import dbconnector
from .defaults import db2covid as default_db_options
import pandas as pd

class HelperConnSingleton:
    __instance = None
    __conn = None
    
    @staticmethod
    def getInstance(opts=None):
        """ Static access method. """
        if HelperConnSingleton.__instance == None:
            HelperConnSingleton(opts)
        
        return HelperConnSingleton.__instance
    
    def __init__(self, opts=None):
        """ Virtually private constructor. """
        if HelperConnSingleton.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            HelperConnSingleton.__instance = self
            HelperConnSingleton.connect(opts)
            
    @staticmethod
    def connect(opts=None):
        HelperConnSingleton.__conn = dbconnector(
            opts if opts is not None else default_db_options)

    def execute(self, sql, c=None):
        conn = c if c is not None else HelperConnSingleton.__conn
        return pd.read_sql(sql, conn)

class DbHelper:
    
    def __init__(self, opts=None):
        self.__dbconn = HelperConnSingleton.getInstance(opts)
    
    def execute(self, sql, c=None):
        return self.__dbconn.execute(sql, c)
    
    def lead_cum_confirmed(self, date: str, sr1_code: str, ndays: int):
        sql = """
        SELECT NDAYS_AFTER
        FROM (
            SELECT
                DATE, SUBREGION1_CODE,
                LEAD(CUMULATIVE_CONFIRMED, %d) OVER (PARTITION BY SUBREGION1_CODE ORDER BY DATE) AS NDAYS_AFTER
            FROM
                COVID19_OPEN_DATA cod
        )
        WHERE DATE = '%s' AND SUBREGION1_CODE = '%s'
        """ % (ndays, date, sr1_code)

        dbconn = self.__dbconn

        return dbconn.execute(sql)
    
    def lead_cum_confirmed_date_range(self, start_date: str, end_date: str, sr1_code: str, ndays: int):
        sql = """
        SELECT NDAYS_AFTER
        FROM (
            SELECT
                DATE, SUBREGION1_CODE,
                LEAD(CUMULATIVE_CONFIRMED, %d) OVER (PARTITION BY SUBREGION1_CODE ORDER BY DATE) AS NDAYS_AFTER
            FROM
                COVID19_OPEN_DATA cod
        )
        WHERE DATE BETWEEN '%s' AND '%s' AND SUBREGION1_CODE = '%s'
        """ % (ndays, start_date, end_date, sr1_code)

        dbconn = self.__dbconn

        return dbconn.execute(sql)
    
    def get_connection(self):
        return self.__dbconn
    
    