from dash import Dash, callback, html, dcc
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import matplotlib as mpl
import gunicorn                     #whilst your local machine's webserver doesn't need this, Heroku's linux webserver (i.e. dyno) does. I.e. This is your HTTP server
from whitenoise import WhiteNoise   #for serving static files on Heroku
from dash.dependencies import Input, Output

# Instantiate dash app
# app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = Dash(__name__, external_stylesheets=external_stylesheets)

# Reference the underlying flask app (Used by gunicorn webserver in Heroku production deployment)
server = app.server 

# Enable Whitenoise for serving static files from Heroku (the /static folder is seen as root by Heroku) 
server.wsgi_app = WhiteNoise(server.wsgi_app, root='static/') 

# Define Dash layout
def create_dash_layout(app):

    # Set browser tab title
    app.title = "Titulo de la pagina" 
    
    # Header
    header = html.Div([html.Br(), dcc.Markdown(""" # Hi. I'm your Dash app."""), html.Br()])
    
    # Body 
    #body = html.Div([dcc.Markdown(""" ## I'm ready to serve static files on Heroku. Just look at this! """), html.Br(), html.Img(src='charlie.png')])

    # Footer
    #footer = html.Div([html.Br(), html.Br(), dcc.Markdown(""" ### Built with ![Image](heart.png) in Python using [Dash](https://plotly.com/dash/)""")])
    
    # Assemble dash layout 
    #app.layout = html.Div([header, body, footer])
    app.layout = html.Div([header,
    dcc.Input(id="input-1", type="text", value="Montréal"),
    dcc.Input(id="input-2", type="text", value="Canada"),
    html.Div(id="number-output"),
    ])  

    return app

# Construct the dash layout
create_dash_layout(app)

@app.callback(
    Output("number-output", "children"),
    Input("input-1", "value"),
    Input("input-2", "value"),
)
def update_output(input1, input2):
    return u'Input 1 is "{}" and Input 2 is "{}"'.format(input1, input2)

# Run flask app
if __name__ == "__main__": app.run_server(debug=False, host='0.0.0.0', port=8050)
