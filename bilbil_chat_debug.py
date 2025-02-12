import os

import openai
import requests

openai.api_key = "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"


os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'

proxies = {
    'http': 'http://127.0.0.1:your_proxy_port',
    'https': 'http://127.0.0.1:your_proxy_port'
}

# 创建一个请求会话并设置代理
session = requests.Session()
session.proxies.update(proxies)

def chat_with_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"An error occurred: {e}"

prompt = "告诉我一个有趣的笑话。"
response = chat_with_gpt(prompt)
print(response)