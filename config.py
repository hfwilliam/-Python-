"""
配置文件 - 请在此处填写你的API密钥和其他配置
"""

# ⚠️⚠️⚠️ 请在这里填写你的OpenAI API密钥 ⚠️⚠️⚠️
OPENAI_API_KEY = "XXX"  # 替换为你的实际API密钥

# 其他配置项
OPENAI_MODEL = "gpt-4"  # 可以选择 "gpt-4" 或 "gpt-3.5-turbo"
REQUEST_TIMEOUT = 30  # API请求超时时间（秒）
MAX_TOKENS = 2000     # 生成文本的最大长度

# 数据源配置
DEFAULT_STOCKS = [
    {"symbol": "000001", "name": "平安银行"},
    {"symbol": "000858", "name": "五粮液"},
    {"symbol": "600519", "name": "贵州茅台"}
]