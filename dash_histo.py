import model.data
import view.GUI
import dash
from dash import html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

dropdown = view.GUI.build_dropdown_menu(model.data.get_unique_values())
graph = view.GUI.init_graph()

app.layout = html.Div([
    dropdown, graph
])

@app.callback(
    Output(graph.id, "figure"),
    [Input(dropdown.id, "value")])
def update_bar_chart(value):
    sub_df, attributes = model.data.extract_df(value)
    return view.GUI.build_figure(sub_df, attributes)

if __name__=='__main__':
	app.run_server(debug=True)