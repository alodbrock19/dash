import plotly.express as px

def build_figure(data,value):
    fig = px.bar(data[data['Periode']==value],
                 x = 'Date',
                 y = 'Duration')
    return fig