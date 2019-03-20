from globals import *


def sma(data, window):
    weight = np.repeat(1.0, window)/ window
    avg = np.convolve(data, weight, mode='valid')
    print(avg)
    return avg


def ema(data, window):
    weight = np.exp(np.linspace(-1. , 0. ,window ))
    weight /=  weight.sum()
    avg = avg = np.convolve(data, weight, mode='full')[:len(data)]
    avg[:window] = avg[window]
    print(avg)
    return avg
    


#reading data function, is just method that calucates the mean of the data and returns the value. Thought we need to manually pass the datafile.
def readData():
    with pd.option_context('display.max_rows', 100, 'display.max_columns', 100):
        rawdata = pd.read_json(PATH+"AMZN/AMZN"+".json")
        df = pd.DataFrame(rawdata)
        # By replacing all the commas in number we can convert all the data point in to a float number type example: float(df['Close'][0].replace(",", ""))
        data = [float(df['Close'][i].replace(",", "")) for i in range(
            0, len(df['Close'].sort_values(ascending=True)))]
        sma(data, 10)
        ema(data, 10)



