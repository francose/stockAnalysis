# stockAnalysis
Exponential Moving Average and Simple Moving Average.

#SMA
A simple moving average (SMA) is simply the average of a set of data. nothing fancy. its just used to smooth out the data and reduce the overall noise and short term volatility of a stock.

goal: filter out for stocks that are above the 180 period SMA

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
![EMA](https://github.com/francose/stockAnalysis/blob/master/src/public/EMA.png)
