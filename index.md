<img src="../main/img/algo_trading_logo.png" width=100 alt="logo">

*Nicolás M. Japas*

## Content
- [Project Description](#project-description)
- [Hypotheses / Questions](#hypotheses-questions)
- [Dataset](#dataset)
- [Cleaning](#cleaning)
- [Analysis](#analysis)
- [Model Training and Evaluation](#model-training-and-evaluation)
- [Conclusion](#conclusion)
- [Future Work](#future-work)
- [Workflow](#workflow)
- [Organization](#organization)
- [Links](#links)

## Project Description
The goal of the project was to reach an MVP for an automated trading platform using bots for buying and selling stocks and cryptocurrencies in real-time. I focused on Bitcoin but the general approach is valid for other instruments after introducing some adaptations. The project will be upscaled in the future. A SARIMAX model was used, and several 'exogenous' variables explored. I built two models, one for 1-hour charts and the other for 1-minute in real-time.

## Hypotheses / Questions
* How to make use of algorithms to predict the price of a stock or cryptocurrency?
* Relevant to anyone interested in trading or investing. 
* Which exogenous variables are relevant for bitcoin? Which parameters are well suited for the ARIMA model applied? Does the confidence in the predictions decay over time?

## Dataset
* The data was obtained from several sources. I used two APIs, one for bitcoin (Binance) and another for stocks (Alpha Vantage). I saved everything on .csv files but the code for fetching data is included in the respective modules ('cryptos' and 'stocks'). The code is modularized inside this files. This way, it will be easy to upscale the project to support other financial instruments.
* I also scraped data for Google Trends, Twitter, and others.

## Cleaning
To get the data was the main difficulty, as I had to adapt to several limitations. For example alpha vantage API has a limit on the amount of GETs available if the free account is used. The documentation of the Binance API is quite poor, although a wrapper was useful for that. To scrape the data about Twitter, Google and Marketcap of bitcoin I had to look carefully at the source code of the website (bitinfocharts dot com), as it was fairly hidden inside javascript code. After all that, a lot of work dealing with datetime indexes and frequencies (which introduce NaNs in the code when a certain time period is not in the original data). 

## Analysis
* Exploratory plotting, check for correlations, scatter, hist and combined plots.

<img src="../main/img/pairplot_.png" alt="Pairplot">
<img src="../main/img/j5_.png" alt="Scatter">
<img src="../main/img/j4_.png" alt="Scatter">

* Feature selection came in this case from BI, and knowing how bitcoin's movements are related with them. The plots and correlations were a confirmation. And the the model provided significant Pearson correlation coefficients in the diagnostics, further suggesting that the selected data was at least to some degree relevant.

## Model Training and Evaluation
* The data was scaled and split. I also used logarithmic transform.
* To get the parameters for the ARIMA model was tricky, it wasn't enough to use the popular AUTO-ARIMA module which provides the apparent better values for p, d and q. It uses the AIC results, but it took me some trial and error to get better results.
* For the real-time data, a simpler model was used, without exogenous variables. Only the endogenous.

## Conclusion
* I was able to generate predictions, both for the test values and for the unknown future (out-of-sample forecast).
* A web-socket was implemented to fetch data in real-time directly from Binance, one of the major exchanges in the world. It streams data straight to the program, which can be analyzed in real-time (see the module binance_web_socket).
* The features selected appear to be relevant. The model should be back-tested (not enough time) but appear to be a useful first approximation to an extremely complex problem.
<img src="../main/img/plotly.png" alt="Plotly">

## Future Work
This is going to be a commercial project in the future, deployed on a website where users will be able to create an account, log-in and set-up their bots to trade for them without the need of knowing anything about coding. The real-time fetching of data will be generalized, and more and more stocks and cryptocurrencies will be available.

The connection with Binance API will enable the placement of real trades, automating the process for the user.

All the data which is now loaded from the disk has to be updated (after buffering) in real-time. For price, volume, etc. but also for Twitter, Google Trends, Marketcap, and other valuable data.

## Workflow
Get the data, build the model, plot the results. Iterate. Try more features, compare results. Iterate.

The model provides diagnostics such as:

<img src="../main/img/diagnostics_.png" alt="Diagnostics">

I also calculated Mean absolute percentage error, Root mean square error, Pearson product-moment correlation coefficients, and others.

But the best indicator would be a back-test, which wasn't able to complete due to time-constraints.

## Organization

No Trello nor Kanban used. Just a lot of work, dedication and passion.

Everything is more or less modularized so there are several notebooks, with 'main' as the one the be run. There are also versions of the notebooks in .py, because they are loaded from main as libraries.

There are several folders with data. The folder 'data' has BTCUSDT (Bitcoin), AMZN (Amazon) and GOOGL (Google) financial data. In 'project_files' are two files with the list of available stocks and cryptocurrencies (for future upscaling). In 'scrape_bitinfocharts' are data files scraped, about Twitter, Google Trends, etc. This structure will be improved later.

## Links
https://github.com/nicojapas/algorithmic_trading

