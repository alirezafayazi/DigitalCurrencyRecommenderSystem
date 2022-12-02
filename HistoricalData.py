from cryptocmd import CmcScraper # To collect data
import os # To make folder
import pandas as pd # To manage dataframes
import currences # Python file that contains symbols and identifiers of digital currencies
symbol=currences.symbol.copy()
symbol.append('USDT')
#Scrapper is a function for collect historical datadatas
def scrapper():
    try:
        # Make data folder if it doesn't exist
        os.mkdir('data')
    except:
        #if data directory exists then do nothing
        pass
    #Collect data for each symbols
    for i in range(len(symbol)):
        print('*'*(i+1), f' {i+1} : collect {symbol[i]} data ','*'*(i+1))
        scraper=CmcScraper(symbol[i])
        headers, data = scraper.get_data()
        info=pd.DataFrame(data, columns=headers)

        print('** The data was downloaded **')
        info=info.set_index("Date")
       
        try:
            #Download data from the beginning of 2018 and save it in the data floder
            info = info.loc[:"31-12-2017"]
            print('** Saving Data ** \n\n')
            info.to_csv(f'data/{symbol[i]}data.csv')
        except:
            #data beginning after of 2018 so save it
            print('** Saving Data ** \n\n')
            info.to_csv(f'data/{symbol[i]}data.csv')
