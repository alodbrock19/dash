from dash import Dash, dash_table
import pandas as pd

df = pd.read_csv('Repro_IS.csv', sep=';')
columns = [{'name': c, 'id': c} for c in list(df.columns)]

app = Dash(__name__)

app.layout = dash_table.DataTable(data=df.to_dict('records'), columns=columns)

if __name__ == '__main__':
    app.run_server(debug=True)