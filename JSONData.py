import requests #To request the api
import json #To manage json type
import MakeModelAndForcast #Python file for perpare data , make model and forcasting
import currences  # Python file that contains symbols and identifiers of digital currencies
import time 

symbol = currences.symbol
ids = currences.ids
informatin=[] # List
crypto = {} # dictionary 
def PredictAndCollectdata():
    #list of percents predicted with votingreg or lstm
    percent=MakeModelAndForcast.PreprocessingAndPredict('votingreg') 
    for i in range(len(ids)):
        time.sleep(3) #interval
        print('make a JSON file')
        print(i+1 ,':', symbol[i] , '*'*(i+1), '\n\n')
        currency={}
        try: #try to request 
            response = requests.get(f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={ids[i]}")
            data = response.text
            #Separate and store the necessary data
            data = data.split(",")
            name = data[2]
            icon = data[3]
        except:
            #bad data or requst is not specified
            print(data)
            continue 
        #Separate and store the necessary data
        name=name.split('"')
        icon = icon.split('"')
        currency['name']=name[3]
        currency[icon[1]]=icon[3] 
        #buy and sell the currencys links
        currency['buy']=f'https://nobitex.ir/{symbol[i]}/'
        #online chart code for displaying for all currencies
        chart='<html lang="en"><head> <meta charset="UTF-8"> <meta http-equiv="X-UA-Compatible" content="IE=edge">  <meta name="viewport" content="width=device-width, initial-scale=1.0"> <title>Document</title></head><body><div class="tradingview-widget-container"><div id="tradingview_0f939"></div><div class="tradingview-widget-copyright">'
        chart+=f'<a href="https://www.tradingview.com/symbols/{symbol[i]}USDT/?exchange=BINANCE"'
        chart+='rel="noopener" target="_blank"></a></div> <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script><script type="text/javascript">  new TradingView.widget({ "autosize": true,' 
        chart+=f'"symbol":"BINANCE:{symbol[i]}USDT",'
        chart+=' "interval": "D",  "timezone": "Etc/UTC",  "theme": "light",  "style": "3",  "locale": "en",  "toolbar_bg": "#f1f3f6",  "enable_publishing": false,  "hide_top_toolbar": true,  "save_image": false,  "container_id": "tradingview_0f939"} ); </script></div></body></html>'
        currency['chart']=chart
        currency['percent']=percent[i]

        informatin.append(currency) # store the currency data

def SaveJson():
    # sort and save information in JSON format file
    from operator import itemgetter
    a = sorted(informatin, key=itemgetter('percent'), reverse=True) 
    crypto['crypto']=a
    with open('data.json', 'w') as fp:
        json.dump(crypto, fp)