from LSTM_short.lstmshort import LSTM_ShortModel
import argparse

parser = argparse.ArgumentParser(description='Short term LSTM model training and predict')

# 股票名称（可选）
parser.add_argument("--stock_name", type=str, default=None)
# 输入股票数据文件路径，要求大于=6条数据
parser.add_argument("--input_dir", type=str, default="stockdata/430017_5m_0903only.csv")
# 输出预测数据文件夹路径
parser.add_argument("--output_dir", type=str, default="predictions/")
# 模型保存路径
parser.add_argument("--model_path", type=str, default="lstm_models/")
# 模型迭代轮次
parser.add_argument("--n_epochs", type=int, default=20)


args = parser.parse_args()
print("Args in training:")
print(args)


lstm_model = LSTM_ShortModel(args)
lstm_model.train()