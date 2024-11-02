import os
import pandas as pd
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from numpy.random import seed
from numpy import array
from sklearn import metrics
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
from datetime import datetime, timedelta


class LSTM_LongModel:
    def __init__(self, args):
        self.args = args

    def train(self):
        args = self.args

        # GPU调用
        gpus = tf.config.list_physical_devices("GPU")
        if gpus:
            tf.config.experimental.set_memory_growth(gpus[0], True)
            tf.config.set_visible_devices([gpus[0]], "GPU")

        # 中文支持
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

        # 固定种子确保结果尽可能重现
        seed(1)
        tf.random.set_seed(1)

        # 命令行参数
        input_dir = args.input_dir
        n_timestamp = args.n_timestamp
        n_epochs = args.n_epochs
        future_days = args.future_days

        # 数据集加载
        data = pd.read_csv(input_dir)  # 读取股票文件
        data['time'] = pd.to_datetime(data['time'])  # 转换时间格式
        data = data.sort_values(by='time')  # 按时间排序

        # 按 stock_code 分组
        grouped = data.groupby('stock_code')

        # 逐组处理
        for stock_code, group in grouped:
            print(f"Processing stock code: {stock_code}")

            # 获取价格数据
            prices = group['price'].values
            data_rows = len(prices)

            # 检查数据量
            if data_rows < 300:
                print(f"Not enough data for stock code {stock_code}, skipping.")
                continue

            # 划分训练集和测试集
            training_set = prices[:data_rows - 300]
            test_set = prices[data_rows - 300:]

            # 数据归一化
            sc = MinMaxScaler(feature_range=(0, 1))
            training_set_scaled = sc.fit_transform(training_set.reshape(-1, 1))
            testing_set_scaled = sc.transform(test_set.reshape(-1, 1))

            # 数据分割函数
            def data_split(sequence, n_timestamp):
                X, y = [], []
                for i in range(len(sequence)):
                    end_ix = i + n_timestamp
                    if end_ix > len(sequence) - 1:
                        break
                    seq_x, seq_y = sequence[i:end_ix], sequence[end_ix]
                    X.append(seq_x)
                    y.append(seq_y)
                return array(X), array(y)

            X_train, y_train = data_split(training_set_scaled, n_timestamp)
            X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)

            X_test, y_test = data_split(testing_set_scaled, n_timestamp)
            X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

            # 构建 LSTM 模型
            model = Sequential()
            model.add(LSTM(units=50, activation='relu', input_shape=(X_train.shape[1], 1)))
            model.add(Dense(1))

            # 编译模型
            model.compile(optimizer='adam', loss='mean_squared_error')
            model.fit(X_train, y_train, batch_size=64, epochs=n_epochs, validation_data=(X_test, y_test))

            # 预测未来数据
            all_data = np.concatenate((training_set_scaled, testing_set_scaled), axis=0)
            last_sequence = all_data[-n_timestamp:]
            predicted_future = []

            for _ in range(future_days):
                next_price = model.predict(last_sequence.reshape(1, n_timestamp, 1))
                predicted_future.append(next_price[0][0])
                last_sequence = np.append(last_sequence[1:], next_price, axis=0)

            # 反归一化和保存结果
            predicted_future = sc.inverse_transform(np.array(predicted_future).reshape(-1, 1))

            # 保存预测结果
            output_data = pd.DataFrame({
                'date': [group['time'].iloc[-1] + timedelta(days=i) for i in range(1, future_days + 1)],
                'predicted_price': predicted_future.flatten()
            })

            output_dir = f"{args.output_dir}/{stock_code}_predictions.csv"
            output_data.to_csv(output_dir, index=False)
            print(f"Predictions saved for stock code: {stock_code}")


# 示例用法
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Long term LSTM model training and predict')

    # 股票名称（可选）
    parser.add_argument("--stock_name", type=str, default=None)
    # 模型类型，可选1到3
    parser.add_argument("--model_type", type=int, default=2)
    # 输入股票数据文件路径，要求大于300条数据
    parser.add_argument("--input_dir", type=str, default="stockdata/stock.csv")
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
