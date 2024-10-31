import os
import pandas            as pd
import tensorflow        as tf  
import numpy             as np
import matplotlib.pyplot as plt

from numpy.random          import seed
from numpy                 import array
from sklearn               import metrics
from sklearn.preprocessing import MinMaxScaler
from keras.models          import Sequential
from keras.layers          import Dense,LSTM,Bidirectional
from datetime              import datetime, timedelta


class LSTM_LongModel:
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
        # ====================================
        #      选择模型：
        #            1: 单层 LSTM
        #            2: 多层 LSTM
        #            3: 双向 LSTM
        # ====================================
        stock_name = args.stock_name
        model_type = args.model_type
        input_dir = args.input_dir
        n_timestamp  = args.n_timestamp    # 时间戳
        n_epochs     = args.n_epochs    # 训练轮数

        if stock_name is not None:
            model_path = args.model_path + stock_name
            output_dir = args.output_dir + stock_name + "_predict.csv"
        else:
            # 去掉前面的目录部分
            base_name = os.path.basename(input_dir)  # 获取文件名部分
            model_path = args.model_path + base_name[:-4] + "_short"
            output_dir = args.output_dir + base_name.replace(".csv", "_short_predict.csv")
    


        # 检测模型类型参数是否错误
        if model_type < 1 or model_type > 3:
            print("Model type range from 1 to 3!")
            return
        
        # 数据集加载
        data = pd.read_csv(input_dir)  # 读取股票文件
        data_rows, data_columns = data.shape

        # 数据集划分
        training_set = data.iloc[0:data_rows - 300, 1:2].values  
        test_set     = data.iloc[data_rows - 300:, 1:2].values


        # 数据归一化，范围是0到1
        sc  = MinMaxScaler(feature_range=(0, 1))
        training_set_scaled = sc.fit_transform(training_set)
        testing_set_scaled  = sc.transform(test_set) 


        # 取前 n_timestamp 天的数据为 X；n_timestamp+1天数据为 Y。
        def data_split(sequence, n_timestamp):
            X = []
            y = []
            for i in range(len(sequence)):
                end_ix = i + n_timestamp
                
                if end_ix > len(sequence)-1:
                    break
                    
                seq_x, seq_y = sequence[i:end_ix], sequence[end_ix]
                X.append(seq_x)
                y.append(seq_y)
            return array(X), array(y)

        X_train, y_train = data_split(training_set_scaled, n_timestamp)
        X_train          = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)

        X_test, y_test   = data_split(testing_set_scaled, n_timestamp)
        X_test           = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)


        # 建构 LSTM模型
        if model_type == 1:
            # 单层 LSTM
            model = Sequential()
            model.add(LSTM(units=50, activation='relu',
                        input_shape=(X_train.shape[1], 1)))
            model.add(Dense(units=1))
        if model_type == 2:
            # 多层 LSTM
            model = Sequential()
            model.add(LSTM(units=50, activation='relu', return_sequences=True,
                        input_shape=(X_train.shape[1], 1)))
            model.add(LSTM(units=40, activation='relu', return_sequences=True))
            model.add(LSTM(units=50, activation='relu'))
            model.add(Dense(1))
        if model_type == 3:
            # 双向 LSTM
            model = Sequential()
            model.add(Bidirectional(LSTM(50, activation='relu'),
                                    input_shape=(X_train.shape[1], 1)))
            model.add(Dense(1))
        """
        if model_type == 4:
            # 原来的多层 LSTM
            model = Sequential()
            model.add(LSTM(units=50, activation='relu', return_sequences=True,
                        input_shape=(X_train.shape[1], 1)))
            model.add(LSTM(units=50, activation='relu', return_sequences=True))
            model.add(LSTM(units=50, activation='relu'))
            model.add(Dense(1))
        """
            
        model.summary() # 输出模型结构


        # 编译（激活）模型
        # 该应用只观测loss数值，不观测准确率，所以删去metrics选项，一会在每个epoch迭代显示时只显示loss值
        model.compile(
            optimizer=tf.keras.optimizers.Adam(
                learning_rate=0.009, 
                beta_1=0.9, 
                beta_2=0.999, 
                epsilon=1e-07
            ),
            loss='mean_squared_error'
        )  # 损失函数用均方误差


        # 训练模型
        history = model.fit(X_train, y_train, 
                            batch_size=64, 
                            epochs=n_epochs, 
                            validation_data=(X_test, y_test), 
                            validation_freq=1)                  #测试的epoch间隔数
        model.summary()

        # 保存模型，保存为tensorflow格式
        model.save(model_path) 
        

        # -----注释部分用于评估模型预测效果-----
        """
        # 绘制loss图
        plt.plot(history.history['loss']    , label='Training Loss')
        plt.plot(history.history['val_loss'], label='Validation Loss')
        plt.title('Training and Validation Loss')
        plt.legend()
        plt.show()

        # 用于评估的预测
        predicted_stock_price = model.predict(X_test)                        # 测试集输入模型进行预测
        predicted_stock_price = sc.inverse_transform(predicted_stock_price)  # 对预测数据还原---从（0，1）反归一化到原始范围
        real_stock_price      = sc.inverse_transform(y_test)# 对真实数据还原---从（0，1）反归一化到原始范围


        # 画出真实数据和预测数据的对比曲线
        plt.plot(real_stock_price, color='red', label='Stock Price')
        plt.plot(predicted_stock_price, color='blue', label='Predicted Stock Price')
        plt.title('Stock Price Prediction')
        plt.xlabel('Time')
        plt.ylabel('Stock Price')
        plt.legend()
        plt.show()

        # 评估预测效果
        # MSE  ：均方误差    ----->  预测值减真实值求平方后求均值
        # RMSE ：均方根误差  ----->  对均方误差开方
        # MAE  ：平均绝对误差----->  预测值减真实值求绝对值后求均值
        # R2   ：决定系数，可以简单理解为反映模型拟合优度的重要的统计量
        # 详细介绍可以参考文章：https://blog.csdn.net/qq_38251616/article/details/107997435
        MSE   = metrics.mean_squared_error(predicted_stock_price, real_stock_price)
        RMSE  = metrics.mean_squared_error(predicted_stock_price, real_stock_price)**0.5
        MAE   = metrics.mean_absolute_error(predicted_stock_price, real_stock_price)
        R2    = metrics.r2_score(predicted_stock_price, real_stock_price)

        print('均方误差: %.5f' % MSE)
        print('均方根误差: %.5f' % RMSE)
        print('平均绝对误差: %.5f' % MAE)
        print('R2: %.5f' % R2)
        """

        # 将所有的历史数据（训练集+测试集）拼接起来作为整体数据
        all_data = np.concatenate((training_set_scaled, testing_set_scaled), axis=0)

        # 获取最后 n_timestamp 天的历史数据作为预测的起点
        last_sequence = all_data[-n_timestamp:]  # 从整体数据中取最后 n_timestamp 天

        # 预测未来 30 天的数据
        future_days = args.future_days  # 预测未来30天
        predicted_future = []

        # 循环预测未来 30 天的股票价格
        for _ in range(future_days):
            # 使用模型预测下一个值
            next_price = model.predict(last_sequence.reshape(1, n_timestamp, 1))  # reshape to 3D

            # 将预测的值保存
            predicted_future.append(next_price[0][0])

            # 更新输入序列：移除序列中的最早一天，添加新预测的值
            last_sequence = np.append(last_sequence[1:], next_price, axis=0)

        # 将预测的未来30天数据反归一化
        predicted_future = np.array(predicted_future).reshape(-1, 1)
        predicted_future = sc.inverse_transform(predicted_future)

        # 以.csv格式保存预测数据
        lastdate_string = data.iloc[-1][0]
        lastdate = datetime.strptime(lastdate_string, "%Y-%m-%d")
        datelist = []
        pricelist = []

        for days in range(1, predicted_future.size):
            nowdate = lastdate + timedelta(days)
            datelist.append(nowdate.strftime("%Y-%m-%d"))
            pricelist.append(predicted_future[days][0])

        # 创建 DataFrame
        output_data = pd.DataFrame({
            "date": datelist,
            "price": pricelist
        })
        # 保存为 CSV 文件
        # index=False 不保存行索引
        output_data.to_csv(output_dir, index=False)

        """
        # 画出未来30天的预测值
        plt.plot(predicted_future, color='green', label='Predicted Future Stock Price')
        plt.title('Predicted Future Stock Price (Next 30 Days)')
        plt.xlabel('Days')
        plt.ylabel('Stock Price')
        plt.legend()
        plt.show()
        """
