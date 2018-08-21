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

cc5 = 'rgba(250,250,250,0.7)'
cc7 = 'rgba(23,123,150,0.9)'
cc8 = 'rgba(10,10,10,0.9)'


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
            html.Div(id='dump_test4'),
            html.Div(dcc.Graph(id='act_scores'),        
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
Output('act_scores', 'figure'),
[Input('dump_test4', 'children'),
 Input('url', 'pathname')
])


def update_test_scores(inst1,url_string):
    
    
    print 'url_string: ',url_string
    
    url = urllib.unquote_plus(url_string).decode('utf8')
    print 'decoded url: ',url
    json_string = url.split('/actscores/')[-1]
    ts_dict = json.loads(json_string)
    print 'decoded my_dict',ts_dict

    #score_type = test_scores_dict.keys()
    #xlabels = my_dict['xlabels']
    #ylabels = my_dict['ylabels']  
    act_list = ['act_cm','act_en','act_mt','act_wr']
    y = []
    x_25 = []
    x_mid = []
    x_75 = []
    x_rest = []
    x2 = []
    x3 = []

    for item in act_list:
        try:
            y.append('ACT '+ts_dict[item][3])
            x_25.append(ts_dict[item][0])
            x_mid.append(ts_dict[item][1])
            x_75.append(ts_dict[item][2])
            x2i = ts_dict[item][0] + ts_dict[item][1]
            x3i = x2i + ts_dict[item][2]
            if item == 'act_wr':
                x4i = 12 - x3i
            else:
                x4i = 36 - x3i                
                
            x_rest.append(x4i)                
            x2.append(x2i)
            x3.append(x3i)

        except KeyError:
            pass
    
    trace1 = go.Bar(
        y = y, x = x_25, orientation = 'h', text=['25 percentile: '+str(xi) for xi in x_25],
        hoverinfo='text',
        marker=dict(
            color=cc5,
            line=dict(
                color=cc8,
                width=1.5,
            )
        ),        
    )
    
    trace2 = go.Bar(
        y = y, x = x_mid, orientation = 'h', text=['median: '+str(x2i) for x2i in x2],
        hoverinfo='text',
        marker=dict(
            color=cc7,
            line=dict(
                color=cc8,
                width=1.5,
            )
        ),        
    )
    
    trace3 = go.Bar(
        y = y, x = x_75, orientation = 'h', text=['75 percentile: '+str(x3i) for x3i in x3],
        hoverinfo='text',      
        marker=dict(
            color=cc7,
            line=dict(
                color=cc8,
                width=1.5,
            )
        ),        
    )
    
    trace4 = go.Bar(
        y = y, x = x_rest, orientation = 'h', text=['', '', ''],
        hoverinfo='text',       
        marker=dict(
            color=cc5,
            line=dict(
                color=cc8,
                width=1.5,
            )
        ),        
    )    
    
    #hoverinfo = 'x+text',
    title1 = ""

    data = [trace1,trace2,trace3,trace4,
        #go.Bar(x=xlabels,y=ylabels,
        #           orientation = 'h',
        #           marker = dict(color=cc7),
                   #hoverinfo=hoverinfo
        #          )
    ]

    layout = go.Layout(title=title1,showlegend=False,hovermode = 'closest',
                           barmode='stack',
                      margin={'l': 100, 'b': 40, 't': 40, 'r': 40},
                      height=205)
    
    return {
        'data': data,'layout': layout
        }

