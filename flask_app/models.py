from flask_app import flask_app,db
from datetime import datetime

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

    __tablename__ = 'wiki_summary'

    id = db.Column(db.Integer, index=True, primary_key=True)
    cs_index = db.Column(db.Integer, index=True, unique=True)
    inst_nm = db.Column(db.String(100))
    wiki_summary = db.Column(db.String(2000))
    date_extracted = db.Column(db.String(10))
    wiki_url = db.Column(db.String(150))
    

    def __init__(self,cs_index, inst_nm, wiki_summary, date_extracted, wiki_url):
        self.cs_index = cs_index
        self.inst_nm = inst_nm
        self.wiki_summary = wiki_summary
        self.date_extracted = date_extracted
        self.wiki_url = wiki_url    


class Email(db.Model):
    __bind_key__ = 'email'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), index=True, nullable=False, unique=True)
    subscribed =  db.Column(db.Boolean)
    timestamp =  db.Column(db.DateTime)
    messages = db.relationship('Message', backref='email', lazy='dynamic', cascade="all, delete-orphan")    
    
    def __init__(self,email,subscribed):
        self.email = email
        self.subscribed = subscribed 
        self.timestamp = datetime.utcnow()
    
class Message(db.Model):
    __bind_key__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(500), index=True, nullable=False)
    timestamp =  db.Column(db.DateTime)
    email_id = db.Column(db.Integer, db.ForeignKey('email.id', ondelete='CASCADE'), nullable=False)    
    
    def __init__(self,body,email_id):
        self.body = body
        self.email_id = email_id
        self.timestamp = datetime.utcnow()    


class Nat_avg(db.Model):
    __tablename__ = 'national_average'
    
    id = db.Column(db.Integer, index=True, primary_key=True)
    CCBASIC = db.Column(db.Integer)
    MN_EARN_WNE_P6 = db.Column(db.Float(5))
    DEBT_MDN = db.Column(db.Float(5))
    C150_4_COMB = db.Column(db.Float(5))
    COSTT4_COMB = db.Column(db.Float(5))
    WDRAW_ORIG_YR6_RT = db.Column(db.Float(5))
    NPT4_COMB = db.Column(db.Float(5))
    PCTPELL = db.Column(db.Float(5))
    RET_FT4_COMB = db.Column(db.Float(5))
    RET_PT4_COMB = db.Column(db.Float(5))
    ADJ_AVGFACSAL = db.Column(db.Float(5))
    ADJ_INEXPFTE = db.Column(db.Float(5))
    PFTFTUG1_EF = db.Column(db.Float(5))
    PFTFAC = db.Column(db.Float(5))
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

    id = db.Column(db.Integer, index=True, primary_key=True)
    cs_index = db.Column(db.Integer, index=True, unique=True)
    INSTNM = db.Column(db.String(100))
    OPEID = db.Column(db.String(10))
    OPEID6 = db.Column(db.String(10))
    CITY = db.Column(db.String(50))
    STABBR = db.Column(db.String(2))
    ZIP5 = db.Column(db.String(5))
    PREDDEG = db.Column(db.Integer)
    HTTPS_INSTURL = db.Column(db.String(100))
    HTTPS_NPCURL = db.Column(db.String(100))
    HIGHDEG = db.Column(db.Integer)
    CONTROL = db.Column(db.Integer)
    REGION = db.Column(db.Integer)
    LOCALE = db.Column(db.Integer)
    LATITUDE = db.Column(db.Float(10))
    LONGITUDE = db.Column(db.Float(10))
    CCBASIC = db.Column(db.Integer)
    CCUGPROF = db.Column(db.Integer)
    CCSIZSET = db.Column(db.Integer)
    SATVRMID = db.Column(db.Float(5))
    SATMTMID = db.Column(db.Float(5))
    SATWRMID = db.Column(db.Float(5))
    ACTCMMID = db.Column(db.Float(5))
    ACTENMID = db.Column(db.Float(5))
    ACTMTMID = db.Column(db.Float(5))
    ACTWRMID = db.Column(db.Float(5))
    POP_SUBS = db.Column(db.String(400))
    FB_HANDL = db.Column(db.String(100))
    TW_HANDL = db.Column(db.String(100))
    PCIP01 = db.Column(db.Float(5))
    PCIP03 = db.Column(db.Float(5))
    PCIP04 = db.Column(db.Float(5))
    PCIP05 = db.Column(db.Float(5))
    PCIP09 = db.Column(db.Float(5))
    PCIP10 = db.Column(db.Float(5))
    PCIP11 = db.Column(db.Float(5))
    PCIP12 = db.Column(db.Float(5))
    PCIP13 = db.Column(db.Float(5))
    PCIP14 = db.Column(db.Float(5))
    PCIP15 = db.Column(db.Float(5))
    PCIP16 = db.Column(db.Float(5))
    PCIP19 = db.Column(db.Float(5))
    PCIP22 = db.Column(db.Float(5))
    PCIP23 = db.Column(db.Float(5))
    PCIP24 = db.Column(db.Float(5))
    PCIP25 = db.Column(db.Float(5))
    PCIP26 = db.Column(db.Float(5))
    PCIP27 = db.Column(db.Float(5))
    PCIP29 = db.Column(db.Float(5))
    PCIP30 = db.Column(db.Float(5))
    PCIP31 = db.Column(db.Float(5))
    PCIP38 = db.Column(db.Float(5))
    PCIP39 = db.Column(db.Float(5))
    PCIP40 = db.Column(db.Float(5))
    PCIP41 = db.Column(db.Float(5))
    PCIP42 = db.Column(db.Float(5))
    PCIP43 = db.Column(db.Float(5))
    PCIP44 = db.Column(db.Float(5))
    PCIP45 = db.Column(db.Float(5))
    PCIP46 = db.Column(db.Float(5))
    PCIP47 = db.Column(db.Float(5))
    PCIP48 = db.Column(db.Float(5))
    PCIP49 = db.Column(db.Float(5))
    PCIP50 = db.Column(db.Float(5))
    PCIP51 = db.Column(db.Float(5))
    PCIP52 = db.Column(db.Float(5))
    PCIP54 = db.Column(db.Float(5))
    UGDS = db.Column(db.Float(5))
    TUITIONFEE_IN = db.Column(db.Float(5))
    TUITIONFEE_OUT = db.Column(db.Float(5))
    CDR2 = db.Column(db.Float(5))
    CDR3 = db.Column(db.Float(5))
    ADJ_ADM_RATE = db.Column(db.Float(5))
    OTHER_AFFIL = db.Column(db.String(100))
    REL_AFFIL = db.Column(db.String(100))
    COUNT_MISSING = db.Column(db.Integer)
    VALUE_INDEX = db.Column(db.Float(5))
    CARE_INDEX = db.Column(db.Float(5))
    fin_MN_EARN_WNE_P6 = db.Column(db.Float(5))
    fin_DEBT_MDN = db.Column(db.Float(5))
    fin_C150_4_COMB = db.Column(db.Float(5))
    fin_COSTT4_COMB = db.Column(db.Float(5))
    fin_WDRAW_ORIG_YR6_RT = db.Column(db.Float(5))
    fin_NPT4_COMB = db.Column(db.Float(5))
    fin_PCTPELL = db.Column(db.Float(5))
    fin_RET_FT4_COMB = db.Column(db.Float(5))
    fin_RET_PT4_COMB = db.Column(db.Float(5))
    fin_ADJ_AVGFACSAL = db.Column(db.Float(5))
    fin_ADJ_INEXPFTE = db.Column(db.Float(5))
    fin_PFTFTUG1_EF = db.Column(db.Float(5))
    fin_PFTFAC = db.Column(db.Float(5))
    fin_COMB_RET_RATE = db.Column(db.Float(5))
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
    
    
    
    def __init__(self,cs_index, OPEID,OPEID6,INSTNM,CITY,STABBR,ZIP5,PREDDEG,HTTPS_INSTURL,HTTPS_NPCURL,
                 HIGHDEG,CONTROL,REGION,LOCALE,LATITUDE,LONGITUDE,CCBASIC,CCUGPROF,CCSIZSET,SATVRMID,
                 SATMTMID,SATWRMID,ACTCMMID,ACTENMID,ACTMTMID,ACTWRMID,POP_SUBS,FB_HANDL,TW_HANDL,PCIP01,
                 PCIP03,PCIP04,PCIP05,PCIP09,PCIP10,PCIP11,PCIP12,PCIP13,PCIP14,PCIP15,PCIP16,PCIP19,PCIP22,
                 PCIP23,PCIP24,PCIP25,PCIP26,PCIP27,PCIP29,PCIP30,PCIP31,PCIP38,PCIP39,PCIP40,PCIP41,PCIP42,
                 PCIP43,PCIP44,PCIP45,PCIP46,PCIP47,PCIP48,PCIP49,PCIP50,PCIP51,PCIP52,PCIP54,UGDS,
                 TUITIONFEE_IN,TUITIONFEE_OUT,CDR2,CDR3,ADJ_ADM_RATE,OTHER_AFFIL,REL_AFFIL,COUNT_MISSING,
                 VALUE_INDEX,CARE_INDEX,fin_MN_EARN_WNE_P6,fin_DEBT_MDN,fin_C150_4_COMB,fin_COSTT4_COMB,
                 fin_WDRAW_ORIG_YR6_RT,fin_NPT4_COMB,fin_PCTPELL,fin_RET_FT4_COMB,fin_RET_PT4_COMB,
                 fin_ADJ_AVGFACSAL,fin_ADJ_INEXPFTE,fin_PFTFTUG1_EF,fin_PFTFAC,fin_COMB_RET_RATE,
                 MN_EARN_WNE_P6_PRESENT,DEBT_MDN_PRESENT,C150_4_COMB_PRESENT,COSTT4_COMB_PRESENT,
                 WDRAW_ORIG_YR6_RT_PRESENT,NPT4_COMB_PRESENT,PCTPELL_PRESENT,RET_FT4_COMB_PRESENT,
                 RET_PT4_COMB_PRESENT,ADJ_AVGFACSAL_PRESENT,ADJ_INEXPFTE_PRESENT,PFTFTUG1_EF_PRESENT,
                 PFTFAC_PRESENT,fin_COMB_RET_RATE_PRESENT,rankp_MN_EARN_WNE_P6,rankp_DEBT_MDN,
                 rankp_C150_4_COMB,rankp_COSTT4_COMB,rankp_WDRAW_ORIG_YR6_RT,rankp_NPT4_COMB,rankp_PCTPELL,
                 rankp_ADJ_AVGFACSAL,rankp_ADJ_INEXPFTE,rankp_PFTFAC,rankp_COMB_RET_RATE):
        self.cs_index = cs_index
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
        self.POP_SUBS = POP_SUBS
        self.FB_HANDL = FB_HANDL
        self.TW_HANDL = TW_HANDL
        self.PCIP01 = PCIP01
        self.PCIP03 = PCIP03
        self.PCIP04 = PCIP04
        self.PCIP05 = PCIP05
        self.PCIP09 = PCIP09
        self.PCIP10 = PCIP10
        self.PCIP11 = PCIP11
        self.PCIP12 = PCIP12
        self.PCIP13 = PCIP13
        self.PCIP14 = PCIP14
        self.PCIP15 = PCIP15
        self.PCIP16 = PCIP16
        self.PCIP19 = PCIP19
        self.PCIP22 = PCIP22
        self.PCIP23 = PCIP23
        self.PCIP24 = PCIP24
        self.PCIP25 = PCIP25
        self.PCIP26 = PCIP26
        self.PCIP27 = PCIP27
        self.PCIP29 = PCIP29
        self.PCIP30 = PCIP30
        self.PCIP31 = PCIP31
        self.PCIP38 = PCIP38
        self.PCIP39 = PCIP39
        self.PCIP40 = PCIP40
        self.PCIP41 = PCIP41
        self.PCIP42 = PCIP42
        self.PCIP43 = PCIP43
        self.PCIP44 = PCIP44
        self.PCIP45 = PCIP45
        self.PCIP46 = PCIP46
        self.PCIP47 = PCIP47
        self.PCIP48 = PCIP48
        self.PCIP49 = PCIP49
        self.PCIP50 = PCIP50
        self.PCIP51 = PCIP51
        self.PCIP52 = PCIP52
        self.PCIP54 = PCIP54
        self.UGDS = UGDS
        self.TUITIONFEE_IN = TUITIONFEE_IN
        self.TUITIONFEE_OUT = TUITIONFEE_OUT
        self.CDR2 = CDR2
        self.CDR3 = CDR3
        self.ADJ_ADM_RATE = ADJ_ADM_RATE
        self.OTHER_AFFIL = OTHER_AFFIL
        self.REL_AFFIL = REL_AFFIL
        self.COUNT_MISSING = COUNT_MISSING
        self.VALUE_INDEX = VALUE_INDEX
        self.CARE_INDEX = CARE_INDEX
        self.fin_MN_EARN_WNE_P6 = fin_MN_EARN_WNE_P6
        self.fin_DEBT_MDN = fin_DEBT_MDN
        self.fin_C150_4_COMB = fin_C150_4_COMB
        self.fin_COSTT4_COMB = fin_COSTT4_COMB
        self.fin_WDRAW_ORIG_YR6_RT = fin_WDRAW_ORIG_YR6_RT
        self.fin_NPT4_COMB = fin_NPT4_COMB
        self.fin_PCTPELL = fin_PCTPELL
        self.fin_RET_FT4_COMB = fin_RET_FT4_COMB
        self.fin_RET_PT4_COMB = fin_RET_PT4_COMB
        self.fin_ADJ_AVGFACSAL = fin_ADJ_AVGFACSAL
        self.fin_ADJ_INEXPFTE = fin_ADJ_INEXPFTE
        self.fin_PFTFTUG1_EF = fin_PFTFTUG1_EF
        self.fin_PFTFAC = fin_PFTFAC
        self.fin_COMB_RET_RATE = fin_COMB_RET_RATE
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



