import numpy as np
import pandas as pd
import ast, random
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
