import time
import datetime
from settings import *

def database_insertValidation():
    ts = time.time()
    dateTime= (datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
    cur.execute('INSERT INTO Validation (Validation_Date, Status) VALUES (?,?)',
                    (dateTime, 'NA'))
    return cur.lastrowid


def database_insertExcelValues(dataframe):
    dataframe.to_sql(name="Excel_Values", con=con, if_exists="append", index=False)
    return None