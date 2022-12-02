#python file to collect data and 
import HistoricalData 
#python file to save data(predicted values, charts, names,symbols,currencys icons) in json type file
import JSONData  

HistoricalData.scrapper()
JSONData.PredictAndCollectdata()
JSONData.SaveJson()

