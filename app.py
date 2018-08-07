import pandas as pd
from DataFrame_Cleaning.df_cleaning import  dataframe_cleaning,dataframe_addColumns, find_excel_filenames
from Database.Database_Insert import database_insertValidation,database_insertExcelValues
from settings import file_paths,con,cur
from Database.Database_query import Validation_1_query, Validation_2_query, file_query
from reports import report
import time
import datetime
import os

def app():
    #Append value to Validation Table
    Validation_key = database_insertValidation()

    #Read all files to database
    for project in file_paths:
        project_name= file_paths.index(project)
        print(project_name)
        for path in project:
            filenames= find_excel_filenames(path)
            for file in filenames:
                sheetName = pd.ExcelFile(path+file).sheet_names
                for sheet in sheetName:
                    dataframe= pd.read_excel(path+file, sheet_name= sheet, header=[0,1])
                    dataframe = dataframe_cleaning(dataframe)
                    dataframe = dataframe_addColumns(dataframe=dataframe, file=file, project_name=project_name,
                                                     sheet=sheet, Validation_key=Validation_key)
                    database_insertExcelValues(dataframe)

    # Validation Test 1 and status report
    Validation_1 = Validation_1_query(Validation_key=Validation_key)

    #Validation Test 2 and status report
    Validation_2 = Validation_2_query(Validation_key=Validation_key)

    files = file_query(Validation_key)

    #Setup datetime for Report and MasterFile
    ts = time.time()
    dateTime = (datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))

    #Update Validation Status
    if(len(Validation_1) > 0) and (len(Validation_2) > 0):
        status = "Failed both validation"
    elif (len(Validation_1) > 0) and (len(Validation_2) == 0):
        status = "Only validation 1 failed"
    elif (len(Validation_1) == 0) and (len(Validation_2) > 0):
        status = "Only Validation 2 failed"
    else :
        status = "OK"
        Master_File = pd.read_sql("Select * From Excel_Values Where Validation_key=" + str(Validation_key), con)
        fileName = "MasterFile_" + str(dateTime)
        completeName = os.path.join("MasterFile/", fileName)
        Master_File.to_csv(completeName, index=False)

    #Update Status in Validation Table
    cur.execute('UPDATE validation SET status = ? WHERE Validation_key = ?', (status, Validation_key));

    #Generate Reprot
    report(dateTime, Validation_1, Validation_2, files)
    return None