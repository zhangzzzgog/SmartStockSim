import pandas as pd
import os
import http.client
import json
# ChatAnywhere API配置
API_URL = "api.chatanywhere.tech"
API_KEY = "sk-5HrY9HDaxQBx1dPDTUozf0mQ6MKwbUZlhZ8BjkRBeUia1QMb"  # 替换为你的API密钥

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

# 初始化消息历史
message_history = [
    {"role": "system", "content": "You are a helpful assistant."}
]

# 调用ChatAnywhere进行初始分析

# 定义文件路径
predictions_dir = 'predictions'
# 获取文件夹下所有 CSV 文件
csv_files = [f for f in os.listdir(predictions_dir) if f.endswith('.csv')]

# 循环读取每个 CSV 文件
for csv_file in csv_files:
    file_path = os.path.join(predictions_dir, csv_file)

    # 读取预测值
    predicted_data = pd.read_csv(file_path)
    if 'price' in predicted_data.columns:  # 确保 'price' 列存在
        predicted_prices = predicted_data['price'].values.flatten()

        # 创建分析提示
        prompt = f"根据以下预测的股票价格，分析其未来趋势并给出投资建议：{predicted_prices.tolist()}"
        message_history.append({"role": "user", "content": prompt})

        # 调用ChatAnywhere进行分析
        response = call_chat_anywhere(message_history)
        print(f"文件 {csv_file} 的助手建议:", response['choices'][0]['message']['content'])  # 输出建议

# 循环进行对话
while True:
    user_input = input("你想问些什么？ (输入 '退出' 结束对话)：")
    if user_input.lower() == '退出':
        print("对话结束。")
        break

    message_history.append({"role": "user", "content": user_input})  # 添加用户输入到消息历史
    response = call_chat_anywhere(message_history)  # 调用API
    print("助手:", response['choices'][0]['message']['content'])  # 输出助手的回复