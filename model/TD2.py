import pandas as pd
import os 
from datetime import datetime
fin_matinee = datetime.strptime('12:00:00', '%H:%M:%S')
fin_journee = datetime.strptime('18:00:00', '%H:%M:%S')

def charger_donnees(path, delete_missing_values=True):
    if not os.path.exists(path):
        raise FileNotFoundError(f'Le fichier {path} est introuvable')
    data = pd.read_csv(path,delimiter=";")
    if delete_missing_values:
        data = data.dropna(subset=['Forward_Number', 'End Time'])
    return data

def filtrer_dates(data, init_date, end_date):
    if isinstance(init_date, str):
        init_date = pd.to_datetime(init_date, format='%Y-%m-%d')  # Format ISO8601
    if isinstance(end_date, str):
        end_date = pd.to_datetime(end_date, format='%Y-%m-%d')    # Format ISO8601
    date_series = pd.to_datetime(data['Date'], format='%d/%m/%Y')  # Format des dates dans le fichier CSV
    return data[(date_series >= init_date) & (date_series <= end_date)]

def to_seconds(h_m_s):
	nb_hours = int(h_m_s[0:2])
	nb_minutes = int(h_m_s[3:5])
	nb_seconds = int(h_m_s[6:])
	return nb_hours*3600 + nb_minutes*60 + nb_seconds

def aux_agreger(data):
    # Définir les heures de fin de matinée et de fin de journée
    fin_matinee = datetime.strptime('12:00:00', '%H:%M:%S').time()
    fin_journee = datetime.strptime('18:00:00', '%H:%M:%S').time()

    # Créer une copie du DataFrame pour éviter de modifier l'original
    df = data.copy()

    # Convertir la colonne 'Date' en datetime
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')

    # Convertir la colonne 'Heure' en datetime et extraire uniquement l'heure
    df['Heure'] = pd.to_datetime(df['Heure'], format='%H:%M:%S').dt.time

    # Convertir la colonne 'Duration' en secondes
    df['Duration'] = df['Duration'].apply(to_seconds)

    # Assigner les périodes de la journée (Matin, Après-midi, Soirée)
    df['Periode'] = df['Heure'].apply(
        lambda x: 'Matin' if x < fin_matinee else ('Après_midi' if x < fin_journee else 'Soiree')
    )

    # Assigner le jour de la semaine (0 = Lundi, 6 = Dimanche)
    df['Day'] = df['Date'].dt.weekday

    # Assigner la semaine de l'année
    df['Week'] = df['Date'].dt.isocalendar().week

    return df
    
def aggregate_data(data):
    # Appliquer la fonction aux_agreger pour préparer les données
    df = aux_agreger(data)

    # Vérifier que les colonnes nécessaires existent
    if 'Duration' not in df.columns or 'Periode' not in df.columns:
        raise ValueError("Les colonnes 'Duration' ou 'Periode' sont manquantes après l'agrégation.")

    # Agrégation des données
    aggregation = {
        'Duration': ['sum', 'mean'],  # Somme et moyenne de la durée
        'Periode': 'count'           # Nombre d'appels par période
    }

    # Agrégation par jour
    daily_aggregation = df.groupby('Day').agg(aggregation)

    # Agrégation par semaine
    weekly_aggregation = df.groupby('Week').agg(aggregation)

    # Agrégation par période de la journée
    time_of_day_aggregation = df.groupby('Periode').agg(aggregation)

    return daily_aggregation, weekly_aggregation, time_of_day_aggregation


path = 'model/appels_tel.csv'
data = charger_donnees(path)
daily_agg, weekly_agg, time_of_day_agg = aggregate_data(data)

select_feature = 'Calling_IMEI'
def get_unique_values_appels():
    return data[select_feature].unique()