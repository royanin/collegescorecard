from config import set23_rand,col_list, col_list2, tr_dict, \
    dist_cal, state_list, region_dict,loc_type_dict, acad_type_dict, table_col_list, table_col_dict, contact_options_dict, msg_len_max,pct_rank_qnty_dict, available_indicators,table_col_present_dict,MAX_RESULTS 
import json
import pandas as pd
import numpy as np
import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_table_experiments as dt
import plotly.graph_objs as go
from flask_app.utils import make_no2_test_dict



cc1 = '#efe9cb'
cc2 = 'rgba(12,67,220,0.7)'
cc3 = 'rgba(220,20,20,0.9)'
cc4 = 'rgba(244,174,61,1.0)'
cc5 = 'rgba(250,250,250,0.7)'
cc6 = 'rgba(188, 204, 209,0.4)'
cc7 = 'rgba(23,123,150,0.9)'
fs15= '15px'
style1 = {'background-color':cc1}
round1 = {'padding':'20px','border': '2px solid #1fa5c4', 'border-radius' : '5px', 'background-color':'rgba(161, 193, 201,0.1)'
         }


    
def update_graph_make_plot(xaxis_column_name, yaxis_column_name,xaxis_type, yaxis_type,json_dataset,inst1):
    
    no_avg_detect = ['Value_score', 'Care_score', 'r_fin_COMB_RET_RATE'] #
    
    if json_dataset is None:
        df_sel2 = set23_rand
    else:    
        datasets = json.loads(json_dataset)
        df_sel2 = pd.read_json(datasets['df_sel'], orient='split')    
    

    df_sel = df_sel2[list(set(['INSTNM',xaxis_column_name,yaxis_column_name]+table_col_list
                              +table_col_present_dict.values() ) )]
    sel_inst = json.loads(json.loads(inst1))
    list_len = df_sel[yaxis_column_name].count()
    
    if (xaxis_column_name in no_avg_detect):
        df_sel.is_copy = False
        df_sel['qts_present'] = np.ones(list_len)
    else:
        df_sel.is_copy = False
        #df_sel['qts_present'] = df_sel.apply(lambda row: row[table_col_present_dict[xaxis_column_name]], axis=1)
        df_sel['qts_present'] = df_sel.apply(lambda row: row[xaxis_column_name], axis=1)
    
    if (yaxis_column_name in no_avg_detect):
        df_sel.is_copy = False
        df_sel['qts_present'] = df_sel.apply(lambda row: row['qts_present']+ 1.0, axis=1)       
    else:
        df_sel.is_copy = False
        df_sel['qts_present'] = df_sel.apply(lambda row: row['qts_present']+row[yaxis_column_name], axis=1)    

    
    
 
    df_color1 = df_sel[df_sel['qts_present']<0.5] #[['INSTNM',xaxis_column_name,yaxis_column_name]]
    df_color2 = df_sel[df_sel['qts_present']>=0.5] #[['INSTNM',xaxis_column_name,yaxis_column_name]]  


    color1 = cc3
    color2 = cc2
    trace1 = go.Scatter(
            x=df_color1[xaxis_column_name],
            y=df_color1[yaxis_column_name],
            text=df_color1['INSTNM'],
            name='Missing values replaced by avg.*',
            showlegend=True,
            mode='markers',
            marker={'size': 15,'opacity': 0.5, 'color':cc3}
        )
    
    trace2 = go.Scatter(
            x=df_color2[xaxis_column_name],
            y=df_color2[yaxis_column_name],
            text=df_color2['INSTNM'],
            name='Reported values',
            showlegend=True,
            mode='markers',
            marker={'size': 15,'opacity': 0.5, 'color':cc7}
        )   

    trace_dd = go.Scatter(
        x = [sel_inst[xaxis_column_name]],
        y = [sel_inst[yaxis_column_name]],
        text = sel_inst['INSTNM'],
        name = sel_inst['INSTNM'],
        showlegend=True,
        mode='markers',
        marker={'size': 20,'opacity': 1.0,'color' : 'black','symbol' : "circle-open",'line' : {'width':5,},
        }
    )
    traces = [trace1,trace2,trace_dd]

    layout = go.Layout(
            xaxis={
                'title': table_col_dict[xaxis_column_name],
                'type': 'log' if xaxis_type == 'log' else 'linear'
            },
            yaxis={
                'title': table_col_dict[yaxis_column_name],
                'type': 'log' if yaxis_type == 'log' else 'linear'
            },
            margin={'l': 60, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest',
            legend={'x':'-0.08',
                    'y':'-0.40',
                    #'xanchor':'right',
                    'bgcolor':'rgba(0,0,0,0.03)'}

        )

    return {
        'data': traces, 'layout' : layout
        
    }        


def create_school_overview(sel_inst,sch):
#open https: -- make sure it's there, else it'll append localhost...
    inst_url = str(sel_inst['HTTPS_INSTURL'])
    npc_url = str(sel_inst['HTTPS_NPCURL'])        
    lat = sel_inst['LATITUDE']
    long = sel_inst['LONGITUDE']
    map_range = 0.010
    bbox = [str(long - map_range), str(lat - map_range), str(long + map_range), str(lat + map_range)]
    address = str(sel_inst['STABBR'])+', '+str(sel_inst['ZIP5'])

    if str(sel_inst['REL_AFFIL']) != 'nan':
        rel_affil = sel_inst['REL_AFFIL']
    else:
        rel_affil = 'None'            
    if str(sel_inst['OTHER_AFFIL']) != 'nan':
        other_affil = sel_inst['OTHER_AFFIL']            
    else:
        other_affil = 'None'            


    map_string = "//www.openstreetmap.org/export/embed.html?bbox="+"%2C".join(bbox[:])+"&marker="+str(lat)+"%2C"+str(long)+"&layers=ND"

    return_div = [
        html.Div([
                html.H5('More details on '+sel_inst['INSTNM']),
            ],style={'text-align':'center'}, className="row"),
        html.Div([

                html.Div([
                    html.Div([
                        html.B('Location: '),
                        html.Span(sel_inst['CITY']+', '+sel_inst['STABBR']+', '+str(sel_inst['ZIP5']))
                               ]),
                    html.A(str(sel_inst['HTTPS_INSTURL']),href=inst_url, target="_blank"),
                    html.Br(),
                    html.A(str(sel_inst['HTTPS_NPCURL']),href=npc_url, target="_blank"),
                    html.Br(),
                    html.Div(children=[
                        html.B('Religious affiliation: '),
                        html.Span(rel_affil),
                    ]),
                    html.Div(children=[
                        html.B('Other affiliation(s): '),
                        html.Span(other_affil),
                    ]),

                    ],className="six columns"),
                html.Div([
                    html.Iframe(src=map_string,
                            style={'border': 'none', 'width': '100%', 'height': 300}),
                    ],className="six columns"),
                ],className="row"),
    ]

    
    
    #SAT and ACT
    no2_test_div = []
    if sch.SATVRMID != None or sch.SATMTMID != None or sch.SATWRMID != None:
        SAT_PRESENT = 1
        sat_string = make_no2_test_dict('SAT_PRESENT',sch)
        no2_test_div.append(
            html.Div([
                    html.Iframe(src="/satscores/{}".format(sat_string) ,
                            style={'border': 'none', 'width': '100%', 'height': 205}),
                    ],className="six columns")
        )
    else:
        sat_string = None
    if sch.ACTCMMID != None or sch.ACTENMID != None or sch.ACTMTMID != None or sch.ACTWRMID != None:
        ACT_PRESENT = 1
        act_string = make_no2_test_dict('ACT_PRESENT',sch)
        no2_test_div.append(
            html.Div([
                    html.Iframe(src="/actscores/{}".format(act_string),
                            style={'border': 'none', 'width': '100%', 'height': 205}),
                    ],className="six columns")
        )
    else:
        act_string = None 
        
    if len(no2_test_div) > 0:
        return_div.append(
        html.Div(no2_test_div, className="row")
        )
        
    return html.Div(return_div, className="row")
    

#https connection to those w/o it may fail. Is http connection going to work?

def fb_output(inst_fb):
    return html.Div([
                        html.Br(),
                        html.Iframe(src="https://www.facebook.com/plugins/page.php?href=https%3A%2F%2Fwww.facebook.com%2F"+inst_fb+"&tabs=timeline&width=340&height=500&small_header=true&adapt_container_width=true&hide_cover=false&show_facepile=true&appId=277208896022831",
                                   style={'border': 'none', 'width': '100%', 'height': 500}),


                    ],className="six columns")                                 
    
def tw_output(TW_HANDL):
    if TW_HANDL != "":
        print TW_HANDL
        if TW_HANDL[-1]==" ":
            TW_ALT = TW_HANDL.rstrip()
        else:
            TW_ALT = TW_HANDL
    else:
        print TW_HANDL
        TW_ALT = ""     
    return  html.Div([
                        html.Iframe(src="/twt/{}".format(TW_HANDL),
                                    style={'border': 'none', 'width': '100%', 'height': 500}
                                   ),
                    ],style={'text-align': 'right'}, className="six columns")    

def yt_output(INSTNM):
    return  html.Div([
            html.H5('Videos on Youtube: '+INSTNM),
            html.Br(),
            html.Iframe(src="https://www.youtube.com/embed?listType=search&list="+str(INSTNM)+', official',
                       style={'border': 'none', 'width': '100%', 'height': 315}),

        ], style={'text-align': 'center'},className="twelve columns")
    