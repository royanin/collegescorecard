from flask_app import flask_app,db
from datetime import datetime

enable_search = True
import flask_whooshalchemy as whooshalchemy

class Message(db.Model):
    #Note the __bind_key__ below --> as this table is going to a different database
    __bind_key__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(500), index=True, nullable=False)
    email = db.Column(db.String(100), index=True, nullable=False)
    sender_type = db.Column(db.String(100), nullable=False)    
    subscribed =  db.Column(db.Boolean)    
    timestamp =  db.Column(db.DateTime)
    
    def __init__(self,body,email,sender_type,subscribed):
        self.body = body
        self.email = email        
        self.sender_type = sender_type
        self.subscribed = subscribed    
        self.timestamp = datetime.utcnow()


class Zip_to_latlong(db.Model):

    __tablename__ = 'zip_to_latlong'

    id = db.Column(db.Integer, index=True, primary_key=True)
    zip_code = db.Column(db.String(5), index=True, unique=True)
    lat_ = db.Column(db.Float(10))
    long_ = db.Column(db.Float(10))
    

    def __init__(self,zip_code, lat_,long_):
        self.zip_code = zip_code
        self.lat_ = lat_
        self.long_ = long_


class Wiki_summary(db.Model):

    __tablename__ = 'wiki_social'
    __searchable__ = ['wiki_summary']

    id = db.Column(db.Integer, index=True, primary_key=True)
    uid = db.Column(db.String(150), index=True, unique=True, nullable=False)
    inst_nm = db.Column(db.String(100))
    UNITID = db.Column(db.String(10)) 
    OPEID = db.Column(db.String(10))
    wiki_summary = db.Column(db.String(10000))
    date_extracted = db.Column(db.String(10))
    wiki_url = db.Column(db.String(150))
    FB_HANDL = db.Column(db.String(100))
    TW_HANDL = db.Column(db.String(100))

    

    def __init__(self, uid, inst_nm, UNITID, OPEID, wiki_summary, date_extracted, wiki_url, FB_HANDL, TW_HANDL):
        self.uid = uid
        self.inst_nm = inst_nm
        self.UNITID = UNITID
        self.OPEID = OPEID        
        self.wiki_summary = wiki_summary
        self.date_extracted = date_extracted
        self.wiki_url = wiki_url
        self.FB_HANDL = FB_HANDL
        self.TW_HANDL = TW_HANDL        

class Nat_avg(db.Model):
    
    __tablename__ = 'national_average'
    
    id = db.Column(db.Integer, index=True, primary_key=True)
    CCBASIC = db.Column(db.Integer)
    MN_EARN_WNE_P6 = db.Column(db.Float(5))
    DEBT_MDN = db.Column(db.Float(5))
    C150_4_COMB = db.Column(db.Float(3))
    COSTT4_COMB = db.Column(db.Float(5))
    WDRAW_ORIG_YR6_RT = db.Column(db.Float(3))
    NPT4_COMB = db.Column(db.Float(5))
    PCTPELL = db.Column(db.Float(3))
    RET_FT4_COMB = db.Column(db.Float(3))
    RET_PT4_COMB = db.Column(db.Float(3))
    ADJ_AVGFACSAL = db.Column(db.Float(5))
    ADJ_INEXPFTE = db.Column(db.Float(5))
    PFTFTUG1_EF = db.Column(db.Float(3))
    PFTFAC = db.Column(db.Float(3))
    COMB_RET_RATE = db.Column(db.Float(3))

    def __init__(self,CCBASIC,MN_EARN_WNE_P6,DEBT_MDN,C150_4_COMB,COSTT4_COMB,WDRAW_ORIG_YR6_RT,
                 NPT4_COMB,PCTPELL,RET_FT4_COMB,RET_PT4_COMB,ADJ_AVGFACSAL,ADJ_INEXPFTE,
                 PFTFTUG1_EF,PFTFAC,COMB_RET_RATE):
        self.CCBASIC = CCBASIC
        self.MN_EARN_WNE_P6 = MN_EARN_WNE_P6
        self.DEBT_MDN = DEBT_MDN 
        self.C150_4_COMB = C150_4_COMB
        self.COSTT4_COMB = COSTT4_COMB
        self.WDRAW_ORIG_YR6_RT = WDRAW_ORIG_YR6_RT
        self.NPT4_COMB =  NPT4_COMB
        self.PCTPELL = PCTPELL 
        self.RET_FT4_COMB = RET_FT4_COMB
        self.RET_PT4_COMB = RET_PT4_COMB
        self.ADJ_AVGFACSAL = ADJ_AVGFACSAL
        self.ADJ_INEXPFTE = ADJ_INEXPFTE         
        self.PFTFTUG1_EF = PFTFTUG1_EF
        self.PFTFAC = PFTFAC
        self.COMB_RET_RATE = COMB_RET_RATE
        
class School_details(db.Model):

    __tablename__ = 'school_details'
    __searchable__ = ['INSTNM']
    
    id = db.Column(db.Integer, index=True, primary_key=True)
    uid = db.Column(db.String(150), index=True, unique=True)
    INSTNM = db.Column(db.String(100))
    UNITID = db.Column(db.String(10))
    OPEID = db.Column(db.String(10))
    OPEID6 = db.Column(db.String(10))
    CITY = db.Column(db.String(50))
    STABBR = db.Column(db.String(2))
    ZIP5 = db.Column(db.String(5))
    PREDDEG = db.Column(db.Integer)
    HTTPS_INSTURL = db.Column(db.String(100))
    HTTPS_NPCURL = db.Column(db.String(300))
    HIGHDEG = db.Column(db.Integer)
    CONTROL = db.Column(db.Integer)
    REGION = db.Column(db.Integer)
    LOCALE = db.Column(db.Integer)
    LATITUDE = db.Column(db.Float(10))
    LONGITUDE = db.Column(db.Float(10))
    CCBASIC = db.Column(db.Integer)
    CCUGPROF = db.Column(db.Integer)
    CCSIZSET = db.Column(db.Integer)
    SATVRMID = db.Column(db.Integer)
    SATMTMID = db.Column(db.Integer)
    SATWRMID = db.Column(db.Integer)
    ACTCMMID = db.Column(db.Integer)
    ACTENMID = db.Column(db.Integer)
    ACTMTMID = db.Column(db.Integer)
    ACTWRMID = db.Column(db.Integer)
    SATVR25 = db.Column(db.Integer)
    SATVR75 = db.Column(db.Integer)
    SATMT25 = db.Column(db.Integer)
    SATMT75 = db.Column(db.Integer)
    SATWR25 = db.Column(db.Integer)
    SATWR75 = db.Column(db.Integer)
    ACTCM25 = db.Column(db.Integer)
    ACTCM75 = db.Column(db.Integer)
    ACTEN25 = db.Column(db.Integer)
    ACTEN75 = db.Column(db.Integer)
    ACTMT25 = db.Column(db.Integer)
    ACTMT75 = db.Column(db.Integer)
    ACTWR25 = db.Column(db.Integer)
    ACTWR75 = db.Column(db.Integer)
    POP_SUBS = db.Column(db.String(400))
    UGDS = db.Column(db.Float(5))
    TUITIONFEE_IN = db.Column(db.Float(5))
    TUITIONFEE_OUT = db.Column(db.Float(5))
    ADJ_ADM_RATE = db.Column(db.Float(5))
    OTHER_AFFIL = db.Column(db.String(300))
    REL_AFFIL = db.Column(db.String(100), nullable=True)
    COUNT_MISSING = db.Column(db.Integer)
    VALUE_INDEX = db.Column(db.Float(5))
    CARE_INDEX = db.Column(db.Float(5))
    Value_score = db.Column(db.Float(5))
    Care_score = db.Column(db.Float(5))    
    r_fin_MN_EARN_WNE_P6 = db.Column(db.Float(5))
    r_fin_DEBT_MDN = db.Column(db.Float(5))
    r_fin_C150_4_COMB = db.Column(db.Float(5))
    r_fin_COSTT4_COMB = db.Column(db.Float(5))
    r_fin_WDRAW_ORIG_YR6_RT = db.Column(db.Float(5))
    r_fin_NPT4_COMB = db.Column(db.Float(5))
    r_fin_PCTPELL = db.Column(db.Float(5))
    r_fin_RET_FT4_COMB = db.Column(db.Float(5))
    r_fin_RET_PT4_COMB = db.Column(db.Float(5))
    r_fin_ADJ_AVGFACSAL = db.Column(db.Float(5))
    r_fin_ADJ_INEXPFTE = db.Column(db.Float(5))
    r_fin_PFTFTUG1_EF = db.Column(db.Float(5))
    r_fin_PFTFAC = db.Column(db.Float(5))
    r_fin_COMB_RET_RATE = db.Column(db.Float(5))
    MN_EARN_WNE_P6_PRESENT = db.Column(db.Integer)
    DEBT_MDN_PRESENT = db.Column(db.Float(5))
    C150_4_COMB_PRESENT = db.Column(db.Integer)
    COSTT4_COMB_PRESENT = db.Column(db.Integer)
    WDRAW_ORIG_YR6_RT_PRESENT = db.Column(db.Integer)
    NPT4_COMB_PRESENT = db.Column(db.Integer)
    PCTPELL_PRESENT = db.Column(db.Integer)
    RET_FT4_COMB_PRESENT = db.Column(db.Integer)
    RET_PT4_COMB_PRESENT = db.Column(db.Integer)
    ADJ_AVGFACSAL_PRESENT = db.Column(db.Integer)
    ADJ_INEXPFTE_PRESENT = db.Column(db.Integer)
    PFTFTUG1_EF_PRESENT = db.Column(db.Integer)
    PFTFAC_PRESENT = db.Column(db.Integer)
    fin_COMB_RET_RATE_PRESENT = db.Column(db.Integer)
    rankp_MN_EARN_WNE_P6 = db.Column(db.Float(5))
    rankp_DEBT_MDN = db.Column(db.Float(5))
    rankp_C150_4_COMB = db.Column(db.Float(5))
    rankp_COSTT4_COMB = db.Column(db.Float(5))
    rankp_WDRAW_ORIG_YR6_RT = db.Column(db.Float(5))
    rankp_NPT4_COMB = db.Column(db.Float(5))
    rankp_PCTPELL = db.Column(db.Float(5))
    rankp_ADJ_AVGFACSAL = db.Column(db.Float(5))
    rankp_ADJ_INEXPFTE = db.Column(db.Float(5))
    rankp_PFTFAC = db.Column(db.Float(5))
    rankp_COMB_RET_RATE = db.Column(db.Float(5))
    adm_pct = db.Column(db.Float(3))
    IF_SAT_PRESENT = db.Column(db.Boolean)
    IF_ACT_PRESENT = db.Column(db.Boolean)
    
    
    
    def __init__(self,uid, UNITID, OPEID,OPEID6,INSTNM,CITY,STABBR,ZIP5,PREDDEG,HTTPS_INSTURL,HTTPS_NPCURL,
                 HIGHDEG,CONTROL,REGION,LOCALE,LATITUDE,LONGITUDE,CCBASIC,CCUGPROF,CCSIZSET,SATVRMID,
                 SATMTMID,SATWRMID,ACTCMMID,ACTENMID,ACTMTMID,ACTWRMID,SATVR25, SATVR75, SATMT25, SATMT75, SATWR25, SATWR75, ACTCM25,ACTCM75, ACTEN25,ACTEN75,ACTMT25, ACTMT75,ACTWR25, ACTWR75,POP_SUBS,UGDS,
                 TUITIONFEE_IN,TUITIONFEE_OUT,ADJ_ADM_RATE,OTHER_AFFIL,REL_AFFIL,COUNT_MISSING,
                 VALUE_INDEX,CARE_INDEX,Value_score, Care_score, r_fin_MN_EARN_WNE_P6,r_fin_DEBT_MDN,r_fin_C150_4_COMB,r_fin_COSTT4_COMB,
                 r_fin_WDRAW_ORIG_YR6_RT,r_fin_NPT4_COMB,r_fin_PCTPELL,r_fin_RET_FT4_COMB,r_fin_RET_PT4_COMB,
                 r_fin_ADJ_AVGFACSAL,r_fin_ADJ_INEXPFTE,r_fin_PFTFTUG1_EF,r_fin_PFTFAC,r_fin_COMB_RET_RATE,
                 MN_EARN_WNE_P6_PRESENT,DEBT_MDN_PRESENT,C150_4_COMB_PRESENT,COSTT4_COMB_PRESENT,
                 WDRAW_ORIG_YR6_RT_PRESENT,NPT4_COMB_PRESENT,PCTPELL_PRESENT,RET_FT4_COMB_PRESENT,
                 RET_PT4_COMB_PRESENT,ADJ_AVGFACSAL_PRESENT,ADJ_INEXPFTE_PRESENT,PFTFTUG1_EF_PRESENT,
                 PFTFAC_PRESENT,fin_COMB_RET_RATE_PRESENT,rankp_MN_EARN_WNE_P6,rankp_DEBT_MDN,
                 rankp_C150_4_COMB,rankp_COSTT4_COMB,rankp_WDRAW_ORIG_YR6_RT,rankp_NPT4_COMB,rankp_PCTPELL,
                 rankp_ADJ_AVGFACSAL,rankp_ADJ_INEXPFTE,rankp_PFTFAC,rankp_COMB_RET_RATE,adm_pct,IF_SAT_PRESENT,
                IF_ACT_PRESENT):
        self.uid = uid
        self.UNITID = UNITID
        self.OPEID = OPEID
        self.OPEID6 = OPEID6
        self.INSTNM = INSTNM
        self.CITY = CITY
        self.STABBR = STABBR
        self.ZIP5 = ZIP5
        self.PREDDEG = PREDDEG
        self.HTTPS_INSTURL = HTTPS_INSTURL
        self.HTTPS_NPCURL = HTTPS_NPCURL
        self.HIGHDEG = HIGHDEG
        self.CONTROL = CONTROL
        self.REGION = REGION
        self.LOCALE = LOCALE
        self.LATITUDE = LATITUDE
        self.LONGITUDE = LONGITUDE
        self.CCBASIC = CCBASIC
        self.CCUGPROF = CCUGPROF
        self.CCSIZSET = CCSIZSET
        self.SATVRMID = SATVRMID
        self.SATMTMID = SATMTMID
        self.SATWRMID = SATWRMID
        self.ACTCMMID = ACTCMMID
        self.ACTENMID = ACTENMID
        self.ACTMTMID = ACTMTMID
        self.ACTWRMID = ACTWRMID
        self.SATVR25 = SATVR25 
        self.SATVR75 = SATVR75 
        self.SATMT25 = SATMT25
        self.SATMT75 = SATMT75 
        self.SATWR25 = SATWR25 
        self.SATWR75 = SATWR75 
        self.ACTCM25 = ACTCM25
        self.ACTCM75 = ACTCM75
        self.ACTEN25 = ACTEN25
        self.ACTEN75 = ACTEN75
        self.ACTMT25 = ACTMT25
        self.ACTMT75 = ACTMT75
        self.ACTWR25 = ACTWR25
        self.ACTWR75 = ACTWR75
        self.POP_SUBS = POP_SUBS
        self.UGDS = UGDS
        self.TUITIONFEE_IN = TUITIONFEE_IN
        self.TUITIONFEE_OUT = TUITIONFEE_OUT
        self.ADJ_ADM_RATE = ADJ_ADM_RATE
        self.OTHER_AFFIL = OTHER_AFFIL
        self.REL_AFFIL = REL_AFFIL
        self.COUNT_MISSING = COUNT_MISSING
        self.VALUE_INDEX = VALUE_INDEX
        self.CARE_INDEX = CARE_INDEX
        self.Value_score = Value_score
        self.Care_score = Care_score        
        self.r_fin_MN_EARN_WNE_P6 = r_fin_MN_EARN_WNE_P6
        self.r_fin_DEBT_MDN = r_fin_DEBT_MDN
        self.r_fin_C150_4_COMB = r_fin_C150_4_COMB
        self.r_fin_COSTT4_COMB = r_fin_COSTT4_COMB
        self.r_fin_WDRAW_ORIG_YR6_RT = r_fin_WDRAW_ORIG_YR6_RT
        self.r_fin_NPT4_COMB = r_fin_NPT4_COMB
        self.r_fin_PCTPELL = r_fin_PCTPELL
        self.r_fin_RET_FT4_COMB = r_fin_RET_FT4_COMB
        self.r_fin_RET_PT4_COMB = r_fin_RET_PT4_COMB
        self.r_fin_ADJ_AVGFACSAL = r_fin_ADJ_AVGFACSAL
        self.r_fin_ADJ_INEXPFTE = r_fin_ADJ_INEXPFTE
        self.r_fin_PFTFTUG1_EF = r_fin_PFTFTUG1_EF
        self.r_fin_PFTFAC = r_fin_PFTFAC
        self.r_fin_COMB_RET_RATE = r_fin_COMB_RET_RATE
        self.MN_EARN_WNE_P6_PRESENT = MN_EARN_WNE_P6_PRESENT
        self.DEBT_MDN_PRESENT = DEBT_MDN_PRESENT
        self.C150_4_COMB_PRESENT = C150_4_COMB_PRESENT
        self.COSTT4_COMB_PRESENT = COSTT4_COMB_PRESENT
        self.WDRAW_ORIG_YR6_RT_PRESENT = WDRAW_ORIG_YR6_RT_PRESENT
        self.NPT4_COMB_PRESENT = NPT4_COMB_PRESENT
        self.PCTPELL_PRESENT = PCTPELL_PRESENT
        self.RET_FT4_COMB_PRESENT = RET_FT4_COMB_PRESENT
        self.RET_PT4_COMB_PRESENT = RET_PT4_COMB_PRESENT
        self.ADJ_AVGFACSAL_PRESENT = ADJ_AVGFACSAL_PRESENT
        self.ADJ_INEXPFTE_PRESENT = ADJ_INEXPFTE_PRESENT
        self.PFTFTUG1_EF_PRESENT = PFTFTUG1_EF_PRESENT
        self.PFTFAC_PRESENT = PFTFAC_PRESENT
        self.fin_COMB_RET_RATE_PRESENT = fin_COMB_RET_RATE_PRESENT
        self.rankp_MN_EARN_WNE_P6 = rankp_MN_EARN_WNE_P6
        self.rankp_DEBT_MDN = rankp_DEBT_MDN
        self.rankp_C150_4_COMB = rankp_C150_4_COMB
        self.rankp_COSTT4_COMB = rankp_COSTT4_COMB
        self.rankp_WDRAW_ORIG_YR6_RT = rankp_WDRAW_ORIG_YR6_RT
        self.rankp_NPT4_COMB = rankp_NPT4_COMB
        self.rankp_PCTPELL = rankp_PCTPELL
        self.rankp_ADJ_AVGFACSAL = rankp_ADJ_AVGFACSAL
        self.rankp_ADJ_INEXPFTE = rankp_ADJ_INEXPFTE
        self.rankp_PFTFAC = rankp_PFTFAC
        self.rankp_COMB_RET_RATE = rankp_COMB_RET_RATE  
        self.adm_pct = adm_pct
        self.IF_SAT_PRESENT = IF_SAT_PRESENT
        self.IF_ACT_PRESENT = IF_ACT_PRESENT

if enable_search:
    whooshalchemy.whoosh_index(flask_app, School_details)
    whooshalchemy.whoosh_index(flask_app, Wiki_summary)