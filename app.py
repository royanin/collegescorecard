from dash import Dash
import flask
from flask_app import flask_app
import os


app = Dash('app', server=flask_app, url_base_pathname='/',
          meta_tags=[{"charset": "utf-8"},
            {"name": "description",
            "content": 'US has thousands of colleges and universities. At CollegeScoreCard.io you can find out more on their cost, graduation rate, average debt incurred by students, admission rate, and so on. Built on official DoE data. Easier to compare and make sense.'},
            {"http-equiv": "X-UA-Compatible", "content": "IE=edge"},
            {"name": "viewport", "content": "width=device-width, initial-scale=1"},
            {"property": "og:image", "content":"/assets/csc_to_img.jpg"}
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
