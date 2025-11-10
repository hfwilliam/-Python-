import openai
from typing import Dict, Any
import json
import time
from config import OPENAI_API_KEY, OPENAI_MODEL, REQUEST_TIMEOUT, MAX_TOKENS

class OpenAIAnalyst:
    """
    OpenAI API分析类
    使用OpenAI GPT模型进行金融分析
    """
    
class OpenAIAnalyst:
    def __init__(self):
        # ⚠️ 修改这里：在初始化客户端时传入 base_url 参数
        self.client = openai.OpenAI(
            api_key=OPENAI_API_KEY,
            base_url="https://api.chatanywhere.tech/v1"  # 你指定的base_url
        )
        
        if not OPENAI_API_KEY or OPENAI_API_KEY == "sk-your-openai-api-key-here":
            print("❌ 警告: 请先在config.py中配置正确的OpenAI API密钥!")
        
        self.model = OPENAI_MODEL
        self.timeout = REQUEST_TIMEOUT
        self.max_tokens = MAX_TOKENS
        self.analysis_history = []
        print("✅ OpenAI分析器初始化完成")
    
    def analyze_company(self, company_data: Dict, financial_data: Dict, 
                       price_data: Dict, macro_data: Dict) -> str:
        """调用OpenAI进行公司分析"""
        
        print("🧠 正在使用OpenAI进行深度分析...")
        
        # 构建分析提示词
        prompt = self._build_analysis_prompt(company_data, financial_data, 
                                           price_data, macro_data)
        
        try:
            # 检查API密钥是否已配置
            if not OPENAI_API_KEY or OPENAI_API_KEY.startswith("sk-your-"):
                return self._get_mock_analysis()
            
            # 调用OpenAI API - 使用新版本的方式
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": """你是一名专业的金融分析师，擅长公司分析和投资价值评估。
                        请用专业、客观的态度进行分析，避免主观臆断。
                        分析要基于提供的数据，条理清晰，重点突出。"""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,  # 较低的温度值确保分析更加客观
                max_tokens=self.max_tokens,
                timeout=self.timeout
            )
            
            analysis_result = response.choices[0].message.content
            print("✅ OpenAI分析完成!")
            return analysis_result
            
        except openai.AuthenticationError:
            error_msg = "❌ OpenAI API认证失败：请检查API密钥是否正确配置"
            print(error_msg)
            return f"{error_msg}\n\n{self._get_mock_analysis()}"
            
        except openai.RateLimitError:
            error_msg = "❌ OpenAI API调用频率超限：请稍后重试或检查账户余额"
            print(error_msg)
            return f"{error_msg}\n\n{self._get_mock_analysis()}"
            
        except openai.APIError as e:
            error_msg = f"❌ OpenAI API错误: {str(e)}"
            print(error_msg)
            return f"{error_msg}\n\n{self._get_mock_analysis()}"
            
        except Exception as e:
            error_msg = f"❌ 分析过程中出现未知错误: {str(e)}"
            print(error_msg)
            return f"{error_msg}\n\n{self._get_mock_analysis()}"
    
    def _build_analysis_prompt(self, company_data: Dict, financial_data: Dict,
                             price_data: Dict, macro_data: Dict) -> str:
        """构建分析提示词"""
        
        # 格式化数据，确保可读性
        formatted_company_data = self._format_data(company_data)
        formatted_financial_data = self._format_data(financial_data)
        formatted_price_data = self._format_data(price_data)
        formatted_macro_data = self._format_data(macro_data)
        
        prompt = f"""
请基于以下提供的公司数据和市场环境，对该投资标的进行全面的专业分析。

【公司基本信息】
{formatted_company_data}

【财务指标】
{formatted_financial_data}

【股价表现】
{formatted_price_data}

【宏观经济环境】
{formatted_macro_data}

请从以下几个方面进行专业分析：

1. 公司基本面分析
   - 业务模式和竞争优势
   - 行业地位和发展前景

2. 财务健康状况评估
   - 盈利能力分析
   - 偿债能力评估
   - 成长性分析

3. 估值与技术面分析
   - 当前估值水平
   - 股价表现和技术指标

4. 宏观环境影响
   - 宏观经济对公司的影响

5. 综合投资建议
   - 投资亮点和风险提示
   - 具体的投资建议（买入/持有/卖出）

要求：
- 用中文回答，分析要客观专业
- 条理清晰，重点突出
- 基于数据说话，避免主观臆断
- 给出具体的理由和支持依据

请开始你的专业分析：
"""
        return prompt
    
    def _format_data(self, data: Dict) -> str:
        """格式化数据为可读字符串"""
        if not data:
            return "无数据"
        
        formatted_lines = []
        for key, value in data.items():
            if isinstance(value, dict):
                # 如果是嵌套字典，进一步格式化
                nested_str = self._format_data(value)
                formatted_lines.append(f"{key}:")
                for line in nested_str.split('\n'):
                    if line.strip():
                        formatted_lines.append(f"  {line}")
            else:
                formatted_lines.append(f"{key}: {value}")
        
        return '\n'.join(formatted_lines)
    
    def _get_mock_analysis(self) -> str:
        """获取模拟分析结果（当API调用失败时使用）"""
        return """
【模拟分析结果 - 实际分析需要配置正确的OpenAI API密钥】

基于提供的公司数据，以下是我的分析：

1. 公司基本面分析
   宁德时代作为全球领先的锂电池制造商，在新能源汽车行业具有重要地位。公司业务模式清晰，专注于动力电池系统和储能系统的研发、生产和销售。

2. 财务健康状况
   从财务指标来看，公司盈利能力强劲，营收和利润持续增长。负债率处于行业合理水平，现金流状况良好。

3. 估值与技术面分析
   当前估值水平需要结合行业PE和公司增长率来评估。股价表现受新能源汽车行业景气度影响较大。

4. 宏观环境影响
   全球碳中和政策推动新能源汽车行业发展，对公司业务形成长期利好。但需关注原材料价格波动和行业竞争加剧的风险。

5. 投资建议
   【综合建议】：长期看好，建议逢低布局
   【理由】：
   - 行业龙头地位稳固
   - 受益于新能源行业发展
   - 技术研发实力强劲
   【风险提示】：
   - 行业竞争加剧
   - 原材料价格波动
   - 技术路线变化风险

注：此为模拟分析，实际投资决策请咨询专业投资顾问。
"""

if __name__ == "__main__":
    # 测试OpenAI分析器
    analyst = OpenAIAnalyst()
    test_data = {
        "company_data": {"symbol": "000001", "name": "测试公司"},
        "financial_data": {"roe": 0.12, "eps": 2.5},
        "price_data": {"price": 50.0, "change": 1.5},
        "macro_data": {"cpi": 2.5}
    }
    result = analyst.analyze_company(**test_data)
    print("测试分析完成!")
    print(result[:200] + "...")  # 只打印前200字符