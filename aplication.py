import pandas as pd
import pandas_datareader.data as wb
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from pytrends.request import TrendReq

import streamlit.components.v1 as components
import requests
import streamlit as st
import tweepy
import csv
import re
import emoji_data_python




#CREAMOS UNA FUNCION DONDE NOS VA A DEVOLVER TODOS LOS NOMBRES DE LAS EMPRESAS QUE TENEMOS EN UN ARCHIVO EXCEL
def total_datos_read1():
    datos = pd.read_excel("DATA/Market Ticker.xls")
    return datos

#CREAMOS UNA FUNCION PARA QUE AL METER EL NOMBRE DE LA EMPRESA ME PILLE DIRECTAMENTE EL TICKER
def ticker_para_empresa1():
    company_name = st.sidebar.selectbox("Seleccione una empresa", datos["Name"])
    ticker_name = datos.loc[datos["Name"] == company_name, "Ticker" ]
    return ticker_name, company_name

#CREAMOS EL DATAFRAME DONDE VAMOS A TENER TODOS LOS DATOS DE BOLSA DE LA EMPRESA QUE EL USUARIO DECIDA
def create_dataframe(ticker_name):
    dataframe = pd.DataFrame()
    for i in ticker_name:
        data = wb.DataReader(ticker_name , "yahoo")[[ "High","Low"]]
        dataframe["High"] = data["High"]
        dataframe["Low"] = data["Low"]
        

        dataframe = dataframe.tail(7)
    return dataframe

#FUNCION PARA OBTENER LOS DATOS DE GOOGLE TRENDS ANTES DE GRAFICARLOS, NOS DA LOS DATOS DE 3 MESES, PERO PODEMOS PONER LOS DATOS DESDE QUE QUERAMOS. 
def obtain_google_trends(company_name):
    pytrends = TrendReq(hl='en-US', tz=360)

    pytrends.build_payload([company_name], cat=0, timeframe='today 3-m') # NO PUEDO PONER MAS DE 3 MESES (90 dias) SI QUIERO TENER LOS DATOS DIARIOS.
    data = pytrends.interest_over_time() 
    data = data.reset_index() 
    data = data.tail(7)
    return data

#FUNCION PARA GRAFICAR LOS DATOS DE GOOGLE TRENDS.

def plot_google_trends(data, company_name):

    fig = px.line(data, x="date", y=company_name, title='GRAFICO SOBRE BUSQUEDAS DE LA EMPRESA', width = 500, height= 400)
    return fig




    

#FUNCION PARA IGUALAR EL TICKER DE LA EMPRESA AL NOMBRE DE LA EMPRESA, PARA NO TENER QUE INTRODUCIR EL TICKER.
def ticker_para_empresa2():
    company_name2= st.sidebar.selectbox("Seleccione segunda empresa", datos["Name"])
    ticker_name2 = datos.loc[datos["Name"] == company_name2, "Ticker" ]
    return ticker_name2, company_name2

#FUNCION PARA GRAFICAR LOS DATOS OBTENIDOS DE YAHOO FINANCE
def graficar_yahoo(dataframe):
    fig2 = px.line(dataframe, x=dataframe.index, y=['High', 'Low'] , width=500, height=400)
    

    #fig2 = go.Figure(data=go.Scatter(x = dataframe.index ,  y=dataframe["High", "Low"],mode='lines+markers', line_color='#ffe476'))
    # fig2.add_trace(go.Scatter(x = dataframe.index , y=dataframe["Low"],mode='lines+markers', line=dict(color="#0000ff")))
    #grafico = fig.show()
    return fig2

#FUNCION PARA PODER OBTENER LOS TWEETS Y MOSTRARLOS POSTERIORMENTE MOSTRAR LOS TWEETS CON IFRAME
def extractTweet(url):

    api = "https://publish.twitter.com/oembed?url={}".format(url)
    response = requests.get(api)
    res = response.json()["html"]
    return res



#HACEMOS LA LLAMADA A LAS FUNCIONES QUE PREVIAMENTE HEMOS CREADO, PARA POSTERIORMENTE CREAR EL STREAMLIT
 
if __name__ == "__main__":
    
    datos = total_datos_read1()
    ticker, company_name = ticker_para_empresa1()
    ticker2 , company_name2 = ticker_para_empresa2()
    dataframe = create_dataframe(ticker)
    dataframe_2 = create_dataframe(ticker2)
    

    grafico = graficar_yahoo(dataframe)
    grafico_2 = graficar_yahoo(dataframe_2)


    dataframe_google_trends1 = obtain_google_trends(company_name)
    grafico_google_trends1 = plot_google_trends(dataframe_google_trends1, company_name)

    dataframe_google_trends2 = obtain_google_trends(company_name2)
    grafico_google_trends2 = plot_google_trends(dataframe_google_trends2, company_name2)


    st.title("MARKET STOCK DASHBOARD")
    st.image("https://i.pinimg.com/474x/57/c4/46/57c44638a33198a802e30cc93619f668--city-state-the-state.jpg",width= 600)
    st.header(company_name)
    st.table(dataframe)
    st.header(company_name2)
    st.table(dataframe_2)
    


    st.header("GRAFICO YAHOO FINANCE" )
    col1, col2 = st.columns(2)

    col1.plotly_chart(grafico)
    col2.plotly_chart(grafico_2)

    st.header("GRAFICO GOOGLE TRENDS" )

    col1, col2 = st.columns(2)

    col1.plotly_chart(grafico_google_trends1)
    col2.plotly_chart(grafico_google_trends2)

    # components.iframe("https://docs.streamlit.io/en/latest", height= 900)

    #components.html('<iframe width="320" height="540" src="https://www.instagram.com/p/BT8cmZRlkVJ/embed" frameborder="0"></iframe>', height= 550)
    # components.html('<blockquote class="instagram-media" data-instgrm-version="7" ><a href="https://www.instagram.com/p/BT8cmZRlkVJ/"></a> </blockquote><script async defer src="//platform.instagram.com/en_US/embeds.js"></script>', height= 900)

    #components.html(extractTweet("https://twitter.com/elpais_economia/status/1520297104077475840"), height= 550, scrolling = True)
    # components.html('<blockquote class="twitter-tweet"><p lang="es" dir="ltr">Google tiene una inteligencia artificial capaz de entender el sentido del humor <a href="https://t.co/O3yTKE1nOM">https://t.co/O3yTKE1nOM</a> <a href="https://twitter.com/hashtag/turismo?src=hash&amp;ref_src=twsrc%5Etfw">#turismo</a> <a href="https://twitter.com/hashtag/google?src=hash&amp;ref_src=twsrc%5Etfw">#google</a> <a href="https://twitter.com/hashtag/inteligenciaartificial?src=hash&amp;ref_src=twsrc%5Etfw">#inteligenciaartificial</a> <a href="https://t.co/Ll3q5zDIYp">pic.twitter.com/Ll3q5zDIYp</a></p>&mdash; Boletinviajesvzla (@boletinviajesve) <a href="https://twitter.com/boletinviajesve/status/1520040217566072832?ref_src=twsrc%5Etfw">April 29, 2022</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>', height= 550)


    

    
    components.iframe("https://www.eleconomista.es", height= 1000, width= 1000, scrolling = True)

    components.iframe("https://www.wsj.com", height= 1000, width= 1000, scrolling = True)





    
#BUSCADOR DE TWEETS



default_accounts = ['LizAnnSonders', 
  'bespokeinvest', 
  'Schuldensuehner', 
  'expansioncom', 
  'Reuters', 
  'sentimentrader', 
  'WSJecon', 
  'zerohedge',
  'WSJmarkets',
  'markets',
  'InvestingEspana',
  'Investingcom',
  'lisaabramowicz1',
  'Stocktwits',
  'SJosephBurns',
  'MarketWatch',
  'PeterSchiff',
  'alphatrends',
  'cnbc',
  'traderstewie',
  'tradertvshawn',
  'OptionsHawk'
  ]
accounts = default_accounts + ['']


@st.cache
def get_tweets(account):
    return api.user_timeline(screen_name=account, count=200, tweet_mode='extended')


st.sidebar.title('Get Tweets')
st.sidebar.markdown('A [simple demonstration](https://github.com/CaliberAI/streamlit-get-tweets) of using [Streamlit](https://streamlit.io/) with [Tweepy](https://www.tweepy.org/) to get Tweets from Twitter Accounts.')
api_key = st.sidebar.text_input('Twitter API Key', '')
api_secret_key = st.sidebar.text_input('Twitter API Secret Key', '')
access_token = st.sidebar.text_input('Twitter Access Token', '')
access_token_secret = st.text_input('Twitter Access Token Secret', '')
included_accounts = st.sidebar.multiselect('Accounts', accounts, default_accounts)
go = st.sidebar.button('Get Tweets')

if go:
    try:
        auth = tweepy.OAuthHandler(api_key, api_secret_key)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        tweets = []
        for account in included_accounts:
            st.write(account)
            api_response = get_tweets(account)
            for tweet in api_response:
                if tweet.retweeted:
                    text = tweet.retweeted_status.full_text
                else:
                    text = tweet.full_text
                if tweet.lang == 'en':
                    text = re.sub('http://\S+|https://\S+', ' ', text)
                    text = re.sub(emoji_data_python.get_emoji_regex(), ' ', text)
                    text = re.sub('\n', ' ', text)
                    text = re.sub('&amp;', '&', text)
                    text = re.sub('@', '', text)
                    text = re.sub('  ', ' ', text)
                
                    tweets += [[tweet.user.screen_name, text, tweet.id_str]]
        st.sidebar.subheader('Tweets')
        st.sidebar.dataframe(tweets)
        with open('tweets.csv', 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerows(tweets)
    except ApiException as e:
        st.sidebar.exception("Exception: %s\n" % e)

  

