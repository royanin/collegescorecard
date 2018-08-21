import numpy as np
import pandas as pd
import ast, random, json, urllib
from operator import itemgetter
from config import subj_dict
from flask_app import db
from sqlalchemy import and_
from models import School_details


def haversine_np(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)

    All args must be of equal length.    

    """
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2

    c = 2 * np.arcsin(np.sqrt(a))
    dist = 3959.87433 * c #c is the angle subtended, 3959.... is the average radius of earth in miles
    return dist


def order_pop_subs(POP_SUBS):

    #pop_subj_pc = ast.literal_eval(sch.POP_SUBS)
    pop_subj_pc = ast.literal_eval(POP_SUBS)
            
    k,v = zip(*pop_subj_pc.iteritems())
    #Make a zipped list of subjects and sort it
    subj_list = [list(x) for x in zip( *sorted(zip(k,v),  key=itemgetter(1), reverse=True) )]

    xlabels = [ subj_dict[i][0] for i in subj_list[0] ]
    ylabels = [ round(100.0*subj_list[1][i],1) for i in range(len(subj_list[0])) ]

    return (xlabels,ylabels)


def suggest_featured_schools(v_score, c_score,uid=None):
           #Find similar featured schools (Care score and value score within +/-3%)
            feat_sch_ =db.session.query(School_details).filter(and_(School_details.Value_score>(v_score-3.0),
                                                        School_details.Value_score<(v_score+3.0),           School_details.Care_score>(c_score-3.0),
                                                        School_details.Care_score<(c_score+3.0))).all()

            #randomize the list of schools so we are not stuck with the same options every time
            feat_sch = random.sample(feat_sch_, len(feat_sch_))                                             
            
            if len(feat_sch) > 1:
                feat_list = []
                for feat in feat_sch:
                    #print feat.INSTNM, feat.uid, feat.Value_score, feat.Care_score
                    if uid != None:                    
                        if feat.uid != uid:
                            feat_list.append([feat.INSTNM, feat.uid, feat.Value_score, feat.Care_score])
                    else:
                        feat_list.append([feat.INSTNM, feat.uid, feat.Value_score, feat.Care_score])                        
                    if len(feat_list) == 6:
                        break
                        
            else:
                feat_list = None
            #print feat_list
            
            return feat_list
        
        
def make_pct_satisfac_dict(sch, nat_mean):
    
    symbol_dict = {}   

    if sch.MN_EARN_WNE_P6_PRESENT != 0:
        symbol_dict['E'] = (sch.r_fin_MN_EARN_WNE_P6, nat_mean.MN_EARN_WNE_P6,'Earning (mean, USD)',
                           sch.rankp_MN_EARN_WNE_P6)
        
    if sch.DEBT_MDN_PRESENT != 0:
        symbol_dict['D']=(sch.r_fin_DEBT_MDN,nat_mean.DEBT_MDN,'Debt (median, USD)',
                         sch.rankp_DEBT_MDN)
        
    if sch.C150_4_COMB_PRESENT != 0:
        symbol_dict['C']=(sch.r_fin_C150_4_COMB,nat_mean.C150_4_COMB,'Completion (%)',
                         sch.rankp_C150_4_COMB)

    if sch.COSTT4_COMB_PRESENT != 0:
        symbol_dict['$']=(sch.r_fin_COSTT4_COMB,nat_mean.COSTT4_COMB,'Sticker price (mean, USD)',
                         sch.rankp_COSTT4_COMB)

    if sch.WDRAW_ORIG_YR6_RT_PRESENT != 0:
        symbol_dict['W']=(sch.r_fin_WDRAW_ORIG_YR6_RT,nat_mean.WDRAW_ORIG_YR6_RT,'Withdrawal (%)',
                         sch.rankp_WDRAW_ORIG_YR6_RT)
        
    if sch.NPT4_COMB_PRESENT != 0:
        symbol_dict['N']=(sch.r_fin_NPT4_COMB,nat_mean.NPT4_COMB,'Net price (mean, USD)',
                         sch.rankp_NPT4_COMB)
        
    if sch.PCTPELL_PRESENT != 0:
        symbol_dict['P']=(sch.r_fin_PCTPELL,nat_mean.PCTPELL,'Pell recipients (%)',
                         sch.rankp_PCTPELL)
        
    if sch.ADJ_INEXPFTE_PRESENT != 0:
        symbol_dict['Ex']=(sch.r_fin_ADJ_INEXPFTE,nat_mean.ADJ_INEXPFTE,'Expenses per student (USD)',
                          sch.rankp_ADJ_INEXPFTE)
        
    if sch.PFTFAC_PRESENT != 0:
        symbol_dict['FT']=(sch.r_fin_PFTFAC,nat_mean.PFTFAC,'Full-time faculty (%)',
                          sch.rankp_PFTFAC)
    
    if (sch.RET_FT4_COMB_PRESENT)*(sch.RET_PT4_COMB_PRESENT)*(sch.PFTFTUG1_EF_PRESENT) != 0:
        symbol_dict['R'] = (sch.r_fin_COMB_RET_RATE,nat_mean.COMB_RET_RATE,'Returning students (%)',
                           sch.rankp_COMB_RET_RATE)    
        
    return symbol_dict
    
    
    
def make_no2_test_dict(no2_flag, sch):
    
    no2_symbol_dict = {}   

    if no2_flag == 'SAT_PRESENT':
        #Verbal
        if sch.SATVRMID != None:
            sat_vr_25 = sch.SATVR25 if (sch.SATVR25 != None) else sch.SATVRMID
            sat_vr_75 = sch.SATVR75 if (sch.SATVR75 != None) else sch.SATVRMID
            no2_symbol_dict['sat_vr'] = (sat_vr_25,
                                         sch.SATVRMID - sat_vr_25,
                                         sat_vr_75 - sch.SATVRMID,
                                         'verbal')            
        #math
        if sch.SATMTMID != None:            
            sat_mt_25 = sch.SATMT25 if (sch.SATMT25 != None) else sch.SATMTMID
            sat_mt_75 = sch.SATMT75 if (sch.SATMT75 != None) else sch.SATMTMID
            no2_symbol_dict['sat_mt'] = (sat_mt_25,
                                         sch.SATMTMID - sat_mt_25,
                                         sat_mt_75 - sch.SATMTMID,
                                         'math')              
        #writing
        if sch.SATWRMID != None:            
            sat_wr_25 = sch.SATWR25 if (sch.SATWR25 != None) else sch.SATWRMID
            sat_wr_75 = sch.SATWR75 if (sch.SATWR75 != None) else sch.SATWRMID
            no2_symbol_dict['sat_wr'] = (sat_wr_25,
                                         sch.SATWRMID - sat_wr_25,
                                         sat_wr_75 - sch.SATWRMID,
                                         'writing')       

        json_param = json.dumps(no2_symbol_dict)
        encoded_json_no2 = urllib.quote_plus(json_param)

        return encoded_json_no2
    
    
    elif no2_flag == 'ACT_PRESENT':
        #cumulative
        if sch.ACTCMMID != None:
            act_cm_25 = sch.ACTCM25 if (sch.ACTCM25 != None) else sch.ACTCMMID
            act_cm_75 = sch.ACTCM75 if (sch.ACTCM75 != None) else sch.ACTCMMID
            no2_symbol_dict['act_cm'] = (act_cm_25,
                                         sch.ACTCMMID -  act_cm_25,
                                         act_cm_75 - sch.ACTCMMID,
                                         'cumulative')            
        #english
        if sch.ACTENMID != None:
            act_en_25 = sch.ACTEN25 if (sch.ACTEN25 != None) else sch.ACTENMID
            act_en_75 = sch.ACTEN75 if (sch.ACTEN75 != None) else sch.ACTENMID
            no2_symbol_dict['act_en'] = (act_en_25,
                                         sch.ACTENMID - act_en_25,
                                         act_en_75 - sch.ACTENMID,
                                         'english')            
        #math
        if sch.ACTMTMID != None:            
            act_mt_25 = sch.ACTMT25 if (sch.ACTMT25 != None) else sch.ACTMTMID
            act_mt_75 = sch.ACTMT75 if (sch.ACTMT75 != None) else sch.ACTMTMID
            no2_symbol_dict['act_mt'] = (act_mt_25,
                                         sch.ACTMTMID - act_mt_25,
                                         act_mt_75 - sch.ACTMTMID,
                                         'math')              
        #writing
        if sch.ACTWRMID != None:            
            act_wr_25 = sch.ACTWR25 if (sch.ACTWR25 != None) else sch.ACTWRMID
            act_wr_75 = sch.ACTWR75 if (sch.ACTWR75 != None) else sch.ACTWRMID
            no2_symbol_dict['act_wr'] = (act_wr_25,
                                         sch.ACTWRMID - act_wr_25,
                                         act_wr_75 - sch.ACTWRMID,
                                         'writing')     

        #return no2_symbol_dict            
        json_param = json.dumps(no2_symbol_dict)
        encoded_json_no2 = urllib.quote_plus(json_param)

        return encoded_json_no2       
    
    
