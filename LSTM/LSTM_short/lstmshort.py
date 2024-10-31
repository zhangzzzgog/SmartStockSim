import os
import pandas            as pd
import numpy             as np
import tensorflow        as tf
import matplotlib.pyplot as plt

from numpy.random          import seed
from keras.models          import Sequential
from keras.layers          import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
from datetime              import timedelta


class LSTM_ShortModel:
    def __init__(self, args):
        self.args = args
    
    def train(self):
        args = self.args

        # GPU调用
        gpus = tf.config.list_physical_devices("GPU")
        if gpus:
            tf.config.experimental.set_memory_growth(gpus[0], True)  #设置GPU显存用量按需使用
            tf.config.set_visible_devices([gpus[0]],"GPU")
        # 中文支持
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        # 固定种子确保结果尽可能重现
        seed(1)
        tf.random.set_seed(1)

        # 命令行参数
        stock_name = args.stock_name
        input_dir = args.input_dir
        n_epochs = args.n_epochs

        if stock_name is not None:
            model_path = args.model_path + stock_name + "_short"
            output_dir = args.output_dir + stock_name + "_short_predict.csv"
        else:
            # 去掉前面的目录部分
            base_name = os.path.basename(input_dir)  # 获取文件名部分
            model_path = args.model_path + base_name[:-4] + "_short"
            output_dir = args.output_dir + base_name.replace(".csv", "_short_predict.csv")


        # 读取数据
        data = pd.read_csv(input_dir, parse_dates=['d'])
        data.set_index("d", inplace=True)

        # 选取需要预测的特征（收盘价 'c'）
        closing_data = data[['c']]

        # 归一化数据
        scaler = MinMaxScaler(feature_range=(0, 1))
        closing_data_scaled = scaler.fit_transform(closing_data)

        # 创建训练集，设定每隔30分钟的窗口大小
        def create_dataset(dataset, window_size=6):
            X, y = [], []
            for i in range(len(dataset) - window_size - 6):
                X.append(dataset[i:(i + window_size), 0])
                y.append(dataset[i + window_size:i + window_size + 6, 0])  # 预测未来30分钟
            return np.array(X), np.array(y)

        window_size = 6  # 30分钟窗口（每5分钟一个点，6个点共30分钟）
        X, y = create_dataset(closing_data_scaled, window_size)

        # 数据集重塑为LSTM输入格式
        X = np.reshape(X, (X.shape[0], X.shape[1], 1))

        # 构建LSTM模型
        model = Sequential([
            LSTM(units=50, return_sequences=True, input_shape=(X.shape[1], 1)),
            Dropout(0.2),
            LSTM(units=50, return_sequences=False),
            Dropout(0.2),
            Dense(units=6)  # 预测未来30分钟的6个数据点
        ])

        # 编译模型
        model.compile(
            optimizer=tf.keras.optimizers.Adam(
                learning_rate=0.009, 
                beta_1=0.9, 
                beta_2=0.999, 
                epsilon=1e-07
            ), 
            loss='mean_squared_error'
        )

        # 训练模型
        model.fit(X, y, epochs=n_epochs, batch_size=32)
        model.summary()

        # 保存模型，保存为tensorflow格式
        model.save(model_path)

        # 使用当天数据预测未来30分钟数据
        def predict_next_30_minutes(current_data, model, scaler, window_size=6):
            # 提取最后一个窗口的数据
            last_window = current_data[-window_size:]
            last_window_scaled = scaler.transform(last_window)

            # 重塑为模型输入
            last_window_scaled = np.reshape(last_window_scaled, (1, window_size, 1))

            # 预测
            predicted_scaled = model.predict(last_window_scaled)
            predicted = scaler.inverse_transform(predicted_scaled)
            return predicted.flatten()

        # 使用当天已有数据来进行预测
        today_data = closing_data
        predicted_next_30_min = predict_next_30_minutes(today_data.values, model, scaler)

        # 保存预测结果
        future_time_index = [today_data.index[-1] + timedelta(minutes=5 * i) for i in range(1, 7)]
        prediction_df = pd.DataFrame({
            'datetime': future_time_index,
            'price': predicted_next_30_min
        })
        print(prediction_df)
        # 保存为 CSV 文件
        # index=False 不保存行索引
        prediction_df.to_csv(output_dir, index=False)
        

        '''
        # 可视化
        plt.plot(predicted_next_30_min, color='green', label='Predicted Closing Price')
        plt.title('Predicted Future Stock Price (Next 30 mins)')
        plt.xlabel('5mins per step')
        plt.ylabel('Stock Closing Price')
        plt.legend()
        plt.show()
        '''
