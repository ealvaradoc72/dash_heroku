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




if __name__ == "__main__": 
    app.run_server(debug=False, host='0.0.0.0', port=8050)
    run_simulation(politica, M, N)        
