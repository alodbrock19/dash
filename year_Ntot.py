import pandas as pd
import plotly.express as px

df = pd.read_csv('Repro_IS.csv', sep=';')

# df_agreg = df[['Year', 'Ntot']].groupby(by="Year", dropna=False).sum()
#df_agreg = df[['Station', 'Ntot']].groupby(by="Station", dropna=False).sum()
df_agreg = df[['Year', 'Station', 'Ntot']].groupby(by=["Station", "Year"]).sum()
df_agreg = df_agreg.reset_index()
df_agreg.head()

#fig = px.bar(df_agreg, x='Station', y='Ntot')
fig = px.bar(df_agreg, x="Year", y="Ntot", color="Station")

fig.show()
