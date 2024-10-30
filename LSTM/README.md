## Introduction
Our module offers 2 kinds of LSTM model for long term(a month) and short term(30 mins) stock prices predicting.
Predicted prices are close prices.
## Quick Start
To run the python scripts, an envirorment with pyhton 3.8 is required. 
Then install packages:
```
pip install -r requirements.txt
```

You can train with default dataset simply by running:
```
python parserlong.py --stock_name 430017
```
LSTM model is saved in tensorflow format.

Comments in parserlong.py provide all the args and details, check it to set a more flexible training strategy.

## About the Dataset
Long term LSTM uses stock data output from the module of crawler, file can be checked at `stockdata/430017_last_6_months.csv`

Short term LSTM's dataset is fetched from a stock prices api: `http://api.mairui.club/hszbl/fsjy/430017/5m/b997d4403688d5e66a`,
'430017' means stock code and '5m' stands the time step is 5 mins between each item.

Mainly difference between the 2 dataset is the format of time, Long one is `date`, the short one is `datetime`
