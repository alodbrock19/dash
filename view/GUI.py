import plotly.express as px

from dash import dcc
from dash import dash_table

def build_dropdown_menu(menu_items):
    return dcc.Dropdown(
        id="dropdown",
        options=[{"label": x, "value": x} for x in menu_items],
        value=menu_items[0],
        clearable=False,
    )

def init_graph():
    return dcc.Graph(id="bar-chart")

def build_figure(df, attributes):
    x, y, z = attributes
    fig = px.bar(df, x=x, y=y,
                 color=z, barmode="group")
    return fig

def data_table(dataframe):
    return dash_table.DataTable(id="datatable",
                                data=dataframe.to_dict('records'),
                                columns=[{"name": i, "id": i, "hideable": True} for i in dataframe.columns],
                                page_size=30,
                                sort_action="native",
                                sort_mode="multi",
                                editable=True,
                                style_data={'whiteSpace': 'normal', 'height': 'auto'},
                                )
