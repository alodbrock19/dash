# script pour alimenter la base de données
import sqlite3
import csv

connexion = sqlite3.connect('Pyrenees.db')
cursor = connexion.cursor()

def build_insert_query(table_name, field_array, value_array):
	field_stub = ', '.join(["'{}'" for i in range(len(field_array))])
	value_stub = ', '.join(["'{}'" for i in range(len(value_array))])
	base_query = "INSERT INTO {} ({}) VALUES ({})".format(table_name, field_stub, value_stub)
	query = base_query.format(*field_array, *value_array)
	return query

def build_select_query(table_name, field, value):
	query = "SELECT id FROM {} WHERE {}='{}'".format(table_name, field, value)
	return query

# X_db_fields = les noms des champs utilises dans la base de donnees
# X_value_fields = les noms correspondant utilises dans le fichier csv

vallee_db_fields = ['nom']
vallee_value_fields = ['Valley']

station_db_fields = ['nom', 'range', 'altitude', 'vallee_id']
station_value_fields = ['Station', 'Range', 'Altitude']

arbre_db_fields = ['code', 'espece', 'VH', 'H', 'SH', 'station_id']
arbre_value_fields = ['code', 'Species', 'VH', 'H', 'SH']

recolte_db_fields = ['harv_num', 'DD', 'harv', 'Year', 'Date', 'Mtot', 'Ntot', 'Ntot1', 'oneacorn',\
					 'tot_Germ', 'M_Germ', 'N_Germ', 'rate_Germ', 'arbre_id']
recolte_value_fields = ['harv_num', 'DD', 'harv', 'Year', 'Date', 'Mtot', 'Ntot', 'Ntot1', 'oneacorn',\
					 'tot_Germ', 'M_Germ', 'N_Germ', 'rate_Germ']

# construction des entites / les caracteristiques des donnees font en sorte
# que nous n'avons pas d'association a construire (tout est en relation 1:N)
# il suffit d'importer la cle etrangere dans la table de l'entite associee
with open('../Repro_IS.csv', 'r') as csvfile:
	reader = csv.DictReader(csvfile, delimiter=';')
	for row in reader:
		# vallee
		vallee_nom = row['Valley']
		query = build_select_query('vallee', 'nom', vallee_nom)
		result = cursor.execute(query)
		try:
			vallee_id = result.fetchone()[0]
		except TypeError:
			values = [row[f] for f in vallee_value_fields]
			query = build_insert_query('vallee', vallee_db_fields, values)
			result = cursor.execute(query)
			vallee_id = cursor.lastrowid

		# station
		station_nom = row['Station']
		query = build_select_query('station', 'nom', station_nom)
		result = cursor.execute(query)
		try:
			station_id = result.fetchone()[0]
		except TypeError:
			values = [row[f] for f in station_value_fields]
			values.append(vallee_id)
			query = build_insert_query('station', station_db_fields, values)
			result = cursor.execute(query)
			station_id = cursor.lastrowid

		# arbre
		arbre_code = row['code']
		query = build_select_query('arbre', 'code', arbre_code)
		result = cursor.execute(query)
		try:
			arbre_id = result.fetchone()[0]
		except TypeError:
			values = [row[f] for f in arbre_value_fields]
			values.append(station_id)
			query = build_insert_query('arbre', arbre_db_fields, values)
			print(query)
			result = cursor.execute(query)
			arbre_id = cursor.lastrowid

		# recolte
		fields = []
		values = []
		for i, v in enumerate(recolte_value_fields):
			if row[v] != 'NA':
				fields.append(recolte_db_fields[i])
				values.append(row[v])
		fields.append('arbre_id')
		values.append(arbre_id)
		query = build_insert_query('recolte', fields, values)
		result = cursor.execute(query)

connexion.commit()
connexion.close()