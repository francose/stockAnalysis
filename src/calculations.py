import globalAttribute as gb

def sma(data, window):
    weight = gb.np.repeat(1.0, window)/ window
    avg = gb.np.convolve(data, weight, mode='valid')
    # print("SMA:", avg)
    return avg


def ema(data, window):
    weight = gb.np.exp(gb.np.linspace(-1. , 0. ,window ))
    weight /=  weight.sum()
    avg = avg = gb.np.convolve(data, weight, mode='full')[:len(data)]
    avg[:window] = avg[window]
    # print("EMA:",avg)
    return avg

#check series


def map_fl_list(fnc: gb.Callable, l: gb.List[float]) -> gb.List[float]:
    return [fnc(i) for i in l]

#reading data function, is just method that calucates the mean of the data and returns the value. Thought we need to manually pass the datafile.
def readData():
    with gb.pd.option_context('display.max_rows', 100, 'display.max_columns', 100):
        rawdata = gb.pd.read_json(gb.PATH+"AMZN/AMZN"+".json")
        df = gb.pd.DataFrame(rawdata)
        # By replacing all the commas in number we can convert all the data point in to a float number type example: float(df['Close'][0].replace(",", ""))
        data = [float(df['Close'][i].replace(",", "")) for i in range(
            0, len(df['Close'].sort_values(ascending=True)))]
        #for both functions we pass the data as an array and set the window (period of 10)
        sma(data, 10)
        ema(data, 10)
        



