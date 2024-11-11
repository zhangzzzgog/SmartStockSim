from lstmlong_newsAndtime import LSTM_LongModel
from eval_news import Eval_Module
import argparse

parser = argparse.ArgumentParser(description='Long term LSTM model training and predict')

# 股票名称（可选）
parser.add_argument("--stock_name", type=str, default="430017")
# 模型类型，可选1到3
parser.add_argument("--model_type", type=int, default=2)
# 输入股票数据文件路径
parser.add_argument("--input_dir", type=str, default="stockdata/430017_2024_year.csv")
# 输出预测数据文件夹路径
parser.add_argument("--output_dir", type=str, default="predictions/")
# 模型保存路径
parser.add_argument("--model_path", type=str, default="lstm_models/")
# 数据集划分窗口，默认前10天为训练集，后1天为测试集
parser.add_argument("--n_timestamp", type=int, default=20)
# 模型迭代轮次，默认30次
parser.add_argument("--n_epochs", type=int, default=30)
# 预测未来天数
parser.add_argument("--future_days", type=int, default=30)
# 测试集数据数目，默认最近60天为测试集
parser.add_argument("--n_test", type=int, default=40)


# 新闻评估依赖的公司简介
parser.add_argument("--inf_dir", type=str, default="news/430017inf.txt")
# 对应的新闻信息
parser.add_argument("--news_dir", type=str, default="news/430017news.csv")


args = parser.parse_args()
print("Args in training:")
print(args)


print("Now starting news evaluation programs.")
eval = Eval_Module(args)
eval.evaluate()

print("Now starting price prediction programs.")
lstm_model = LSTM_LongModel(args)
lstm_model.train()