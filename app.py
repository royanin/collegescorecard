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

app = Dash('app', server=flask_app, url_base_pathname='/',
          meta_tags=[{"charset": "utf-8"},
            {"name": "description",
            "content": 'US has thousands of colleges and universities. At CollegeScoreCard.io you can find out more on their cost, graduation rate, average debt incurred by students, admission rate, and so on. Built on official DoE data. Easier to compare and make sense.'},
            {"http-equiv": "X-UA-Compatible", "content": "IE=edge"},
            {"name": "viewport", "content": "width=device-width, initial-scale=1"}
]
)


#app = Dash('app', server=flask_app, url_base_pathname='/',)
app.title = "CollegeScoreCard.io"
app.index_string = '''
<!DOCTYPE html>
<html lang="en-US">
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        <!--<div>My Custom header</div>-->
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
        </footer>
        <div><br></div>
    </body>
</html>
'''
#app.title = "CollegeScoreCard.io"
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

#css_directory = os.getcwd()
#stylesheets = ['plt.css']
#static_css_route = '/flask_app/static/css/'

#@flask_app.route('{}<stylesheet>'.format(static_css_route))
#def serve_stylesheet(stylesheet):
#    if stylesheet not in stylesheets:
#        raise Exception(
#            '"{}" is excluded from the allowed static files'.format(
#                stylesheet
#            )
#        )
#    print 'css_file_directory:',css_directory+static_css_route
#    return flask.send_from_directory(css_directory+static_css_route, stylesheet)


#for stylesheet in stylesheets:
#    app.css.append_css({"external_url": "/flask_app/static/css/{}".format(stylesheet)})
