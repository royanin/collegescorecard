import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import plotly.graph_objs as go
import pandas as pd
import json
from flask_sqlalchemy import SQLAlchemy

from app import app
from dash_app import app_table#, search
from flask_app import views

print(dcc.__version__) # 0.6.0 or above is required


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    html.Div(id='inst_opeid', style={'display': 'none'}),
    html.Div(dt.DataTable(rows=[{}]), style={'display': 'none'}),
    html.Div(dcc.Graph(id='dummy_g1'), style={'display': 'none'}),
    html.Div(dcc.RadioItems(), style={'display': 'none'}),    
    html.Div(dcc.Dropdown(), style={'display': 'none'}),
    html.Div(dcc.Tabs(tabs=[{}]), style={'display': 'none'}),
    html.Div(id='dummy_div1', style={'display': 'none'})
    #The 5 lines above are super important to initiate the dcc or dt components so they
    #can be displayed when called. Otherwise it'll show no error and just a white page
])

# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url','pathname')])
def display_page(pathname):
    pathname = str(pathname)
    
    if pathname == '/':
        return app_table.layout
    else:
        return '404'    

    # You could also return a 404 "URL not found" page here



if __name__ == '__main__':
    app.run_server(debug=True)
