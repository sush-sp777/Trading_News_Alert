import requests
from twilio.rest import Client

STOCK_NAME="TSLA"
COMPANY_NAME="Tesla Inc"

SMD_Endpoint="https://www.alphavantage.co/query"
NAPI_Endpoint="https://newsapi.org/v2/everything"
newsapi="NEWSAPI"
api_key="YOURAPIKEY"

acc_sid="YOUR_ACC_SID"
Auth_token="AUTH_TOKEN"
params={
    "function":"TIME_SERIES_DAILY",
    "symbol":STOCK_NAME,
    "apikey":api_key
}
response=requests.get(SMD_Endpoint,params=params)
data=response.json()["Time Series (Daily)"]
data_list=[value for (key,value) in data.items()]
yesterday_data=data_list[0]
yesterday_closing_price=yesterday_data["4. close"]

day_before_yesterday_data=data_list[1]
day_before_yesterday_closing_price=day_before_yesterday_data["4. close"]

difference=float(yesterday_closing_price)-float(day_before_yesterday_closing_price)
up_down=None
if difference>0:
    up_down="🔺"
else:
    up_down="🔻"
    
diff_percent=round((difference/float(yesterday_closing_price))*100)

if abs(diff_percent) >0.1:
    parms={
        "apikey":newsapi,
        "qInTitle": COMPANY_NAME
    }
    response=requests.get(NAPI_Endpoint,params=parms)
    articles=response.json()["articles"]
    three_articles=articles[:3]
 
    formated_article=[f"{STOCK_NAME}: {up_down} {diff_percent}%\n Headline: {article['title']}. \n Brief: {article['description']}" for article in three_articles]
    #print(formated_article)

    client=Client(acc_sid,Auth_token)
    for article in formated_article:
        message=client.messages.create(
            body=article,
            from_="YOUR_TWILIO_REAL_NO",
            to="VERIFIED_NO"
        )
        print(message.sid)
