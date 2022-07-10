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

my_input = dcc.Input(value='initial value', type='text')
my_output = html.Div()

# Reference the underlying flask app (Used by gunicorn webserver in Heroku production deployment)
server = app.server 

# Enable Whitenoise for serving static files from Heroku (the /static folder is seen as root by Heroku) 
server.wsgi_app = WhiteNoise(server.wsgi_app, root='static/') 

# Define Dash layout
def create_dash_layout(app):

    # Set browser tab title
    app.title = "Titulo de la pagina" 
    
    # Header
    header = html.Div([html.Br(), dcc.Markdown(""" # Prueba de app para DASH ."""), html.Br()])
    
    # Body 
    #body = html.Div([dcc.Markdown(""" ## I'm ready to serve static files on Heroku. Just look at this! """), html.Br(), html.Img(src='charlie.png')])

    # Footer
    #footer = html.Div([html.Br(), html.Br(), dcc.Markdown(""" ### Built with ![Image](heart.png) in Python using [Dash](https://plotly.com/dash/)""")])
    
    # Assemble dash layout 
    #app.layout = html.Div([header, body, footer])
    app.layout = html.Div([header,
    html.H6("Change the value in the text box to see callbacks in action!"),
    html.Div([
        "Input: ",
        my_input
    ]),
    html.Br(),
    my_output
    ])  

    return app

# Construct the dash layout
create_dash_layout(app)

@app.callback(
    Output(my_output, component_property='children'),
    Input(my_input, component_property='value')
)
def update_output(input_value):
    return f'Output: {input_value}'

# Run flask app
if __name__ == "__main__": app.run_server(debug=False, host='0.0.0.0', port=8050)
