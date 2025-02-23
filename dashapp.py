import model.data
import model.TD2
import view.GUI
import view.visualization

import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY])

# styling the sidebar
SIDEBAR_STYLE = {
	"position": "fixed",
	"top": 0,
	"left": 0,
	"bottom": 0,
	"width": "18rem",
	"padding": "2rem 1rem",
	"background-color": "#f8f9fa",
}

# padding for the page content
CONTENT_STYLE = {
	"margin-left": "18rem",
	"margin-right": "2rem",
	"padding": "2rem 1rem",
}

sidebar = html.Div(
	[
		html.H2("My Dashboard", className="display-4"),
		html.Hr(),
		html.P(
			"Appels Téléphoniques", className="lead"
		),
		dbc.Nav(
			[
				dbc.NavLink("Histogramme", href="/", active="exact"),
				dbc.NavLink("Tableur", href="/table", active="exact"),
			],
			vertical=True,
			pills=True,
		),
	],
	style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
	dcc.Location(id="url"),
	sidebar,
	content
])

@app.callback(
	Output("page-content", "children"),
	[Input("url", "pathname")]
)
def render_page_content(pathname):
	if pathname == "/":
		dropdown = view.GUI.build_dropdown_menu(model.TD2.get_period())
		graph = view.GUI.init_graph()
		return [
			html.Div([
				dropdown, graph
			])
		]

	elif pathname == "/table":
		# fetch client info
		return [
				html.H1('Données forêt pyrénnées (tableur)', id='table_view',
						style={'textAlign':'left'}),
				html.Hr(style={'width': '75%', 'align': 'center'}),
				html.Div(id="edit-message", children=[html.P("Nope")]),
				dcc.Store(id="diff-store"),
				html.Div(id='data_table_container', children = view.GUI.data_table(model.data.df))
				]

	else:
		return html.Div(
			[
				html.H1("404: Not found", className="text-danger"),
				html.Hr(),
				html.P(f"The pathname {pathname} was not recognised..."),
			]
		)

@app.callback(
    Output("bar-chart", "figure"),
    [Input("dropdown", "value")])
def update_bar_chart(value):
    data = model.TD2.agg_data
    return view.visualization.build_figure(data,value)

@app.callback(
    Output('edit-message', 'children'),
    [Input('datatable', 'active_cell'), Input('datatable', 'data'), State('datatable', 'value')],
    )
def display_output(cell, data, state):
	if cell != None:
		#print(cell)
		#print(data[0])
		i, j, col_header = cell['row'], cell['column'], cell['column_id']
		#print(model.data.df.iloc[i, j])
		#print(data[i][col_header])
		return [html.P('{}, {}, {}'.format(i, j, state))]

@app.callback(
    Output("diff-store", "data"),
    [
		Input("datatable", "data_timestamp"),
	],
    [
		State("datatable", "active_cell"),
		State("datatable", "data"),
        State("datatable", "data_previous"),
        State("diff-store", "data"),
    ],
)
def capture_diffs(timestamp, cell, data, data_previous, store_data):
	if timestamp is None:
		raise PreventUpdate
	else:
		#print('Active_cell', cell['row'], cell['column'])
		#print('Timestamp', timestamp)
		#print('Data', type(data))
		print(data)
		print(data_previous)
if __name__=='__main__':
	app.run_server(debug=True)
