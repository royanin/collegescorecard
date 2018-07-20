import pandas as pd
import numpy as np

set23_rand = pd.read_csv('data/set_234_rand.csv', dtype={'OPEID': np.string_ ,
                            'OPEID6': np.string_ ,
                            'ZIP5': np.string_ })

MAX_RESULTS = 50

available_indicators = ['VALUE_INDEX','CARE_INDEX','fin_ADJ_AVGFACSAL','fin_ADJ_INEXPFTE']

col_list = ['87,88,187','18,137,167','163,203,56','247,105,76',
           '46, 74, 98','183, 107, 163','192, 171, 142','158, 70, 36',
           '0, 155, 119']
#col_list = ['46, 74, 98','180, 183, 186','192, 171, 142','240, 237, 229' ]
col_list2 = ['247, 202, 201','247, 120, 107','145, 168, 208','3, 79, 132',
            '152, 221, 222','136, 176, 75','247, 202, 201','146, 168, 209',
            '181, 101, 167','0, 155, 119','221, 65, 36','214, 80, 118',
            '68, 184, 172','239, 192, 80','91, 94, 166','155, 35, 53',
            '223, 207, 190','85, 180, 176','225, 93, 68','127, 205, 205',
            '188, 36, 60','195, 68, 122','152, 180, 212',
            '76, 106, 146','146, 182, 213','131, 132, 135','185, 58, 50',
            '175, 148, 131','173, 93, 93','0, 110, 81','216, 174, 71',
            '158, 70, 36','183, 107, 163']
tr_dict = ['1.0','0.6','0.2']


subj_dict = {
        'PCIP01' : ('Agriculture, Agriculture Operations, and Related Sciences','247, 202, 201'),
        'PCIP03' : ('Natural Resources and Conservation','247, 120, 107'),
        'PCIP04' : ('Architecture and Related Services','145, 168, 208'),
        'PCIP05' : ('Area, Ethnic, Cultural, Gender, and Group Studies','3, 79, 132'),
        'PCIP09' : ('Communication, Journalism, and Related Programs','152, 221, 222'),
        'PCIP10' : ('Communications Technologies/Technicians and Support Services','136, 176, 75'),
        'PCIP11' : ('Computer and Information Sciences and Support Services','247, 202, 201'),
        'PCIP12' : ('Personal and Culinary Services','146, 168, 209'),
        'PCIP13' : ('Education','181, 101, 167'),
        'PCIP14' : ('Engineering','0, 155, 119'),
        'PCIP15' : ('Engineering Technologies and Engineering-Related Fields','221, 65, 36'),
        'PCIP16' : ('Foreign Languages, Literatures, and Linguistics','214, 80, 118'),
        'PCIP19' : ('Family and Consumer Sciences/Human Sciences','68, 184, 172'),
        'PCIP22' : ('Legal Professions and Studies','239, 192, 80'),
        'PCIP23' : ('English Language and Literature/Letters','91, 94, 166'),
        'PCIP24' : ('Liberal Arts and Sciences, General Studies and Humanities','155, 35, 53'),
        'PCIP25' : ('Library Science','223, 207, 190'),
        'PCIP26' : ('Biological and Biomedical Sciences','85, 180, 176'),
        'PCIP27' : ('Mathematics and Statistics','225, 93, 68'),
        'PCIP29' : ('Military Technologies and Applied Sciences','127, 205, 205'),
        'PCIP30' : ('Multi/Interdisciplinary Studies','188, 36, 60'),
        'PCIP31' : ('Parks, Recreation, Leisure, and Fitness Studies','195, 68, 122'),
        'PCIP38' : ('Philosophy and Religious Studies','152, 180, 212'),
        'PCIP39' : ('Theology and Religious Vocations','76, 106, 146'),
        'PCIP40' : ('Physical Sciences','146, 182, 213'),
        'PCIP41' : ('Science Technologies/Technicians','131, 132, 135'),
        'PCIP42' : ('Psychology','185, 58, 50'),
        'PCIP43' : ('Homeland Security, Law Enforcement, Firefighting and Related Protective Services','175, 148, 131'),
        'PCIP44' : ('Public Administration and Social Service Professions','173, 93, 93'),
        'PCIP45' : ('Social Sciences','0, 110, 81'),
        'PCIP46' : ('Construction Trades','216, 174, 71'),
        'PCIP47' : ('Mechanic and Repair Technologies/Technicians','158, 70, 36'),
        'PCIP48' : ('Precision Production','183, 107, 163'),
        'PCIP49' : ('Transportation and Materials Moving','46, 74, 98'),
        'PCIP50' : ('Visual and Performing Arts','180, 183, 186'),
        'PCIP51' : ('Health Professions and Related Programs','192, 171, 142'),
        'PCIP52' : ('Business, Management, Marketing, and Related Support Services','240, 237, 229'),
        'PCIP54' : ('History','121, 199, 83'),
        'other'  : ('Other subjects','250, 224, 60' ),
    
}

state_list = ['WA', 'DE', 'DC', 'WI', 'WV', 'HI', 'FL', 'FM', 'WY', 'NH', 'NJ', 'NM', 'TX', 'LA', 'NC', 'ND', 'NE', 'TN', 'NY', 'PA', 'CA', 'NV', 'VA', 'GU', 'CO', 'PW', 'VI', 'AK', 'AL', 'AS', 'AR', 'VT', 'IL', 'GA', 'IN', 'IA', 'OK', 'AZ', 'ID', 'CT', 'ME', 'MD', 'MA', 'OH', 'UT', 'MO', 'MN', 'MI', 'MH', 'RI', 'KS', 'MT', 'MP', 'MS', 'PR', 'SC', 'KY', 'OR', 'SD']

region_dict = {
    'U.S. Service Schools' : 0,
    'New England (CT, ME, MA, NH, RI, VT)' : 1,
    'Mid East (DE, DC, MD, NJ, NY, PA)' : 2,
    'Great Lakes (IL, IN, MI, OH, WI)' : 3,
    'Plains (IA, KS, MN, MO, NE, ND, SD)' : 4,
    'Southeast (AL, AR, FL, GA, KY, LA, MS, NC, SC, TN, VA, WV)' : 5,
    'Southwest (AZ, NM, OK, TX)' : 6,
    'Rocky Mountains (CO, ID, MT, UT, WY)' : 7,
    'Far West (AK, CA, HI, NV, OR, WA)' : 8,
    'Outlying Areas (AS, FM, GU, MH, MP, PR, PW, VI)' : 9,
}

def dist_cal(zip_in,miles,df_in):
    #Step1: Convert zip_in into lat and long
    #lat_in = zip_dict[zip_in][0]
    #long_in = zip_dict[zip_in][1]
    
    
    
    print zip_in, miles
    
loc_type_dict = {
    1:'ignore',
    2:'dist',
    3:'state',
    4:'region',
}

acad_type_dict = {
    1:'ignore',
    2:'open',
    3:'adm',
    4:'act',
    5:'sat'
}


table_col_list = ['INSTNM','OPEID', 'OPEID6', 'Value_score', 'Care_score', 'r_fin_MN_EARN_WNE_P6', 'r_fin_DEBT_MDN', 'r_fin_C150_4_COMB', 'r_fin_COSTT4_COMB', 'r_fin_WDRAW_ORIG_YR6_RT', 'r_fin_NPT4_COMB', 'r_fin_PCTPELL', 'r_fin_ADJ_AVGFACSAL', 'r_fin_PFTFTUG1_EF', 'r_fin_PFTFAC', 'r_fin_COMB_RET_RATE', 'r_fin_ADJ_INEXPFTE']


table_col_dict = {'INSTNM':'School',
                  'OPEID':'OPEID',
                  'ZIP5' : 'Zip',                  
                  'OPEID6':'OPEID6',
                  #'VALUE_INDEX':'Value index',
                  #'CARE_INDEX':'Care index',
                  'Value_score':'Value score',
                  'Care_score':'Care score',                  
                  'r_fin_MN_EARN_WNE_P6':'Mean earning USD',
                  'r_fin_DEBT_MDN':'Median debt USD',
                  'r_fin_C150_4_COMB':'Completion %',
                  'r_fin_COSTT4_COMB':'Avg. cost USD',
                  'r_fin_WDRAW_ORIG_YR6_RT':'Withdrawal %',
                  'r_fin_NPT4_COMB':'Net Price USD',
                  'r_fin_PCTPELL':'Pell students %',
                  'r_fin_ADJ_AVGFACSAL':'Avg. faculty salary USD',
                  'r_fin_PFTFTUG1_EF':'% FT students',
                  'r_fin_PFTFAC':'% FT faculty',
                  'r_fin_COMB_RET_RATE':'Returning student %',
                  'r_fin_ADJ_INEXPFTE':'Expenses per student USD'}



table_col_present_dict = {
    'Mean earning USD':'MN_EARN_WNE_P6_PRESENT',
    'Median debt USD':'DEBT_MDN_PRESENT',
    'Completion %':'C150_4_COMB_PRESENT',
    'Avg. cost USD':'COSTT4_COMB_PRESENT',
    'Withdrawal %':'WDRAW_ORIG_YR6_RT_PRESENT',
    'Net Price USD':'NPT4_COMB_PRESENT',
    'Pell students %':'PCTPELL_PRESENT',
    'Avg. faculty salary USD':'ADJ_AVGFACSAL_PRESENT',
    '% FT students':'PFTFTUG1_EF_PRESENT',
    '% FT faculty':'PFTFAC_PRESENT',
    'Expenses per student USD':'ADJ_INEXPFTE_PRESENT'
}

contact_options_dict = {
    'data_ana_viz_enthu': 'Data analysis and visualization enthusiast',
    'career_counselor':'Career counselor',
    'student':'Student -- shopping for college',
    'parent':'Parent -- shopping for college',
    'inst_admin':'College/University Admin',
    'gen_feedback':'General website feedback',
    'p_sponsor':'Potential sponsor!',
    'other':'Anything else',    
}

msg_len_max = 500

pct_rank_qnty_dict = {
    'rankp_MN_EARN_WNE_P6':'E',
    'rankp_DEBT_MDN':'D',
    'rankp_C150_4_COMB':'C',
    'rankp_COSTT4_COMB':'$',
    'rankp_WDRAW_ORIG_YR6_RT':'W',
    'rankp_NPT4_COMB':'N',
    'rankp_PCTPELL':'P',
    #'rankp_ADJ_AVGFACSAL':'',
    'rankp_ADJ_INEXPFTE':'Ex',
    'rankp_PFTFAC':'FT',
    'rankp_COMB_RET_RATE':'R'
}
