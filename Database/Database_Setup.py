from settings import cur


cur.execute(
    "CREATE TABLE Validation(Validation_Key INTEGER PRIMARY KEY AUTOINCREMENT,  Validation_Date STR, Status STR)"
            )

cur.execute(
    "CREATE TABLE Excel_Values(ID INTEGER PRIMARY KEY AUTOINCREMENT, CaseID STR,"
    "ColumnName STR,ColumnDescription STR, ColumnValue STR,"
    "ProjectName STR, FileName STR, TabName STR, TabType STR,"
    "Validation_Key STR,"
    "FOREIGN KEY(Validation_Key) REFERENCES Validation(Validation_Key)"
    ")"
            )