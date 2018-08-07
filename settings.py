import sqlite3


file_paths = [['/Users/akalambur/Documents/SAW/Test2/'], ['/Users/akalambur/Documents/SAW/Test1/']]
con = sqlite3.connect("/Users/akalambur/Documents/SAW/Database/excelTable.sqlite",isolation_level=None)
cur = con.cursor()



