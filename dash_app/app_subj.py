import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_table_experiments as dt
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import json,ast, shelve, re, urllib
from config import set23_rand,col_list, col_list2, tr_dict, \
    dist_cal, state_list, region_dict,loc_type_dict, acad_type_dict, table_col_list, table_col_dict, contact_options_dict, msg_len_max,pct_rank_qnty_dict, available_indicators,table_col_present_dict,MAX_RESULTS #,set23,nat_set234_mean
from flask_app import flask_app, db, subj_dict
from flask_app.models import Nat_avg, School_details, Zip_to_latlong, Wiki_summary, Message #Email
from flask_app.utils import haversine_np, order_pop_subs
import base64
from operator import itemgetter
from sqlalchemy.sql import text

from app import app

cc7 = 'rgba(23,123,150,0.9)'


image_sm = 'flask_app/static/assets/tu.png'
image_me = 'flask_app/static/assets/meh.png'
image_fr = 'flask_app/static/assets/td.png'
image_beta = 'flask_app/static/assets/beta1.png'


#Including images for one of the plots
encoded_sm = base64.b64encode(open(image_sm, 'rb').read())
encoded_me = base64.b64encode(open(image_me, 'rb').read())
encoded_fr = base64.b64encode(open(image_fr, 'rb').read())
encoded_beta = base64.b64encode(open(image_beta, 'rb').read())

layout = html.Div([
    #---------------------------------
    #Subj bar chart
    #
    html.Div([        
        html.Div(children=[
            html.Div(id='dump_test'),
            html.Div(dcc.Graph(id='subj_bar2'),        
                    ),
        ], className='twelve columns'),                                    
    ], className='container'),
    #---------------------------------
    #Percentile satisfaction chart and numbers at a glance
    #

],# className='container')
className='twelve columns')

#################################################################################
#Layout ends above; callbacks start below
#################################################################################


#callback7: make the bar charts of some financial info, based on dump1

@app.callback(
Output('subj_bar2', 'figure'),
[Input('dump_test', 'children'),
 Input('url', 'pathname')
])


def update_subject_bar(inst1,url_string):
    
    url = urllib.unquote_plus(url_string).decode('utf8')
    json_string = url.split('/popsub/')[-1]
    my_dict = json.loads(json_string)

    xlabels = my_dict['xlabels']
    ylabels = my_dict['ylabels']    
    
    #hoverinfo = 'label+percent'
    title1 = "Popular subjects"

    data = [go.Bar(x=xlabels,y=ylabels,
                   marker = dict(color=cc7),
                   #hoverinfo=hoverinfo
                  )]

    layout = go.Layout(title=title1,showlegend=False,hovermode = 'closest',
                      margin={'l': 40, 'b': 200, 't': 40, 'r': 40},
                      height=415)
    
    return {
        'data': data,'layout': layout
        }

