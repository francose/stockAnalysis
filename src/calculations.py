import globalAttribute as gb

def sma(data, window):
    weight = gb.np.repeat(1.0, window)/ window
    avg = gb.np.convolve(data, weight, mode='valid')
    # print("SMA:", avg)
    return avg


def ema(data, window):
    weight = gb.np.exp(gb.np.linspace(-1. , 0. ,window ))
    weight /=  weight.sum()
    avg = gb.np.convolve(data, weight, mode='full')[:len(data)]
    avg[:window] = avg[window]
    return avg


def discreteDiff(obj: gb.List[float]) -> gb.List[float]:
    series = gb.pd.Series(obj)
    return series.diff(periods=14).dropna()

#reading data function, is just method that calucates the mean of the data and returns the value. Thought we need to manually pass the datafile.
def readData():
    with gb.pd.option_context('display.max_rows', 100, 'display.max_columns', 100):
        rawdata = gb.pd.read_json(gb.PATH+"AMZN/AMZN"+".json")
        df = gb.pd.DataFrame(rawdata)
        # By replacing all the commas in number we can convert all the data point in to a float number type example: float(df['Close'][0].replace(",", ""))
        data = [float(df['Close'][i].replace(",", "")) for i in range(
            0, len(df['Close'].sort_values(ascending=True)))]
        #for both functions we pass the data as an array and set the window (period of 10)
        return data
        
        
def RSI(period=4):
    data = readData()
    e = ema(data, period)
    deltas = gb.np.diff(e)
    newArry = deltas[:period + 1]
    up = newArry[newArry >= 0].sum()/period
    down = -newArry[newArry < 0].sum() / period
    relativeStrenght = up/down
    rsi = gb.np.zeros_like(e)
    rsi[:period] = 100. - 100. / (1.+ relativeStrenght)
    for i in range(period, len(e)):
        delta = deltas[i-1] 
        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta
        up = (up*(period-1) + upval)/period
        down = (down*(period-1) + downval)/period
        rs = up//down
        rsi[i] = 100. - 100./(1.+rs)
    return rsi


def macd(x=readData(), slow=25, fast=12):
    emaFast = ema(x, fast) 
    emaSlow = ema(x, slow)
    print(emaFast, emaSlow, emaFast - emaSlow)
    return emaFast, emaSlow, emaFast - emaSlow

   




