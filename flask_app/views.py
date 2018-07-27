from flask import render_template, flash, redirect, session, url_for, request, g, json, jsonify, send_from_directory
from flask_app import flask_app, db, WARN_LEVEL
from models import Wiki_summary, Nat_avg, School_details, Message
from .forms import ContactForm
from .emails import notify_server_error, new_message



@flask_app.route('/twt/<uid>')
def show_tw(uid):
    w = db.session.query(Wiki_summary).filter_by(uid=uid).first()
    if w.TW_HANDL != None:
        return('<a class="twitter-timeline" href="https://twitter.com/'+str(w.TW_HANDL)+'?ref_src=twsrc%5Etfw/">Tweets</a> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>')
    else:
        return("<h4>Sorry, we can't find the twitter feed...</h4>")

@flask_app.route('/wiki_summary/<uid>')
def show_wiki_summary(uid):
    w = db.session.query(Wiki_summary).filter_by(uid=uid).first()
    if w != None:
        return render_template("wiki_summary.html",w=w)
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
    
    
@flask_app.route('/explainer')
def explainer():

    return render_template("explainer.html")    

