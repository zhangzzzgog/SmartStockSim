## Introduction
Our module offers 2 kinds of LSTM model for long term(a month) and short term(30 mins) stock prices predicting.
Predicted prices are close prices.
## Quick Start
To run the python scripts, an envirorment with pyhton 3.8 is required. 
You can use conda to manage environments, install miniconda:
```
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh
~/miniconda3/bin/conda init bash
~/miniconda3/bin/conda init zsh
```
Reboot the terminal, then use conda to create a new envirorment:
```
conda create --name lstm_predict python=3.8
conda activate lstm_predict
cd LSTM
pip install -r requirements.txt
```

You can train with default dataset simply by running:
```
python lstm.py 
```
LSTM model is saved in tensorflow format.

Comments in parserlong.py provide all the args and details, check it to set a more flexible training strategy.

## About the Dataset
Long term LSTM uses stock data output from the module of crawler, file can be checked at `stockdata/430017_last_6_months.csv`

Short term LSTM's dataset is fetched from a stock prices api: `http://api.mairui.club/hszbl/fsjy/430017/5m/b997d4403688d5e66a`,
'430017' means stock code and '5m' stands the time step is 5 mins between each item.

Mainly difference between the 2 dataset is the format of time, Long one is `date`, the short one is `datetime`
