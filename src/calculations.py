import globalAttribute as gb

def sma(data, window):
    weight = gb.np.repeat(1.0, window)/ window
    avg = gb.np.convolve(data, weight, mode='valid')
    print("SMA:", avg)
    return avg


def ema(data, window):
    weight = gb.np.exp(gb.np.linspace(-1. , 0. ,window ))
    weight /=  weight.sum()
    avg = avg = gb.np.convolve(data, weight, mode='full')[:len(data)]
    avg[:window] = avg[window]
    print("EMA:",avg)
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
        
        
def RSI(period):
    data = readData()
    fncArry = [sma(data, 30), ema(data, 30)]
    for delta in fncArry:
            discreteDiff(delta)
            u = delta * 0
            d = u.copy()
            u[delta > 0] = delta[delta > 0]
            d[delta < 0] = -delta[delta < 0]
            u[u.index[period-1]] = gb.np.mean(u[:period])
            u = u.drop(u.index[:(period-1)])
            # first value is sum of avg losses
            d[d.index[period-1]] = gb.np.mean(d[:period])
            d = d.drop(d.index[:(period-1)])
            rs = gb.pd.stats.moments.ewma(u, com=period-1, adjust=False) / \
                gb.pd.stats.moments.ewma(d, com=period-1, adjust=False)
            return 100 - 100 / (1 + rs)

RSI(14)
   


