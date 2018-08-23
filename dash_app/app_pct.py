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
cc6 = 'rgba(188, 204, 209,0.4)'
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
            html.Div(id='dump_test2'),
            html.Div(dcc.Graph(id='pct_satisfaction2'),        
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


#pct_satisfaction
@app.callback(
Output('pct_satisfaction2', 'figure'),
[Input('dump_test2', 'children'),
 Input('url', 'pathname')
])
def update_pct_satisfaction(inst1,url_string):
    
    #hoverinfo = 'label+percent'
    
    url = urllib.unquote_plus(url_string).decode('utf8')
    json_string = url.split('/pct/')[-1]
    symbol_qnty_dict = json.loads(json_string)

    y_list = []
    ann_list = []

    for k in symbol_qnty_dict.keys():
        y_list.append(symbol_qnty_dict[k][3])
        ann_list.append(k)
        
    y_ann = [list(x) for x in zip(*sorted(zip(y_list,ann_list), key=itemgetter(0) )) ]
    random_y = y_ann[0]
    ann_text = y_ann[1]
    random_x = [(1.3 - i*0.08) for i in range(len(random_y))]

    text1 = ['<b>'+symbol_qnty_dict[i][2]+' :</b> '+str(symbol_qnty_dict[i][0])+'<br><b>National avg.:</b> '+str(symbol_qnty_dict[i][1])+'<br>' for i in ann_text ]
    
    # Create a trace
    trace = go.Scatter(
        x = random_x,
        y = random_y,
        mode = 'markers',
        text = text1,
        hoverinfo = "text",
        marker=dict(size=35,opacity=0.5,color='rgba(0,0,0,0.2)',
            line=dict(width=3,color=cc7))        
    )    
       
    layout = go.Layout(
    shapes=[#dict(type='line',x0=0.0,y0=0.0,x1=1.0,y1=1.0,line=dict(color='red',width=3),),
        dict(type='line',x0=0.0,y0=random_y[i],x1=(random_x[i]-0.1),y1=random_y[i],
             line=dict(color=cc7,width=3)) for i in range(len(random_y))],
    yaxis=dict(
        range=[0,100],
        showgrid=False,
        tick0=0.0,
        dtick=50.0,
    ),
    xaxis=dict(
        range=[0,1.5],
        showline=False,
        showgrid=False,        
        #tickfont=dict(
            #size=0)),
        showticklabels=False,
    ),
    annotations=[dict(x=random_x[i],y=random_y[i],text=ann_text[i],showarrow=False,) for i in range(len(random_y))],
    #annotations=[dict(text=ann_text[i],showarrow=False,) for i in range(len(random_y))],        

    images= [dict(source='data:image/png;base64,{}'.format(encoded_sm),xref= "paper",yref= "paper",
                x= -0.1,y= 0.95,sizex= 0.15,sizey= 0.15,xanchor= "right",yanchor= "bottom"),
             dict(source='data:image/png;base64,{}'.format(encoded_me),xref= "paper",yref= "paper",
                x= -0.1,y= 0.47,sizex= 0.15,sizey= 0.15,xanchor= "right",yanchor= "bottom"),
             dict(source='data:image/png;base64,{}'.format(encoded_fr),xref= "paper",yref= "paper",
                x= -0.1,y= -0.02,sizex= 0.13,sizey= 0.13,xanchor= "right",yanchor= "bottom")],
    
    hoverlabel=dict(bgcolor=cc6,),
    width=400,
    height=750,
    plot_bgcolor=cc5,
    title='Percentile rank compared to national stat*',
    hovermode='closest',
    showlegend=False,
    )    

    data = [trace]

    
    return ({
        'data': data,'layout': layout
        })
