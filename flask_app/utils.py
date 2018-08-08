import numpy as np
import pandas as pd
import ast
from operator import itemgetter
from config import subj_dict


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
