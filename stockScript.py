import requests
import sys
import time



def foo(n):
    #tied to multiprocessing
    x = getRecommendationMean()
    volatility()
    y = getPrice()

    return float(x) , float(y)

def volatility():
    url = "https://finance.yahoo.com/quote/" + TICKER_SYMBOL + "?p=" + TICKER_SYMBOL
    r = requests.get(url).text
    x = r.find("FIFTY_TWO_WK_RANGE-value")
    start = x+44
    end = x+61
    fin = r[start:end].replace("<", "")
    fin = fin.replace("/", "")
    fin = fin.replace("t", "")
    fin = fin.replace("d", "")
    fin = fin.replace(">", "")
    fin = fin.replace(",", "")
    # print(fin)
    middle = fin.find(" - ");
    recomendation = str(truncate(float(fin[middle+3:])- float(fin[:middle]),2))
    #print(recomendation)
    changePerc = (float(fin[middle+3:])- float(fin[:middle]))/ float(fin[:middle])
    # print("Change" + str(changePerc))
    if changePerc > .75:
        lowRisk.append((TICKER, fin[middle+3:]))
    if changePerc < .75 and changePerc > .35:
        medRisk.append((TICKER, fin[middle+3:]))
    if changePerc < .35:
        highRisk.append((TICKER, fin[middle+3:]))
        
def getPrice():
    url = "https://finance.yahoo.com/quote/" + TICKER_SYMBOL + "/analysts?p=" + TICKER_SYMBOL
    r = requests.get(url).text
    r = requests.get(url).text
    x = r.find("regularMarketPrice")

    return x
      
def getRecommendationMean():
    url = "https://finance.yahoo.com/quote/" + TICKER_SYMBOL + "/analysts?p=" + TICKER_SYMBOL
    r = requests.get(url).text
    x = r.find("recommendationMean")
    # print(r[x+27:x+30])

    return r[x+27:x+30]

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

sdict = [("Google","GOOG"), ("Go Pro", "GPRO"), ("Snap INC", "Snap"), ("Disney", "DIS"), ("Amazon", "AMZN"), ("NVIDIA", "NVDA"), ("Apple", "AAPL"), ("Microsoft", "MSFT"), ("Facebook", "FB"), ("Twitter", "TWTR"), ("Tesla", "TSLA"), ("Netflix", "NFLX")]
highRisk = [];
medRisk = [];
lowRisk = [];
TICKER_SYMBOL = "DIS"
reccomdation = []
TICKER = "Disney"
sice = []
for i in sdict:
    # print(i[0])
    TICKER_SYMBOL = i[1]
    TICKER = i[0]
    num = foo(10)
    recc = num[0]
    current = num[1]
    reccomdation.append((i[0],num,recc));

sice = sorted(reccomdation, key=lambda tup: tup[1])

print (sice)
