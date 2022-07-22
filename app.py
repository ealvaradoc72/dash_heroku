from dash import Dash, callback, html, dcc
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import matplotlib as mpl
import gunicorn                     #whilst your local machine's webserver doesn't need this, Heroku's linux webserver (i.e. dyno) does. I.e. This is your HTTP server
from whitenoise import WhiteNoise   #for serving static files on Heroku
import plotly.express as px
from dash.dependencies import Input, Output

# Instantiate dash app
# app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

#Aqui voy a leer el archivo de las proporciones en cada tiempo t
#y crear una lista de listas con las proporciones en cada tiempo

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')


app = Dash(__name__, external_stylesheets=external_stylesheets)

K = np.array([
    [[0.25,0.20,0.40,0.15],[0.00,0.94,0.04,0.02],[0.01,0.19,0.30,0.50],[0.10,0.20,0.30,0.40]],
    [[0.02,0.20,0.18,0.60],[0.00,0.60,0.12,0.27],[0.06,0.29,0.18,0.47],[0.05,0.61,0.10,0.23]],
    [[0.00,0.36,0.09,0.55],[0.01,0.49,1.10,0.40],[0.01,0.57,0.09,0.33],[0.03,0.69,0.08,0.20]],
])

M = np.array([150,50,50,50])
politica = K
ka1 = K[0]
n = M.shape[0]
b = np.zeros((n,1))
print("b",b)
print("tpo de B: ", type(b))
print ("n :",n)
print("valor de ka1: ",ka1)
print("tipo de Ka1: ", type(ka1))
c = np.c_[b,ka1.cumsum(axis=1)]
print(c)
print (c[0,0])
print(c[0,1])


def paso (Mt, N, Ka):
    n = Mt.shape[0]
    print("valor de n = ", n)
    acc = np.c_[np.zeros((n,1)),Ka.cumsum(axis=1)]
    print("Valor de Acc : ", acc)
    Mt1 = np.zeros((n))
    #print ("Mt1: ",Mt1)
    #print("Valor de Ka : ", Ka)
    for j in range(n):
        print ("j: ",j)
        for i in range(n):
            #print ("i: ",i)
            aleatorios = np.random.random(int(N * Mt[i]))
            print("tamaño de aleatorios : ", len(aleatorios))
            print("Aleatorios Longitud:  ", len(aleatorios), " valor : ", aleatorios)
            print("Valor de i y j: ", i, " - ", j)
            print("acc de [i, j] ", acc[i, j])
            print("acc de [i, (j + 1)] ", acc[i,(j+1)])
            print("aleatorios >= acc[i, j+1] -> ", aleatorios >= acc[i, j])
            print("aleatorios < acc[i, j+1] -> ", aleatorios < acc[i, (j+1)])
            print ("Total : ",  (aleatorios >= acc[i,j]) & (aleatorios < acc[i, (j+1)]))
            Mt1[i] += sum((aleatorios >= acc[i,j]) & (aleatorios < acc[i, (j+1)]))
            print ("Mt1[i]: ",Mt1[i])
    return Mt1/N

#Primero definimos N definimods M que es el tamaño de mi muestra
N = 3000 # numero de objetos en mi ejemplo
M = np.array([.5,.1666,.1666,.1666])
politica = K

def run_simulation(politica, M, N):
    hist_M = [M]
    #politica = (K1, K2, K3, K4)
    #for i in range(politica):
    for ka in politica:
        hist_M.append(paso(M,N,np.array(ka)))
        M = hist_M[-1]
        print("Valor nuevo de M : ",M)
    print(hist_M)

run_simulation(politica, M, N)    

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
    header = html.Div([html.Br(), dcc.Markdown(""" # Simulación """), html.Br()])
    
    # Body 
    #body = html.Div([dcc.Markdown(""" ## I'm ready to serve static files on Heroku. Just look at this! """), html.Br(), html.Img(src='charlie.png')])

    # Footer
    #footer = html.Div([html.Br(), html.Br(), dcc.Markdown(""" ### Built with ![Image](heart.png) in Python using [Dash](https://plotly.com/dash/)""")])
    
    # Assemble dash layout 
    #app.layout = html.Div([header, body, footer])
    app.layout = html.Div([header,
    dcc.Input(id='input-on-submit', type='text'),
    html.Button('Submit', id='submit-val', n_clicks=0),
    html.Div(id='container-button-basic',
             children='Numero de repeticiones: ') ,                         
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        df['year'].min(),
        df['year'].max(),
        step=None,
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
        id='year-slider'
    )
    ])  

    return app

# Construct the dash layout
create_dash_layout(app)

@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'))
def update_figure(selected_year):
    classes = ['Clase 1', 'Clase 2', 'Clase 3', 'Clase 4']
    df = pd.DataFrame(M)
    df.columns = classes
    filtered_df = df[df.year == selected_year]
    fig = px.bar(df, x="nation", y="count", color="medal", title="Long-Form Input")
    fig.show()

    fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
                     size="pop", color="continent", hover_name="country",
                     log_x=True, size_max=55)

    fig.update_layout(transition_duration=500)

    return fig

# Run flask app
if __name__ == "__main__": app.run_server(debug=False, host='0.0.0.0', port=8050)
