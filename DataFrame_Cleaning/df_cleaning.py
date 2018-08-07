import pandas as pd
from os import listdir


def find_excel_filenames( path_to_dir, suffix=".xlsx" ):
    filenames = listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]

def dataframe_cleaning(dataframe):
    """
    :param dataframe: The dataframe that needs to be cleaned
    Step 1: Combine first two rows
    Step 2: Remove all NA rows
    Step 3: Convert from wide to long format
    Step 4: Remove all rows with NA in values colum
    :return: Cleaned dataframe
    """

    dataframe.columns=dataframe.columns.map('/n'.join)
    dataframe.reset_index(inplace=True)
    dataframe = dataframe[dataframe['index'].notnull()]
    dataframe= pd.melt(dataframe, id_vars='index', value_vars=list(dataframe)[1:])
    dataframe = dataframe[dataframe['value'].notnull()]
    return dataframe

def dataframe_addColumns(dataframe,file, project_name, sheet,Validation_key):
    """
    :param dataframe: The cleaned dataframe
    :param file: The excel file name
    :param sheet: The excel tab name
    :return: Dataframe with new columns appended
    """

    dataframe['ProjectName'] = project_name
    dataframe['FileName'] = file
    dataframe['TabName'] = sheet
    dataframe['TabType'] = sheet.split('_')[0]
    dataframe[['ColumnName', 'ColumnDescription']] = dataframe['variable'].str.split('/n', n=1, expand=True)
    dataframe=dataframe.drop(columns=['variable'])
    dataframe['Validation_Key']= Validation_key
    dataframe= dataframe.rename({'index': 'CaseID', 'value':'ColumnValue'}, axis=1)
    dataframe = dataframe.reindex(['CaseID','ColumnName', 'ColumnDescription','ColumnValue','ProjectName','FileName','TabName',
                                   'TabType', 'Validation_Key'], axis=1)
    dataframe['ColumnValue'] = dataframe.ColumnValue.astype(str)
    return dataframe


