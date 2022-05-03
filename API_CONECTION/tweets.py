#IMOPORTS NECESARIOS
#streamlit==0.49.0
#tweepy==3.8.0
#emoji-data-python==1.3.0

import streamlit as st
import tweepy
import csv
import re
import emoji_data_python

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


