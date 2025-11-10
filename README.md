面向金融的Python课程大作业项目 - 基于GPT-4的智能投资研究助手
## 项目简介

这是一个使用Python开发的智能投资研究助手，能够：

自动获取股票数据和财务信息

使用GPT-4模型进行深度分析

生成专业的投资分析报告（支持Markdown渲染）

提供文本和HTML两种格式的报告输出
## 功能特点

✅ 自动获取股票数据（使用AKShare）

✅ GPT-4智能分析

✅ Markdown格式报告渲染

✅ 生成文本和HTML格式报告

✅ 支持单股票和批量分析

✅ 完善的错误处理机制

✅ 交互式操作界面
## 项目结构

```text

financial_research_assistant/

│

├── config.py                 # 配置文件（在这里填API密钥）

├── data_fetcher.py          # 数据获取模块

├── llm_analyst.py           # GPT-4分析模块

├── report_generator.py      # 报告生成模块（支持Markdown渲染）

├── main.py                  # 主程序入口

├── requirements.txt         # 依赖库列表

└── README.md               # 项目说明

```
## 快速开始

### 1. 安装依赖

```bash

pip install -r requirements.txt

```
### 2. 配置API密钥

编辑 config.py 文件，填入你的API密钥：
```python

# ⚠️⚠️⚠️ 请在这里填写你的OpenAI API密钥 ⚠️⚠️⚠️

OPENAI_API_KEY = "sk-your-actual-api-key-here"  # 替换为你的真实API密钥
# 使用GPT-4模型

OPENAI_MODEL = "gpt-4"
```
### 3. 运行程序

```bash
python main.py
```
## 使用说明

1. **启动程序**后，选择分析模式：
 - 分析默认股票列表（平安银行、五粮液、贵州茅台）
 - 分析单个自定义股票
 - 批量分析自定义股票

2. **程序会自动**：
 - 获取股票数据和财务信息
 - 调用GPT-4进行深度分析
 - 生成专业的投资分析报告

3. **查看报告**：
 - 所有报告保存在 reports 目录
 - 包含文本格式（.txt）和HTML格式（.html）报告
 - HTML报告支持Markdown渲染，显示效果更佳
## 报告示例

生成的HTML报告包含：
 - 公司基本信息和股价数据
 - GPT-4的专业分析（使用Markdown格式）
 - 投资建议和风险提示
 - 美观的排版和样式
## 技术栈
 - **数据分析**: AKShare, Pandas
 - **AI分析**: OpenAI GPT-4 API
 - **报告生成**: Markdown渲染
 - **交互界面**: 命令行交互
## 注意事项
 - 请确保已安装所有依赖库
 - 使用前务必在config.py中配置正确的API密钥
 - 程序包含完善的错误处理，API不可用时使用模拟数据
 - 生成的投资报告仅供参考，不构成投资建议
## 开发团队

本项目为面向金融的Python课程大作业开发，展示了Python在金融数据分析与AI应用中的强大能力。
