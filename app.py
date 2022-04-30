import pandas as pd
import pandas_datareader.data as wb
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from pytrends.request import TrendReq




#CREAMOS UNA FUNCION DONDE NOS VA A DEVOLVER TODOS LOS NOMBRES DE LAS EMPRESAS QUE TENEMOS EN UN ARCHIVO EXCEL
def total_datos_read():
    datos = pd.read_excel("DATA/Market Ticker.xls")
    return datos

#CREAMOS UNA FUNCION PARA QUE AL METER EL NOMBRE DE LA EMPRESA ME PILLE DIRECTAMENTE EL TICKER
def ticker_para_empresa():
    ticker = st.sidebar.selectbox("Seleccione una empresa", datos["Name"])
    ticker = datos.loc[datos["Name"] == ticker, "Ticker" ]
    return ticker

#CREAMOS EL DATAFRAME DONDE VAMOS A TENER TODOS LOS DATOS DE BOLSA DE LA EMPRESA QUE EL USUARIO DECIDA
def dataframe():
    dataframe = pd.DataFrame()
    for i in ticker:
        data = wb.DataReader(ticker , "yahoo")[[ "High","Low"]]
        dataframe["High"] = data["High"]
        dataframe["Low"] = data["Low"]
        dataframe = dataframe.tail(20)
    return dataframe

    

# FUNCION PARA GRAFICAR LOS VALORES MINIMO Y MAXIMO DE LA EMPRESA QUE EL USUARIO DECIDA PARA COMPARARLO CON LA GRAFICA QUE CREEMOS DE GOOGLE TRENDS

def graficar_yahoo(dataframe):

    fig = go.Figure(data=go.Scatter(x = dataframe.index ,  y=dataframe["High"],mode='lines+markers', line_color='#ffe476'))
    fig.add_trace(go.Scatter(x = dataframe.index , y=dataframe["Low"],mode='lines+markers', line=dict(color="#0000ff")))
    grafico = fig.show()
    return grafico

#HACEMOS LA LLAMADA A LAS FUNCIONES QUE PREVIAMENTE HEMOS CREADO, PARA POSTERIORMENTE CREAR EL STREAMLIT
 
if __name__ == "__main__":

    tickers = total_datos_read()
    ticker = ticker_para_empresa()
    total_ticker_data = dataframe()
    plot_yahoo_finance= graficar_yahoo()


#MONTAMOS EL STREAMLIT EN EL QUE VAMOS A TENER LAS GRAFICAS DE YAHOO FINANCE Y DE GOOGLE TRENDS, CON UN SIDEBAR PARA QUE EL USUARIO META EL NOMBRE DE LA EMPRESA QUE QUIERA.
#PARA PODER HACER LA COMPARATIVA ENTRE LAS BUSQUEDAS DE GOOGLE TRENDS CON LOS DATOS DE BOLSA DE LA EMPRESA QUE EL USUARIO HA DECIDIDO.

st.title("MARKET STOCK DASHBOARD")
st.dataframe(total_ticker_data)
st.plotly_chart(plot_yahoo_finance)






















