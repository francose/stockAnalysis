This package includes Stock analysis tools and data extractor by using Yahoo Finance..

# Installation

- pip install -r requirements.txt


# Yahoo Finance S&P500 Extrator 

Method and Params: YahooFinance( Symbol , Range/Duration , interval )
Symbol is the stock ticker symbol, e.g. AAPL for Apple
range/duration is the desired range of the query, allowed parameters are [1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max]
interval is the desired interval of the quote, e.g. every 5 minutes, allowed parameters are [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3m]


# USAGE

yf = YahooFinance('AAPL', '1d', '1d')
quotes = yf.CompanyQuotes()
print(quotes)





# stockAnalysis
Exponential Moving Average and Simple Moving Average.

#SMA
A simple moving average (SMA) is simply the average of a set of data. nothing fancy. its just used to smooth out the data and reduce the overall noise and short term volatility of a stock.

goal: filter out for stocks that are above the 100 period SMA

mathematical formula: (example, 10 period average)
[sum of last 10 closing cost ÷ 10] = SMA

the simple moving average could be used in many different ways depending on the application. but mostly its used to reduce overall noise in a stock. its usually used with other indicators/ strategies.

note: different periods will show different long term/ short term trends.

attached is a photo that shows example of different moving averages. as we can see in the image, the shorter the period, the closer the SMA line wraps around the stock price. the larger the period, the smoother the SMA line is, showing very long term trends.
![SMA](https://github.com/francose/stockAnalysis/blob/master/src/public/SMA.png)



#EMA
We plot the EMA line on top of the stock price graph. The EMA acts as a signal of when to buy/sell.

The EMA line usually acts as a line of support or resistance for a stock price. meaning that the EMA is usually either below or above a stock price. when we see a crossover between the stock price and the EMA, we interpret that as a signal of when to buy or sell.

for example: the photo attached shows examples of when to buy and sell based on the EMA cross over

in mathematical terms, we are looking for the moment where stock value is less than, equal to, then greater than the EMA value. those three steps serve as an indication to look at the verification. look at next board for verification.

the moment where the stock price then dips below the ema line, thats an indication to sell/ stop losses.

The EMA (exponential moving average) is a type of moving average that puts more weight on more recent stock prices. which is unlike the simple moving average which views all the data equally. 

for example, we want to plot a 10 day EMA. The first data point of the EMA line is just the average of the past 10 days. (we have to start somewhere) so add the past 10 closing prices and divide by 10.  

(note: the unit for EMA is a candlestick. the closing price of the candlestick specifically. 1 candlestick is 1 period)

the next data point is where we calculate the EMA.

General Formula: 
[Closing price - EMA (previous day)] x constant  + EMA (previous day)

the constant =  [ 2 ÷ ( period + 1 ) ] = [2 ÷ (10 + 1)]= 2/11

Note: the first data point is just an average. so when we calculate the second data point, we use the first data point(the avg) as the previous day's EMA in the calculation. 

Refer to the google doc shared to see this calculation being used

![EMA](https://github.com/francose/stockAnalysis/blob/master/src/public/EMA.png)

Once we see a cross over with the stock price and the EMA, it not a guarantee that the stock price will continue to go up. its a strong suggestion that there might be a rise/ decline in stock price, but we need to be safe that a strong trend is present.

OPTION 1: MACD
to validate the EMA cross over, we need to look at the MACD indicator (moving average convergence divergence indicator). on the MACD indicator, we are also looking for a cross over. attached is a photo/example of this validation. after the MACD lines clearly cross, it's safer to say that the stock will either rise or fall depending on given circumstance.

note:
for more detailed description of the MACD indicator, look over at the MACD board.

OPTION 2: SMA
another way to validate the strength of the EMA signal/trend is to look at the simple moving average (SMA). the period of the SMA needs to be double the period of the EMA. if the EMA also crosses the SMA, then it's a verified buy or sell. check out the photo for an example.



![EMA2](https://github.com/francose/stockAnalysis/blob/master/src/public/EMA2.png)


#RSI
The equation for the RSI (Relative Strength Index) has multiple parts. be sure to refer to the google doc shared with you all to see how these calculations are used.

General Equation to calculate the RSI is:
RSI = 100 - [100/(1+RS)]

this equation results in a value ranging from 0-100. depending on the output of this equation, we can conclude whether or not to buy/sell. The default time frame is 14, as in 14 trading days or 14 candles.

when the RSI is below 25-30, its over sold and we can expect it to go up soon. when the RSI is above 70-80, it's over bought and we can expect it to go down.

calculating RS (Relative Strength):
RS = (Average Gain/Average Loss)

the most optimal or "default" period used in this calculation is a 14 candle stick period. to get the values for gain and loss, we subtract the last two closing prices from each other

Example
08/05/2018: closing price = $100
08/06/2018: closing price = $102

gain= $2
loss = $0

NOTE: if there is loss, we use the absolute value of the price. no negatives in this clculation

this simple calculation for the loss and gain is made for each day.

First value for AVG Gain or Loss:
to find the average gain, we sum up all the gains for the past 14 days, and divide by 14. (even if the gain for a day is 0, we still take that 0 into account when finding the average). same this for average loss. sum up all the losses, divide by 14.

^ NOTE: the paragraph above is used only for the first calculation of the average. after the first average gain or loss has been calculated, we move onto a new equation to calculate the rest of the average gains and losses.

AVG gain and loss 2.0
AVG Gain= [Previous avg Gain*(period-1)+current gain]/period

in our case, we should use a period of 14^

AVG Loss 2.0
AVG Loss= [Previous avg Loss*(period-1)+current Loss]/period

Overall Formula

RSI day 1: 
=100 - [100/(1+RS)]
= 100 - [100/(1+ (AVG gain/AVG Loss) ) ]

RSI day 2-today:
= 100 - [100/(1+RS)]
= 100-[100/(1+[Previous avg Gain*(period-1)+current gain]/period

NOTE: if this is getting confusing, refer to the google spread sheet and see the formula being used

again, the RS is found by dividing the AVG Gain by the AVG Loss
![RSI](https://github.com/francose/stockAnalysis/blob/master/src/public/RSI.png)

#MACD

Moving average convergence divergence (MACD) is a trend-following momentum indicator that shows the relationship between two moving averages of prices.

to calculate the MACD: 
we calculate the 12 period EMA of the stock, minus the 26 period EMA. these values are plotted and is called the MACD line. these points are plotted on a separate graph from that of the stock price.

after that, we calculate a 9 period EMA OF THE MACD LINE. this second line is called a "signal line" and is plotted on top of the MACD line.

General Formula: 
1) MACD
same concept discussed in the previous EMA board. the first point plotted uses an average, as discussed previously. same mathematical formula for calculating the EMA:

MACD = (12 period EMA - 26 peiod ema) =
[(closing price of last candle - previous EMA)(2/(12+1))+previous EMA] - [(closing price of last candle - previous EMA)(2/(26+1))+previous EMA]

2) signal line: 9 period ema of the MACD line.
[(last MACD value - previous EMA)*(2/(9+1))+previous EMA]
points are plotted on top of MACD line

we interpret the crossing of the MACD line and the signal line as validations of whether or buy or sell. look at photos attached for more detail
look at the photos attached in the EMA board for more verification photos with he MACD line.

![MACD](https://github.com/francose/stockAnalysis/blob/master/src/public/MACD.jpg)