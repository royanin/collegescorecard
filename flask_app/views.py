from flask import render_template, flash, redirect, session, url_for, request, g, json, jsonify, send_from_directory, make_response
from flask_app import flask_app, db, WARN_LEVEL, MAX_SEARCH_RESULTS, subj_dict
from models import Wiki_summary, Nat_avg, School_details, Message
import flask_whooshalchemy as whooshalchemy
from .forms import ContactForm
from .emails import notify_server_error, new_message
from .utils import order_pop_subs, suggest_featured_schools
from datetime import datetime, timedelta


@flask_app.route('/twt/<uid>')
def show_tw(uid):
    w = db.session.query(Wiki_summary).filter_by(uid=uid).first()
    if w.TW_HANDL != None:
        return('<a class="twitter-timeline" href="https://twitter.com/'+str(w.TW_HANDL)+'?ref_src=twsrc%5Etfw/">Tweets</a> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>')
    else:
        return("<h4>Sorry, we can't find the twitter feed...</h4>")

@flask_app.route('/wiki_summary/<uid>')
def show_wiki_summary(uid):
    wiki_social = db.session.query(Wiki_summary).filter_by(uid=uid).first()
    if wiki_social != None:
        return render_template("wiki_summary.html",wiki_social=wiki_social)
    else:
        return ("No entries found.")


@flask_app.route('/numbers/<uid>')
def show_numbers(uid):
    #sch = db.session.query(School_details).filter_by(cs_index=cs_index).first()
    sch = db.session.query(School_details).filter_by(uid=uid).first()
    nat_mean = db.session.query(Nat_avg).filter_by(CCBASIC=sch.CCBASIC).first()
    if sch != None:
        return render_template("numbers.html",sch=sch,nat_mean=nat_mean,WARN_LEVEL=WARN_LEVEL)
    else:
        return ("No entries found.")
    

@flask_app.route('/social/')
def social_shares():

    return render_template("form_share_social.html")


@flask_app.route('/contact_us', methods=['GET', 'POST'])
def contact_form():
    g.contact_form = ContactForm()

    #get the request details
    if request.method == "POST" and g.contact_form.validate_on_submit():
        sender_email = g.contact_form.email.data
        sender_msg = g.contact_form.message.data
        sender_type = g.contact_form.contact_reason.data
        get_newsletter = g.contact_form.get_newsletter.data

        session['message'] = "Thank you for getting in touch with us!"
        
        #The following line sends email
        new_message(sender_email,sender_msg, sender_type, get_newsletter)
        #The next 3 lines store the message in the database email
        new_msg = Message(body=sender_msg,
                          email=sender_email,
                          sender_type=sender_type,
                            subscribed=False)
        db.session.add(new_msg)
        db.session.commit()            
        
        return ('', 204)

    elif request.method == "POST":
        if g.contact_form.validate_on_submit() is not True:
            session['message'] = "Sorry, your message couldn't be sent. Please try again."            
            return ('', 204)
    elif request.method == "GET":
        return render_template("contact_form.html")
    
    
@flask_app.route('/explainer',methods=['GET'])
def explainer():

    return render_template("explainer.html")   


@flask_app.route('/profile/<uid>', methods=['GET', 'POST'])
def school_profile(uid):
    g.contact_form = ContactForm()
    if uid == None:
        print 'profile inst. is missing..'
        return redirect("/")
    else:
        #Search for a school in School_details, wiki_summary, and national_mean
        sch = db.session.query(School_details).filter_by(uid=uid.lower()).first()
        wiki_social = db.session.query(Wiki_summary).filter_by(uid=uid.lower()).first()
        if sch != None:
            nat_mean = db.session.query(Nat_avg).filter_by(CCBASIC=sch.CCBASIC).first()
        else:
            return redirect(url_for('search'))
        
        if sch != None:
            #print sch.INSTNM
            #Define map_string here -- easier than defining it in the template
            lat = sch.LATITUDE
            long = sch.LONGITUDE
            map_range = 0.01
            bbox = [str(long - map_range), str(lat - map_range), str(long + map_range),
                    str(lat + map_range)]
            map_string = "//www.openstreetmap.org/export/embed.html?bbox="+"%2C".join(bbox[:])+"&marker="+str(lat)+"%2C"+str(long)+"&layers=ND"

            #Rendering pop_subs:
            xlabels,ylabels = order_pop_subs(sch.POP_SUBS)
            num_pop_subs = len(xlabels)

            #Convert ADJ_ADM_RATE to pct
            adm_pct = round(sch.ADJ_ADM_RATE*100,1)

            #Check if any SAT or ACT scores is present
            SAT_PRESENT = 0
            ACT_PRESENT = 0
            if sch.SATVRMID != None or sch.SATMTMID != None or sch.SATWRMID != None:
                SAT_PRESENT = 1
            if sch.ACTCMMID != None or sch.ACTENMID != None or sch.ACTMTMID != None or sch.ACTWRMID != None:
                ACT_PRESENT = 1

            if wiki_social.TW_HANDL != "":
                print wiki_social.TW_HANDL
                if wiki_social.TW_HANDL[-1]==" ":
                    TW_ALT = wiki_social.TW_HANDL.rstrip()
                else:
                    TW_ALT = wiki_social.TW_HANDL
            else:
                print wiki_social.TW_HANDL
                TW_ALT = ""
                
            #Find similar featured schools (Care score and value score within +/-3 )
            feat_list = suggest_featured_schools(sch.Value_score,sch.Care_score,uid=sch.uid)

            return render_template("profile.html",
                                   sch=sch,
                                   wiki_social=wiki_social,
                                   nat_mean=nat_mean,
                                   WARN_LEVEL=WARN_LEVEL,
                                   map_string=map_string,
                                   xlabels=xlabels,
                                   ylabels=ylabels,
                                   num_pop_subs=num_pop_subs,
                                   adm_pct = adm_pct,
                                   SAT_PRESENT = SAT_PRESENT,
                                   ACT_PRESENT = ACT_PRESENT,
                                   TW_ALT=TW_ALT,
                                   feat_list=feat_list)

        else:
            return ("No entries found.") 


@flask_app.route('/profile', methods=['GET'])
@flask_app.route('/profile/', methods=['GET'])
@flask_app.route('/search', methods=['GET','POST'])
def search():
    if request.method == "GET":
        feat_list1 = suggest_featured_schools(90,90,uid=None)
        feat_list2 = suggest_featured_schools(70,70,uid=None)        
        return render_template('search.html',
                               feat_list1=feat_list1,
                               feat_list2=feat_list2) 

    #g.search_form = SearchForm()
    elif request.method == "POST":
        print 'POST request'
        query = request.form.get('autocomplete')
        print query


    
    results_schools = School_details.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
    results_wiki = Wiki_summary.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
    
    for item in results_schools:
        print item.INSTNM, item.uid
    print '\n\n'
    for item in results_wiki:
        print item.inst_nm, item.uid

    #If there's no result, message plus exit:
    if (len(results_schools)+ len(results_wiki) == 0):
        return render_template('search_results.html',
                               query = query,
                               results = None,
                               result_type = None,
                               results_count = 0)
                               #search_message="Sorry! No result found for {}. Check spelling and give it another go?"

    #If there's only 1 result, go straight to profile:
    if len(results_schools) == 1:
        link = results_schools[0].uid
        print 'In 1 result', link
        return redirect("/profile/"+link)
    elif len(results_schools) ==0 and len(results_wiki) == 1:
        link = results_wiki[0].uid
        print 'In 1 result', link
        return redirect("/profile/"+link)
    
    if len(results_schools) > 1:
        results = results_schools
        #results_count = len(results)
        result_type = 'school_table'
    elif len(results_schools) == 0 and len(results_wiki)>1:
        results = results_wiki
        result_type = 'wiki_table'

        
    results_count = len(results)
    print results,result_type,results_count
    return render_template('search_results.html',
                               query = query,
                               results = results,
                               result_type = result_type,
                               results_count = results_count)
                               #search_message=None)
    
    
# a route for generating sitemap.xml
@flask_app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    """Generate sitemap.xml. Makes a list of urls and date modified."""
    pages=[]
    pages_temp = []
    ws_url_string = "https://collegescorecard.io"
    ten_days_ago=(datetime.now() - timedelta(days=10)).date().isoformat()
    # static pages
    for rule in flask_app.url_map.iter_rules():
        if "GET" in rule.methods and len(rule.arguments)==0:
            pages_temp.append(
                [rule.rule,ten_days_ago]
            )

    for item in pages_temp:
        #if item[0] == '/_dash-dependencies':
        if item[0] in ['/_dash-dependencies','/_dash-layout','/_dash-routes','/profile/','/profile','/social/']:
            pass
        else:
            pages.append(item)
    
    print pages
    # school model pages
    sch_list = db.session.query(School_details).all()
    for sch in sch_list:
        url=url_for('school_profile',uid=sch.uid)
        #modified_time=sch.modified_time.date().isoformat()
        modified_time=ten_days_ago
        pages.append([url,modified_time]) 

    sitemap_xml = render_template('sitemap_template.xml', pages=pages, ws_url_string=ws_url_string)
    response= make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"    
    
    return response