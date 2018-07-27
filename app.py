from dash import Dash
import flask
#from flask_sqlalchemy import SQLAlchemy
#from flask import render_template
from flask_app import flask_app
import os

#server = flask.Flask('apps')
#server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
#server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db = SQLAlchemy(server)
#con=db.engine.connect().connection
#print con

app = Dash('app', server=flask_app, url_base_pathname='/')
app.config.suppress_callback_exceptions = True
app.scripts.config.serve_locally = False



app.css.append_css({
    "external_url": "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
})

app.css.append_css({
    #"external_url": "https://fonts.googleapis.com/css?family=Montserrat:400,300,600"
    "external_url": "https://fonts.googleapis.com/css?family=Roboto:500,400|Montserrat:400"
})

#app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

css_directory = os.getcwd()
stylesheets = ['plt.css']
static_css_route = '/flask_app/static/css/'

@flask_app.route('{}<stylesheet>'.format(static_css_route))
#@app.server.route('{}<stylesheet>'.format(static_css_route))
def serve_stylesheet(stylesheet):
    if stylesheet not in stylesheets:
        raise Exception(
            '"{}" is excluded from the allowed static files'.format(
                stylesheet
            )
        )
    print 'css_file_directory:',css_directory+static_css_route
    return flask.send_from_directory(css_directory+static_css_route, stylesheet)


for stylesheet in stylesheets:
    app.css.append_css({"external_url": "/flask_app/static/css/{}".format(stylesheet)})
