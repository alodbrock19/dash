import sqlite3

db_path = './Pyrenees.db'
db = sqlite3.connect(db_path)
cursor = db.cursor()

create_query = 'CREATE TABLE "Pyrenees" (\
    ID text,\
    code text,\
    Valley text,\
    Station text,\
    Range int,\
    Altitude int,\
    Species text,\
    DD int,\
    Year int,\
    harv_num int,\
    harv int,\
    Date text,\
    Ntot1 int,\
    Ntot int,\
    Mtot real,\
    oneacorn real,\
    VH real,\
    H real,\
    SH real,\
    tot_Germ int,\
    M_Germ real,\
    N_Germ int,\
    rate_Germ real,\
    PRIMARY KEY (ID, Date));'

cursor.execute(create_query)
db.commit()

