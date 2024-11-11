# 本模块用于分析某支股票新闻信息对股票价格的attitude

import pandas as pd
import json
import re
import http.client


class Eval_Module:
    def __init__(self,args):
        self.args = args

    def evaluate(self):
        args = self.args

        # 命令行参数配置
        stock_name = args.stock_name
        inf_dir = args.inf_dir
        news_dir = args.news_dir
        input_dir = args.input_dir


        # ChatAnywhere API配置
        API_URL = "api.chatanywhere.tech"
        API_KEY = "sk-5HrY9HDaxQBx1dPDTUozf0mQ6MKwbUZlhZ8BjkRBeUia1QMb"  # 替换为你的API密钥

        # 定义调用ChatAnywhere API的函数
        def call_chat_anywhere(message_history):
            conn = http.client.HTTPSConnection(API_URL)
            payload = json.dumps({
                "model": "gpt-3.5-turbo",
                "messages": message_history
            })
            headers = {
                'Authorization': f'Bearer {API_KEY}',
                'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
                'Content-Type': 'application/json'
            }
            conn.request("POST", "/v1/chat/completions", payload, headers)
            res = conn.getresponse()
            data = res.read()
            return json.loads(data.decode("utf-8"))

        # 读取股价数据
        price_data = pd.read_csv(input_dir)
        price_data['date'] = pd.to_datetime(price_data['date'], errors='coerce')

        # 读取公司简介
        with open(inf_dir, 'r', encoding='utf-8') as f:
            company_info = f.read()

        # 读取新闻数据
        news_data = pd.read_csv(news_dir, encoding='utf-8')
        news_data['date'] = pd.to_datetime(news_data['date'], errors='coerce')


        # 调用ChatAnywhere API获取情绪分数的函数
        def get_attitude_score(news_content):
            # 设置聊天历史，向API请求情绪分数
            message_history = [
                {"role": "system", "content": f"你是一个金融分析助手，分析与{company_info}相关的新闻内容，要求只给出一个-100到100之间的整数，代表对股价的影响。返回的文本信息中除了该整数之外不得包含其他任何文本信息"},
                {"role": "user", "content": news_content}
            ]
            
            response = call_chat_anywhere(message_history)
            
            # 输出 API 返回的完整文本信息
            print("GPT API 返回的响应:", response)
            
            # 提取生成的文本
            try:
                attitude_text = response['choices'][0]['message']['content'].strip()
                print("提取的情绪文本:", attitude_text)  # 打印提取的情绪文本

                # 使用正则表达式提取分数
                match = re.search(r'[-+]?\d+', attitude_text)
                if match:
                    attitude_score = int(match.group())
                else:
                    print("未找到有效的情绪分数，默认情绪分数为 0")
                    attitude_score = 0
            except (KeyError, ValueError, IndexError):
                print("解析失败，默认情绪分数为 0")  # 如果解析失败，输出错误信息
                attitude_score = 0  # 如果解析失败则返回默认值 0
            
            return attitude_score

            
        # 初始化结果数据框
        results = pd.DataFrame(columns=['date', 'attitude'])

        # 为每个日期获取相应的新闻情绪分数
        for _, row in price_data.iterrows():
            date = row['date']
            daily_news = news_data[news_data['date'] == date]
            
            if not daily_news.empty:
                # 计算当日新闻的平均情绪分数
                attitudes = daily_news['news'].apply(get_attitude_score)
                average_attitude = int(attitudes.mean())
            else:
                average_attitude = 0  # 没有新闻时情绪分数为0

            # 添加到结果数据框
            # 使用 pd.concat 创建新行，并重新赋值给 results
            new_row = pd.DataFrame([{'date': date, 'attitude': average_attitude}])
            results = pd.concat([results, new_row], ignore_index=True)

        # 导出结果为CSV文件
        results.to_csv('attitude/' + stock_name + 'attitude.csv', index=False)
        print("情绪预测结果已保存至 attitude/" + stock_name + "attitude.csv")
