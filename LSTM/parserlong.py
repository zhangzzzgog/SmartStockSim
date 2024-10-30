from LSTM_long.lstmlong import LSTM_LongModel
import argparse

parser = argparse.ArgumentParser(description='Long term LSTM model training and predict')

# 股票名称（可选）
parser.add_argument("--stock_name", type=str, default=None)
# 模型类型，可选1到3
parser.add_argument("--model_type", type=int, default=2)
# 输入股票数据文件路径，要求大于300条数据
parser.add_argument("--input_dir", type=str, default="stockdata/430017_last_6_months.csv")
# 输出预测数据文件夹路径
parser.add_argument("--output_dir", type=str, default="predictions/")
# 模型保存路径
parser.add_argument("--model_path", type=str, default="lstm_models/")
# 数据集划分窗口，默认前40天为训练集，后1天为测试集
parser.add_argument("--n_timestamp", type=int, default=40)
# 模型迭代轮次
parser.add_argument("--n_epochs", type=int, default=30)
# 预测未来天数
parser.add_argument("--future_days", type=int, default=30)


args = parser.parse_args()
print("Args in training:")
print(args)


lstm_model = LSTM_LongModel(args)
lstm_model.train()