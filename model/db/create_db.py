# script pour alimenter la base de données
import sqlite3

connexion = sqlite3.connect('Pyrenees.db')
cursor = connexion.cursor()

for table_name in ['arbre', 'station', 'vallee', 'recolte']:
	query = "DROP TABLE IF EXISTS '{}';".format(table_name)
	cursor.execute(query)

query = "CREATE TABLE IF NOT EXISTS vallee (\
	id INTEGER PRIMARY KEY AUTOINCREMENT,\
	nom TEXT NOT NULL\
	);"

result = cursor.execute(query)

query = "CREATE TABLE IF NOT EXISTS station (\
	id INTEGER PRIMARY KEY AUTOINCREMENT,\
	nom TEXT NOT NULL,\
	range INT NOT NULL,\
	altitude INT NOT NULL,\
	vallee_id INT NOT NULL,\
	FOREIGN KEY (vallee_id) REFERENCES vallee (id)\
	);"

result = cursor.execute(query)

query = "CREATE TABLE IF NOT EXISTS arbre (\
	id INTEGER PRIMARY KEY AUTOINCREMENT,\
	code TEXT NOT NULL,\
	espece TEXT NOT NULL,\
	VH REAL,\
	H REAL,\
	SH REAL,\
	station_id INT NOT NULL,\
	FOREIGN KEY (station_id) REFERENCES station (id)\
	);"

result = cursor.execute(query)

query = "CREATE TABLE IF NOT EXISTS recolte (\
	id INTEGER PRIMARY KEY AUTOINCREMENT,\
	harv_num INT NULL,\
	DD INT NULL,\
	harv INT NULL,\
	Year INT NULL,\
	Date TEXT NULL,\
	Mtot REAL NULL,\
	Ntot REAL NULL,\
	Ntot1 REAL NULL,\
	oneacorn REAL NULL,\
	tot_Germ INT NULL,\
	M_Germ REAL NULL,\
	N_Germ INT NULL,\
	rate_Germ REAL NULL,\
	arbre_id INT NOT NULL,\
	FOREIGN KEY (arbre_id) REFERENCES arbre (id)\
	);"

result = cursor.execute(query)

connexion.commit()
connexion.close()
