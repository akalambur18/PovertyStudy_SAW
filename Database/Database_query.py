import pandas as pd
from settings import con


def Validation_1_query(Validation_key):
    Validation_1 = pd.read_sql_query(
        "WITH duplicates AS (select CaseID, ColumnName, TabType, ColumnValue, ProjectName, count(*) from [Excel_Values] "
            "where Validation_Key= " + str(Validation_key) + " group by  CaseID, ColumnName, TabType, ProjectName "
            "having count(distinct ColumnValue) > 1 ) "
        "SELECT  a.ProjectName, a.FileName, a.TabName, a.CaseID, a.ColumnName,a.ColumnValue FROM   [Excel_Values]  a "
        "JOIN   duplicates b ON (a.CaseID = b.CaseID and  "
                                "a.ColumnName = b.ColumnName and "
                                "a.TabType = b.TabType and a.Validation_Key = " + str(Validation_key) + ")", con)

    return Validation_1

def Validation_2_query(Validation_key):
    Validation_2 = pd.read_sql_query(
        "with latest_ok_snapshot as( "
        "Select FileName, CaseID, ColumnName, ColumnValue, TabType, ProjectName, TabName from Excel_Values where Validation_Key in  "
        "(select Validation_Key from Validation "
        "where Status = 'OK' "
        "order by Validation_Date desc limit 1)), "
        "latest_snapshot as ( "
        "select FileName, CaseID, ColumnName, ColumnValue, TabType, ProjectName  from Excel_Values where Validation_Key = "+ str(Validation_key) + ")"
        "SELECT los.ProjectName, los.FileName, los.TabName, los.CaseID, los.ColumnName, los.ColumnValue as ColumnName_old, "
        "ls.ColumnValue as ColumnName_new  FROM latest_ok_snapshot  "
        "AS los Left JOIN latest_snapshot AS ls ON los.ProjectName=ls.ProjectName "
        "and los.CaseID=ls.CaseID and los.ColumnName = ls.ColumnName and los.TabType = ls.TabType "
        "WHERE (los.projectName, los.CaseID, los.ColumnName, los.ColumnValue, los.TabType) "
        "NOT IN (SELECT ProjectName, CaseID, ColumnName, ColumnValue, TabType FROM latest_snapshot)", con
    )
    return Validation_2

def file_query(Validation_key):
    files = pd.read_sql("select distinct FileName,ProjectName "
                "from Excel_Values where Validation_Key = " + str(Validation_key) + " group by ProjectName ", con)
    return files