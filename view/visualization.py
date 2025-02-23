def visualization(data):
    """
    Crée un scatter plot avec Plotly :
    - Axe des x : Date
    - Axe des y : Duration
    - Couleur des points : Periode (Matin, Après-midi, Soirée)
    """
    # Créer le scatter plot
    fig1 = px.scatter(
        data,
        x='Date',              # Colonne pour l'axe des x
        y='Duration',          # Colonne pour l'axe des y
        color='Periode',       # Colonne pour la couleur des points
        labels={
            'Date': 'Date',
            'Duration': 'Durée (secondes)',
            'Periode': 'Moment de la journée'
        }
    )
    
    data['Day of Week'] = data['Date'].dt.day_name()

    fig2 = px.sunburst(
        data,
        path=['Day of Week', 'Periode'],
    )
    
    fig3 = px.violin(
        data,
        x='Periode',
        y='Duration',
    )
    
def scatter(data):
    