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
from flask_app.utils import haversine_np, order_pop_subs, make_no2_test_dict, make_pct_satisfac_dict
from dash_func import update_graph_make_plot, create_school_overview, fb_output, tw_output, yt_output
import base64
from operator import itemgetter
from sqlalchemy.sql import text

from app import app


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

    html.Div([
        html.Div([
        html.H2(children=[
            html.Span('The Unofficial College ScoreCard'),
            html.Img(src='data:image/png;base64,{}'.format(encoded_beta),sizes= 0.15),
        ]),
        html.P('When it comes to choosing a college, we have many questions. How much debt will I have if I go to my favorite college? What will be my salary after graduation? What percentage of students graduate from this college? How good is this school compared to other schools in my reach? At CollegeScoreCard.io you can compare colleges with interactive plots and tables, (and Youtube videos and social media feeds!), all in one place, and for FREE.'),
        html.Br(),
        html.P('Numbers presented here come from official sources. At CollegeScoreCard.io we help you make sense of these important numbers.'),
        html.P(children=[html.B('DISCLAIMER:'),
                        html.Span(children=['The official college scorecard website run by US DoE is ',
                        html.A('here...',href='https://collegescorecard.ed.gov/',
                      target="_blank")]),
                     ]),
            html.Div(id='show_filter_button',children=[
                html.Button('SHOW FILTERS', id='button-toggle-filter',
                           className="btn btn-md btn-default"),
                html.P('OR'),
                html.Button(children=[html.A("SEARCH FOR A SCHOOL",href="/search")],className="btn btn-md btn-default"),                
            ]),
        ], #className="col-md-10 col-md-offset-left-1" ),
            className="twelve columns",style={'text-align':'center'} ),
    ], #className='row'),
        className='container'),
    
    html.Div([
        html.Br(),
        html.Div(id='show_all_filters',children=[
            
            html.Div(children=[  #begin new container for the filter panel
                
            #This is the first panel asking about school types
            html.Div([
                #html.Br(),
                    html.Div([
                    html.Div([                        
                        html.Div([
                            #html.B('School type: '),
                        ],className='two columns'),                        
                        html.Div([
                                dcc.Dropdown(
                                id='filter_sc_type', 
                                options=[
                                    {'label': '4-year inst.', 'value': 'four_'},
                                    {'label': '2-year inst.', 'value': 'two_'},
                                    {'label': 'Show both', 'value': 'both_'}
                                ],
                                value='four_',                         
                                multi=False,
                                placeholder='School type:',
                                ),
                        ],className='three columns'),
                        html.Div([                        
                                #html.Br(),
                                dcc.Dropdown(
                                    id='filter_sc_control', 
                                    options=[
                                        {'label': 'Public', 'value': 1},
                                        {'label': 'Private not-for-profit', 'value': 2},
                                        {'label': 'Private for-profit', 'value': 3}
                                    ],
                                 multi=True,
                                 value=[1,2,3], 
                                 #className="Select--multi1 Select-value1",
                                ),
                        ],className='seven columns',),                    
                    ],className='row'),
                    ],className='round1'),      
                    #style={"background-color":'rgba(87,123,42,0.5)'},
                        #className="col-md-4 col-md-offset-right-8" ),
                    #className='four column'),
                ],#className='four columns'),
                className='container'),
    
            #This is the second panel asking about academics
            #html.Hr(),
            html.Br(),                
            html.Div([
                html.Div([
                html.Div([                    
                html.Div([
                    #html.B('Academics: '),
                ],className='two columns'),
                html.Div([    
                dcc.Dropdown(
                    id='filter_acad_type', 
                    options=[
                        {'label': 'Ignore (Show all)', 'value': 'ignore'},
                        {'label': 'Open admission', 'value': 'open'},                        
                        {'label': 'Admission rate', 'value': 'adm'},
                        {'label': 'Avg. SAT score', 'value': 'sat'},
                        {'label': 'Avg. ACT score', 'value': 'act'}
                    ],
                    value='adm',                         
                    multi=False,
                ),
                ],className='three columns'),
                #html.Br(),
                html.Div([
                    html.Div(id='acad_1', children=[
                        html.B("No academic filter has been set.")
                    ],style={"text-align":'center'}),
                    html.Div(id='acad_2', children=[
                        html.B("Filtering for institutions with admission rate 1.0")
                    ]),
                    html.Div(id='acad_3', children=[
                        html.Div([   
                            dcc.RangeSlider(
                                id = 'adm_range',
                                marks={0.1*i: '{}'.format(0.1*i) for i in range(0, 11)},
                                min= 0.0,
                                max=1.0,
                                step = 0.1,
                                value=[0.2, 0.7],
                                #className = 'rc-slider-track-2'
                                ),
                            html.Br(),           
                            html.P("Choose the range of admission rate")
                        ])
                    ]),                
                    html.Div(id='acad_4', children=[
                        html.Div([  
                            html.Div([                            
                            #html.B("ACT Math"),            
                                dcc.Slider(
                                    id = 'act_math',
                                    marks={10*i: '{}'.format(10*i) for i in range(1, 4)},
                                    min= 0,
                                    max=36,
                                    step = 1,
                                    value= 26,
                                    ),
                            ],className='eight columns'),
                            html.Div([                           
                                html.B("ACT Math"),            
                            ],className='four columns'),                                
                        ],className='row'),
                                
                        html.Br(),           
                        html.Div([ 
                            html.Div([ 
                            #html.B("ACT English"),            
                            dcc.Slider(
                                id = 'act_verbal',
                                marks={10*i: '{}'.format(10*i) for i in range(1, 4)},
                                min= 0,
                                max=36,
                                step = 1,
                                value= 24,
                                ),
                            ],className='eight columns'),
                            html.Div([                           
                                html.B("SAT verbal"),            
                            ],className='four columns'),                                
                        ],className='row'),
                    ],className='row'),
                    #]),                    
                    html.Div(id='acad_5', children=[
                        html.Div([ 
                            html.Div([                                
                                dcc.Slider(
                                    id = 'sat_math',
                                    marks={100*i: '{}'.format(100*i) for i in range(3, 9)},
                                    min= 220,
                                    max=800,
                                    step = 10,
                                    value= 650,
                                    ),
                            ],className='eight columns'),
                            html.Div([                           
                                html.B("SAT Math"),            
                            ],className='four columns'),                                
                        ],className='row'),
                        html.Br(),           

                        html.Div([ 
                            html.Div([                            
                                dcc.Slider(
                                    id = 'sat_verbal',
                                    marks={100*i: '{}'.format(100*i) for i in range(3, 9)},
                                    min= 220,
                                    max=800,
                                    step = 10,
                                    value= 650,
                                    ),
                            ],className='eight columns'),
                            html.Div([                           
                                html.B("SAT verbal"),            
                            ],className='four columns'),                                
                        ],className='row'),
                    ],className='row'),    
                    
                ],className='seven columns',style={"text-align":'center'}),
                ],className='row'),
                ],className='round1'),                    
             ],className='container'),
            html.Br(),
            #html.Hr(),                
            #This is the third panel asking about location                
            html.Div([  
                html.Div([                 
                html.Div([
                    html.Div([
                        #html.B('Location/'),
                        #html.Br(),
                        #html.B('distance: '),
                    ],className='two columns'),
                    html.Div([    
                    
                        dcc.Dropdown(
                            id='filter_loc_type', 
                            options=[
                                {'label': 'Ignore', 'value': 'ignore'},                        
                                {'label': 'Distance', 'value': 'dist'},
                                {'label': 'State', 'value': 'state'},                        
                                {'label': 'Region', 'value': 'region'},
                            ],
                            value='dist',                         
                            multi=False,
                        )
                    ],className='three columns'),                        
                #html.Br(),

                    html.Div([
                    
                        html.Div(id='loc_1', children=[
                            html.B("No location filter has been set.", id='loc-ignore')
                            ]),
                    
                        html.Div(id='loc_2', children=[
                            html.Div([
                                html.Div([
                                        html.Div([   
                                            dcc.Input(
                                                id="loc_dist_range",
                                                placeholder='miles',
                                                type='number',
                                                value='100',
                                                style= {'display': 'inline-block', 'width': '100%'}
                                            ),
                                            
                                        ],className='three columns'),                                            
                                        html.Div([
                                            html.P("miles of zipcode"),
                                        ],className='five columns'),#,style = {'display': 'inline-block', 'width': '50%'}),
                                        html.Div([
                                            dcc.Input(
                                            id="loc_dist_center",
                                            placeholder='US zipcode',
                                            type='text',
                                            value='02139',
                                            style= {'display': 'inline-block', 'width': '100%'}
                                        ),
                                        ],className='four columns'),
                                    ],className='row'),#,style = {'display': 'inline-block', 'width': '100%'}
                                #),
                        
                            ]),
                        ]),                            
                    
                        html.Div(id='loc_3', children=[
                                    html.Div([   
                                        dcc.Dropdown(
                                            id='loc_state', 
                                            options=[ {'label':st, 'value':st } for st in state_list ],
                                            value='MA',                         
                                            multi=False,
                                        ),          
                                        #html.B("Choose a US state/territory")
                                    ])                                                
                            ],style= {'display': 'inline-block', 'width': '50%'}),

                        html.Div(id='loc_4', children=[
                                      html.Div([   
                                            dcc.Dropdown(
                                                id='loc_region', 
                                                options=[ {'label':k, 'value':region_dict[k] } for k in region_dict ],
                                                value=1,                         
                                                multi=False,
                                            ),          
                                            #html.B("Choose a region")
                                      ],)
                            ]),                     
                         
                #]),                
                ],className='seven columns',style={'text-align': 'center'}),
            ], className='row'),
            ], className='round1'),                    
            ], className='container'),
            #html.Br(),    
            ]#, className='container',style={'background-color': cc1}
            ),
            #----------------------------------
            #end container for the filter panel
            #----------------------------------                
            #html.Hr(), 
            html.Br(),                            
            #----------------------------------
            #begin container for the submit button and hide filter panel
            #----------------------------------                            
            html.Div([ 
            #html.Br(),
            html.Div([
                    html.Div(id='filter-selection'),
                    html.Br(),
                    html.Button('HIDE FILTERS', id='button-hide-filter',
                               className="btn btn-md btn-default"),
                    html.Button('SUBMIT', id='button-submit-filter',
                                className="btn btn-md btn-primary",style={'background-color':
                                                                         cc7}),                
                    #html.Div(id='show_filter_selection', children=[]),                

            ], style={'text-align':'center'}#className="col-lg-2 col-lg-offset-left-5 col-md-2 col-md-offset-left-5" )
             #className="col-xl-6 col-lg-6 col-md-6 text-center")
            )
            ], className='container'),  
            #----------------------------------    
            #end container for the submit button
            #----------------------------------                
            ],className='row',style={'display': 'none'})
    ], className='row'),

    html.Div([
        html.Div([
            html.Div([
            #html.Hr(),    
    
            html.Div(id='filter-output', style={'display': 'none'}),
            #Have this filter-output only in the interim -- to be replaced by tab-output
            html.Div(id='loc-dump', style={'display': 'none'}),
            html.Div(id='dump1', 
                     style={'display': 'none'}),
            html.Div(id='dump2', 
                     children=("abcdefghijklmnop"),
                     style={'display': 'none'}),                
            html.Div(dt.DataTable(rows=[{}],columns=[]), style={'display': 'none'}),
            ], style={
                'width': '90%',
                'fontFamily': 'Sans-Serif',
                'margin-left': 'auto',
                'margin-right': 'auto'
            }),
        ], className='three columns'),
        
    ],  style={'display': 'none'}, className='container'),
    
    html.Hr(),
    
    #
    #Table block
    #
    html.Div([
        html.Div([
                html.Div(id='table_desc',
                        #style={'color': 'grey', 'font-size' : '15px'}
                        ),
                dt.DataTable(
                    rows=[{}],
                    #rows= set23_rand.to_dict('records'),
                    
                    columns=[],                    
                    row_selectable=False,
                    filterable=True,
                    sortable=True,
                    editable=False,
                    id='datatable-ranking',

                    )
                ]),
                html.Details([
                html.Summary("Select columns shown in the table above",
                              style={'color': 'grey', 'font-size' : '15px'}
                ),
                html.Div([
                    html.Br(),
                    dcc.Checklist(id='col_select_checklist', 
                    options = [ {'label':table_col_dict[i], 'value':table_col_dict[i] } for i in table_col_list[3:] ],
                    values=['School', 'Value score','Care score'],
                    labelStyle={'display': 'inline-block'}
                                  
                    ),
                    html.Br(),
                    ],className=round1),
                ]),
                html.Details([
                html.Summary("Did you know you could sort and filter these table columns?",
                              style={'color': 'grey', 'font-size' : '15px'}
                ),
                html.Div([
                    html.P("Click on the column name on any column (e.g., on Value Score),\
                    and it can sort the entire table based on the values low-to-high or \
                    high-to-low in this column."),
                    html.Br(),
                    html.P("To filter any column, click on the 'FILTER ROWS' button on the \
                    upper right corner of the table, and then insert your filtering condition \
                    (e.g., type '>50' under the value score column. Click on the 'FILTER ROWS \
                    button again to dismiss the prompts.')"),
                    html.Br(),
                    html.P("And don't forget to check out other quantities you can see on the table!")
                ],style=round1,
                #className=round1
                ),
        
                ]),
                html.A('What do these quantities mean?',href='/explainer',
                      target="_blank"),
        
        
            ], className='container'),
    
    #
    #Institute dropdown block
    #
    html.Div([
        #html.Br(),
        html.Div([
                html.Div([            
                    html.H5("Choose a school to view details:",className="five columns"),
                    dcc.Dropdown(id='inst_dropdown', 
                             multi=False,
                             placeholder='Choose a school',
                             options = [ {'label': i, 'value': j} for (i,j) in          zip(set23_rand['INSTNM'].tolist(),set23_rand['uid'].tolist()) ],
                             #value = options[0]['value'],
                             value = set23_rand.iloc[0]['uid'],
                            className="seven columns"),
                    ], className='row'),
                ], className='round1'),            
            ], className='container'),

    #
    #scatter plot description starts here...
    #
    #---------------------------------    
    html.Div([
        #html.H5(''),
        html.Div(id='crossfilter-scatter-title'),
    ],className='container'),
    
    html.Div([
        html.Div([
            html.Div(dcc.Graph(id='crossfilter-indicator-scatter')),
            
            ], className='eight columns'),
        html.Div([
            html.Div(id='crossfilter-numbers'
                    ),
            html.Hr(),
            html.Br(),            
            html.B('X axis:'),
            html.Br(),
            dcc.Dropdown(
                id='crossfilter-xaxis-column',
                #options=[{'label': i, 'value': i} for i in table_col_list[3:]],
                options=[{'label': table_col_dict[i], 'value': i} for i in table_col_list[3:]],
                value='Care_score'
            ),
            dcc.RadioItems(
                id='crossfilter-xaxis-type',
                options=[{'label': i, 'value': i} for i in ['linear', 'log']],
                value='linear',
                labelStyle={'display': 'inline-block'}
            ),
            html.Br(),
            #html.Br(),    
            html.B('Y axis:'),
            html.Br(),            
            dcc.Dropdown(
                id='crossfilter-yaxis-column',
                options=[{'label': table_col_dict[i], 'value': i} for i in table_col_list[3:]],
                value='Value_score'
            ),
            dcc.RadioItems(
                id='crossfilter-yaxis-type',
                options=[{'label': i, 'value': i} for i in ['linear', 'log']],
                value='linear',
                labelStyle={'display': 'inline-block'}
            ),
            html.Br(),
            html.A('What do these quantities mean?',href='/explainer',
                      target="_blank"),            
            ], className='four columns' ),

            html.Br(),
            html.Div(children=[
                html.Details([
                html.Summary("What does this plot mean?",
                              style={'color': 'grey', 'font-size' : '15px'}
                ),
                html.Br(),
                html.Div([
                    html.P("In this plot each colored circle represents a school listed in the \
                           table above. Hover on a circle to see which school it represents.\
                           The selected school has a black circle around it. You can change the x \
                           and the y axes from the dropdown lists to the right.")
                ],#style={'background-color': cc1}
                style=round1,
                ),

                ])                
            ],className= "twelve columns"),
        

    ], className='container'),    
    
    
    #
    #Institute description starts here...
    #
    #---------------------------------
    #experimental section
    #            
    html.Div(id='expt_section',children=[    
    ]),
    #---------------------------------
    #contact form + social share embed
    #        
    html.Div(id='contact_us',children=[
            html.H6("Say hello to CollegeScoreCard.io",style={'text-align':'center'}),
            html.Iframe(src="/contact_us",
            style={'border': 'none', 'width': '100%', 'height': 540}
           ),
            
            html.Iframe(src="/social/",
            className="four columns",
            style={'border': 'none', 'width': '100%', 'height': 150, 'text-align':'center'}
           ),
            #html.I(className="fa fa-camera-retro fa-lg"),
            #html.Hr(),  
           html.Br(),
           html.Br(),
           html.Hr(),
           html.Div(children=[
               html.H4("Other important official links"),
               html.Div(children=[
                html.Button(children=[html.A("Fin Aid",href="https://studentaid.ed.gov/sa/types#aid-from-the-federal-government",target="_blank")],className="btn btn-md btn-default"),
                html.Button(children=[html.A("Calculate Aid",href="https://fafsa.ed.gov/FAFSA/app/f4cForm?execution=e1s1",target="_blank")],className="btn btn-md btn-default"),
                html.Button(children=[html.A("Start FAFSA app",href="https://fafsa.ed.gov/",target="_blank")],className="btn btn-md btn-default"),
                html.Button(children=[html.A("GI Bill Benefits",href="https://www.vets.gov/gi-bill-comparison-tool",target="_blank")],className="btn btn-md btn-default"),                   
                html.Button(children=[html.A("CFPB",href="https://www.consumerfinance.gov/paying-for-college/",target="_blank")],className="btn btn-md btn-default"),                   
               ],className="row"),
               html.Br(),
               html.Br(),
               html.Hr(),   
               html.P("WARNING: this website is still under construction, and use the information on this website at your own risk."),
               html.Div(children=[
                   html.Span("The website codebase is open-source and is available "),
                   html.A("here",href="https://github.com/royanin/collegescorecard",target="_blank"),
                   html.Span(" and "),
                   html.A("here",href="https://github.com/royanin/collegescorecard_db",target="_blank"),  
               ]),
           ],className="twelve columns",style={'text-align':'center'})   
         
    ],className='container'),  

], className='twelve columns')

#################################################################################
#Layout ends above; callbacks start below
#################################################################################

#show_filter_button
@app.callback(
Output('show_filter_button', 'style'),
[Input('button-submit-filter', 'n_clicks'),
 Input('button-hide-filter','n_clicks'),
Input('button-toggle-filter', 'n_clicks')]
)
def show_hide_filters(nclicks_submit, nclicks_hide, nclicks_filter):
    if nclicks_filter == None:
        filter_show = 0
    else:
        filter_show = nclicks_filter
        
    if nclicks_hide == None:
        filter_hide = 0
    else:
        filter_hide = nclicks_hide
        
    if nclicks_submit == None:
        filter_submit = 0
    else:
        filter_submit = nclicks_submit
        
    
    if (filter_show + filter_hide + filter_submit)%2 == 0:    
        return {'display' : 'block'}
    else:
        return {'display' : 'none'}     

#callback_5: dump all the filter choices:
@app.callback(
Output('show_all_filters', 'style'),
[Input('button-submit-filter', 'n_clicks'),
 Input('button-hide-filter','n_clicks'),
Input('button-toggle-filter', 'n_clicks')]
)
def show_hide_filters(nclicks_submit, nclicks_hide, nclicks_filter):

    if nclicks_filter == None:
        filter_show = 0
    else:
        filter_show = nclicks_filter
        
    if nclicks_hide == None:
        filter_hide = 0
    else:
        filter_hide = nclicks_hide
        
    if nclicks_submit == None:
        filter_submit = 0
    else:
        filter_submit = nclicks_submit
          
    
    if (filter_show + filter_hide + filter_submit)%2 == 0:    
        return {'display' : 'none'}
    else:
        return {'display' : 'block'}  

#Callback_6: submit all filter choices
@app.callback(Output('filter-output', 'children'),
              [Input('button-submit-filter', 'n_clicks')],
            state=[
                State('filter_sc_type','value'),
                State('filter_sc_control','value'),                
                State('filter_acad_type','value'),
                State('adm_range','value'),
                State('sat_math','value'),
                State('sat_verbal','value'),
                State('act_math','value'),
                State('act_verbal','value'),                
                State('filter_loc_type','value'),
                #State('loc_1','children'),
                State('loc_dist_range','value'),
                State('loc_dist_center','value'),
                State('loc_state','value'),
                State('loc_region','value'),
            ])
def filter_df(n_clicks,sc_type, sc_control, acad_type, adm_range, sat_math, sat_verbal, act_math, act_verbal,
              loc_type,loc_dist_range,loc_dist_center,loc_state,loc_region):
    
    filter_dict = []
    sql_filter_dict = []
    lat_in = None
    long_in = None

    #school-type related filters
    if sc_type == 'two_' :
        filter_dict.append('PREDDEG == 2')
        sql_filter_dict.append("school_details.PREDDEG=2")
    elif sc_type == 'four_' :
        #filter_dict['PREDDEG'] = ">2"
        filter_dict.append('PREDDEG > 2')
        sql_filter_dict.append("school_details.PREDDEG>2")
        
    if len(sc_control) == 2:
        for i in range (1,4):
            if i not in sc_control:
                filter_dict.append('CONTROL != {}'.format(i))
                sql_filter_dict.append("school_details.CONTROL<>{}".format(i))                
    
    elif len(sc_control) == 1:
        for i in range (1,4):
            if i in sc_control:
                filter_dict.append('CONTROL == {}'.format(i))
                sql_filter_dict.append("school_details.CONTROL={}".format(i))                

    #academics related filters                  
    if acad_type == 'adm':
        filter_dict.append('ADJ_ADM_RATE >= {}'.format(adm_range[0]))
        filter_dict.append('ADJ_ADM_RATE <= {}'.format(adm_range[1]))
        sql_filter_dict.append("school_details.ADJ_ADM_RATE BETWEEN {} AND {}".format(adm_range[0],
                                                                                      adm_range[1]))                
        
    elif acad_type == 'open':
        filter_dict.append('ADJ_ADM_RATE == 1.0')
        sql_filter_dict.append("school_details.ADJ_ADM_RATE=1.0")
        
    elif acad_type == 'sat':
        filter_dict.append('SATMTMID >= {}'.format(0.9*sat_math))
        filter_dict.append('SATMTMID <= {}'.format(1.1*sat_math))        
        filter_dict.append('SATVRMID >= {}'.format(0.9*sat_verbal))
        filter_dict.append('SATVRMID <= {}'.format(1.1*sat_verbal))
        sql_filter_dict.append("school_details.SATMTMID BETWEEN {} AND {}".format(0.9*sat_math,
                                                                                      1.1*sat_math))
        sql_filter_dict.append("school_details.SATVRMID BETWEEN {} AND {}".format(0.9*sat_verbal,
                                                                                      1.1*sat_verbal))      

                
    elif acad_type == 'act':
        filter_dict.append('ACTMTMID >= {}'.format(0.9*act_math))
        filter_dict.append('ACTMTMID <= {}'.format(1.1*act_math))        
        filter_dict.append('ACTVRMID >= {}'.format(0.9*act_verbal))
        filter_dict.append('ACTVRMID <= {}'.format(1.1*act_verbal))        
        sql_filter_dict.append("school_details.ACTMTMID BETWEEN {} AND {}".format(0.9*act_math,
                                                                                      1.1*act_math))
        sql_filter_dict.append("school_details.ACTVRMID BETWEEN {} AND {}".format(0.9*act_verbal,
                                                                                      1.1*act_verbal))
        
        
    #location related filters:
    if loc_type == 'state':
        filter_dict.append('STABBR == "{}"'.format(loc_state))
        sql_filter_dict.append("school_details.STABBR='{}'".format(loc_state))                        
    elif loc_type == 'region':
        filter_dict.append('REGION == {}'.format(loc_region))
        sql_filter_dict.append("school_details.REGION={}".format(loc_region))        
    elif loc_type == 'dist':

        try:
            if (re.match("^[0-9.]*$",str(loc_dist_range))) and (re.match("^[0-9]*$",str(loc_dist_center))):
                if len(loc_dist_center) == 5:
                    try:
                        #lat_in,long_in = db_shelve[str(loc_dist_center)]
                        u = db.session.query(Zip_to_latlong).filter_by(zip_code=str(loc_dist_center)).first()
                        lat_in = u.lat_
                        long_in = u.long_
                    except:
                        print "Zipcode not found"
                else:
                    print "Bad character in the input"
            else:
                print "Bad character in the input"
            
            #db_shelve.close()

        except KeyError:
            print "Unfortunately the zipcode {} is not in the database".format
            #db_shelve.close()
        
    """
    This could actually be the first filter, if it's reasonably fast enough
    However, we may need a sqlite database for doing this efficiently. There's
    no point loading a 2.3MB file in dictionary which is used only occasionally at best
    """ 
                
    #Construct the query string:
    filter_string = '('+") & (".join(filter_dict[:])+')'


    print 'Constructing sql query:'
    sql_query_string = ' '+' AND '.join(sql_filter_dict[:])
    
    sql_query = "SELECT * FROM school_details where{}".format(sql_query_string)
    filtered_df = pd.read_sql(sql_query,con=db.engine)
    if (lat_in) and (long_in):
        lat_long_mat = filtered_df[['LATITUDE','LONGITUDE']].as_matrix()
        filtered_df['DISTANCE'] = haversine_np(lat_in, long_in,
                                              lat_long_mat[:,0],lat_long_mat[:,1])

        filtered_df = filtered_df[filtered_df['DISTANCE']<float(loc_dist_range)].head(MAX_RESULTS).copy()
    else:
        filtered_df = filtered_df.head(MAX_RESULTS).copy()
    
    #And finally dump the filtered dataframe into a json.
    #BUG: This changes the dtype of ZIP5 from string to integer
    datasets = {
         'df_sel': filtered_df.to_json(orient='split', date_format='iso')
    }

    return json.dumps(datasets)

#Get wiki_social info


#callback_collapse:
#show_filter_selection
@app.callback(
Output('show_filter_selection', 'children'),
[Input('filter-output', 'children')])
def show_table_desc(json_dataset):
    if json_dataset is None:

        return html.Div("Showing {} randomly selected colleges".format(35),
                       style={'text-align':'center'})
    else:
        datasets = json.loads(json_dataset)        
        df_sel = pd.read_json(datasets['df_sel'], orient='split')
        num_rows = df_sel.shape[0]
        return html.Div("Showing {} colleges selected based on your filters".format(num_rows),
                       style={'text-align':'center','color':cc7})  

    
#callback_3: Update panel 3
for i in range (1,5):
    @app.callback(
    Output('loc_{}'.format(i), 'style'),
    [Input('filter_loc_type', 'value')
    ])
    def loc_i(loc_type_val,i=i):
        if loc_type_val == loc_type_dict[i]:
            return {'display' : 'block'}
        else:  
            return {'display' : 'none'}   

#callback_2: Update panel 2
for j in range (1,6):
    @app.callback(
    Output('acad_{}'.format(j), 'style'),
    [Input('filter_acad_type', 'value')
    ])
    def acad_j(acad_type_val,j=j):
        if acad_type_val == acad_type_dict[j]:
            return {'display' : 'block'}
        else:  
            return {'display' : 'none'}



#Callback_1: Filter panel 1:
@app.callback(
Output('filter2', 'children'),
[Input('filter_sc_type', 'value'),
])
def update_filter2(inst_type): 
    return  html.Div([
            html.H4("You chose "+inst_type),
            dcc.Dropdown(
                id='filter3', 
                options=[
                    {'label': '4-year inst.', 'value': 'four_'},
                    {'label': '2-year inst.', 'value': 'two_'},
                    {'label': 'Show both', 'value': 'both_'}
                ],                
             multi=False,
             placeholder='School type:',
            ),        

        ],
    )


#Callback 1: Get the tab value, filter the dataframe and send it to datatable
@app.callback(
Output('datatable-ranking', 'rows'),
[Input('filter-output', 'children'),
])
def update_datatable(json_dataset):
    if json_dataset is None:
        df_sel = set23_rand
    else:    
        datasets = json.loads(json_dataset)
        df_sel = pd.read_json(datasets['df_sel'], orient='split')

    row_list =  df_sel.to_dict('records')
    qnt_list = table_col_dict.keys()

    for item in row_list:
        for qnt in qnt_list:
            #item['Care score'] = item.pop('CARE_INDEX')
            item[table_col_dict[qnt]] = item.pop(qnt)

    return row_list

#Callback 1a: Choose a selection of columns to show on the table (from a dropdown list?)
@app.callback(
Output('datatable-ranking', 'columns'),
[Input('col_select_checklist', 'values'),
])
def update_datatable(table_col_vals):
    return (table_col_vals)

#Callback 2: Top-level breakdown -- donut plots
@app.callback(
Output('inst_dropdown', 'options'),
[Input('filter-output', 'children'),
])
def update_dropdwnlist(json_dataset):
    if json_dataset is None:
        df_sel = set23_rand
    else:
        datasets = json.loads(json_dataset)
        df_sel = pd.read_json(datasets['df_sel'], orient='split')
    
    return [ {'label': i, 'value': j} for (i,j) in zip(df_sel['INSTNM'].tolist(),df_sel['uid'].tolist()) ]


@app.callback(
Output('inst_dropdown', 'value'),
[Input('filter-output', 'children'),
])
def update_dropdwnlistvalue(json_dataset):
    if json_dataset is None:
        df_sel = set23_rand
    else:
        datasets = json.loads(json_dataset)
        df_sel = pd.read_json(datasets['df_sel'], orient='split')
    return df_sel.iloc[0]['uid']



#callback2a: ClickData to dump1
@app.callback(
Output('table_desc', 'children'),
[Input('filter-output', 'children')])
def show_table_desc(json_dataset):

    if json_dataset is None:
        return html.Div([
            html.P("Showing {} randomly selected colleges; filters applied: None".format(30)),
        ],          style={'text-align':'center'})
    else:
        datasets = json.loads(json_dataset)        
        df_sel = pd.read_json(datasets['df_sel'], orient='split')
        num_rows = df_sel.shape[0]
        return html.Div("Showing {} colleges selected based on your filters".format(num_rows),
                       style={'text-align':'center','color':cc7})     
    

#callback3: ClickData to dump1
@app.callback(
Output('dump1', 'children'),
[Input('inst_dropdown', 'value'),
Input('filter-output', 'children'),
])
def dfRowFromDropdown(dd_value,json_dataset):

    if json_dataset is None:
        df_sel = set23_rand
    else:
        datasets = json.loads(json_dataset)        
        df_sel = pd.read_json(datasets['df_sel'], orient='split', dtype={'ZIP5': np.string_,
                                                        'OPEID':np.string_,
                                                        'OPEID6':np.string_})
    uid = dd_value

    sel_inst = json.dumps(df_sel.loc[df_sel['uid']==uid].reset_index().to_dict('index')[0])   

    if sel_inst is None:
        sel_inst = json.dumps(df_sel.iloc[0].reset_index().to_dict('index')[0])

    return json.dumps(sel_inst)


#crossfilter-scatter-title        
@app.callback(
    Output('crossfilter-scatter-title', 'children'),
    [Input('crossfilter-xaxis-column', 'value'),
    Input('crossfilter-yaxis-column', 'value'),
    Input('dump1', 'children')
    ])
def update_cf_title(xaxis_column_name, yaxis_column_name,inst1):
    sel_inst = json.loads(json.loads(inst1))
    
    return html.Div([
        html.Br(),
        html.H5("How does "+sel_inst['INSTNM']+" compare with other schools on the list?",style={'text-align': 'center'}
               ),
        html.Br(),
    ],className="row")        
        
#crossfilter-numbers
@app.callback(
    Output('crossfilter-numbers', 'children'),
    [Input('crossfilter-xaxis-column', 'value'),
    Input('crossfilter-yaxis-column', 'value'),
    Input('dump1', 'children')
    ])
def update_cf_numbers(xaxis_column_name, yaxis_column_name,inst1):
    sel_inst = json.loads(json.loads(inst1))
    return html.Div([
        html.Div([   
        #html.Br(),            
        html.Div([html.B(sel_inst['INSTNM'])
                 ],style={'text-align': 'center'}),
        #html.Hr(),
        #html.Div([            
            html.Div([
                html.Div([
                    html.P(table_col_dict[xaxis_column_name],style={'text-align': 'center'},className="six columns"),                
                    html.P(table_col_dict[yaxis_column_name],style={'text-align': 'center'},className="six columns"),
                ],className="row"),
                
                html.Div([        
                    html.P(str(sel_inst[xaxis_column_name]),className="six columns",
                       style={'color': cc7, 'font-size' : '20px',
                                 'text-align':'center',
                                #'margin-top': '5px', 'margin-bottom': '5px'
                             }                       
                      ),
                    html.P(str(sel_inst[yaxis_column_name]),className="six columns",
                       style={'color': cc7, 'font-size' : '20px',
                                 'text-align':'center',
                             }                       
                      ),
                    
                ],className="row"),                  
        ],className="row"),
        ],className="round1"),        
    ],className="twelve columns")

@app.callback(
    Output('crossfilter-indicator-scatter', 'figure'),
    [Input('crossfilter-xaxis-column', 'value'),
    Input('crossfilter-yaxis-column', 'value'),
    Input('crossfilter-xaxis-type', 'value'),
    Input('crossfilter-yaxis-type', 'value'),
    Input('filter-output', 'children'),
    Input('dump1', 'children')
    ])
def update_graph(xaxis_column_name, yaxis_column_name,xaxis_type, yaxis_type,json_dataset,inst1):
    return update_graph_make_plot(xaxis_column_name, yaxis_column_name,xaxis_type, yaxis_type,
                                  json_dataset,inst1)
     


#pct_satisfaction
 

@app.callback(
Output('expt_section', 'children'),    
[Input('dump1', 'children'),
])    
def show_inst_details(inst1):
    
    sel_inst = json.loads(json.loads(inst1))
    uid = sel_inst['uid']
    sch = db.session.query(School_details).filter_by(uid=uid).first()
    nat_mean = db.session.query(Nat_avg).filter_by(CCBASIC=sch.CCBASIC).first() 
    wiki_social = db.session.query(Wiki_summary).filter_by(uid=sel_inst['uid']).first()  
    
    #school_info:
    #quick_facts_div = create_school_overview(sel_inst)
    
    #pop_sub:
    xlabels,ylabels = order_pop_subs(sel_inst['POP_SUBS'])
    param = {'xlabels':xlabels,'ylabels':ylabels}
    json_param = json.dumps(param)
    encoded_json_param = urllib.quote_plus(json_param)
    

    #pct dict plot
    symbol_dict = make_pct_satisfac_dict(sch,nat_mean)
    json_pct_dict = json.dumps(symbol_dict)
    encoded_json_pct_dict = urllib.quote_plus(json_pct_dict)
    
    #facebook:
    if wiki_social.FB_HANDL != None:
        inst_fb = wiki_social.FB_HANDL
    else:
        inst_fb = ''
        
    return   html.Div([
                html.Div([        
                    html.Br(),

                    html.Div(#id='quick_facts'
                        create_school_overview(sel_inst)
                    )]#,style={'text-align': 'center'}
                    , className='container'),

                #---------------------------------
                #Subj bar chart
                #
                html.Div([        
                    html.Div([
                        html.Div(#id='subj_bar',
                            html.Div([
                                html.Iframe(src='/popsub/{}'.format(encoded_json_param),
                                           style={'border': 'none', 'width': '95%', 'height': 450}
                                           ),

                            ])
                            #dcc.Graph(id='subj_bar'),        
                                ),
                    ], className='six columns'),            
                    html.Div(#id='summary_wikipedia',
                        children = [html.Div([
                            html.Iframe(src="/wiki_summary/"+str(sel_inst['uid']),
                                       style={'border': 'none', 'width': '95%', 'height': 415}
                                       ),

                        ])],
                             className='six columns'),                        
                ], className='container'),
                #---------------------------------
                #Percentile satisfaction chart and numbers at a glance
                #
                html.Div([ 
                    html.Div([
                        html.H6("Numbers at a glance"), 
                    ], className='row',style={'text-align': 'center'}),
                    html.Div([        
                    html.Div([
                        html.Div(#id='pct_satisfaction',
                            html.Div([
                                html.Iframe(src='/pct/{}'.format(encoded_json_pct_dict),
                                           style={'border': 'none', 'width': '95%', 'height': 750}
                                           ),

                            ])
                            #dcc.Graph(id='pct_satisfaction'),        
                                ),          
                    ], className='five columns'),            
                    html.Div([
                        html.Div(#id='numbers_glance'
                            html.Div([
                                html.Br(),
                                html.Iframe(src="/numbers/"+str(sel_inst['uid']), 
                                            #use uid
                                           style={'border': 'none', 'width': '100%', 'height': 725}
                                           ),

                            ])
                        ),
                    ], className='seven columns'),  
                    ], className='row'),
                    html.Div([
                        html.Div(children=[
                            html.Details([
                            html.Summary("What does this plot mean?",
                                          style={'color': 'grey', 'font-size' : '15px'}
                            ),
                            html.Br(),
                            html.Div([
                                html.P("In this plot we show the available/calculated quantities according to their percentile rank. The table to the right explains what each of them means. We compare these quantities among colleges in the same Carnegie class.")
                            ],#style={'background-color': cc1}
                            style=round1,
                            ),
                            ])                
                        ],className= "twelve columns"),        
                    ], className='row')            
                ], className='container'),    
        
                html.Div([
                    html.Div(id='social_yt1',
                             children=yt_output(sel_inst['INSTNM'])
                            ),
                ],style={'text-align': 'center'}, className='container'),
                html.Br(),
                #---------------------------------
                #twitter and facebook embed
                html.Div([
                    html.H5('On other social media...',style={'text-align':'center'}),
                    #---------------------------------
                    #twitter embed     
                        html.Div(id='social_tw1',
                                 children=tw_output(wiki_social.TW_HANDL)                                 
                                ),
                    html.Br(),
                    #---------------------------------
                    #facebook embed     
                        html.Div(id='social_fb1',
                                 children=fb_output(inst_fb)
                                ),
                ], className='container'),
            ]),



