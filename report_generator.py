import os
from datetime import datetime
import markdown
from typing import Dict, List, Any

class ReportGenerator:
    """报告生成类 - 支持Markdown渲染"""
    
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        print(f"✅ 报告生成器初始化完成，输出目录: {output_dir}")
    
    def _render_markdown_to_html(self, markdown_text: str) -> str:
        """将Markdown文本渲染为HTML"""
        try:
            html_content = markdown.markdown(markdown_text)
            return html_content
        except Exception:
            return f"<pre>{markdown_text}</pre>"
    
    def generate_text_report(self, result: Dict[str, Any]) -> str:
        """生成文本格式报告"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"research_report_{result['symbol']}_{timestamp}.txt"
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write("           智能投研助手 - 投资分析报告\n")
                f.write("=" * 60 + "\n\n")
                
                f.write("📋 基本信息\n")
                f.write("-" * 30 + "\n")
                f.write(f"股票代码: {result['symbol']}\n")
                f.write(f"公司名称: {result.get('company_name', 'N/A')}\n")
                f.write(f"分析时间: {result['timestamp']}\n\n")
                
                f.write("🤖 AI分析结果\n")
                f.write("-" * 30 + "\n")
                f.write(result['analysis'])
                f.write("\n\n")
                
                f.write("=" * 60 + "\n")
                f.write("数据来源: AKShare | 分析模型: GPT-4\n")
                f.write("注: 本报告仅供参考，不构成投资建议\n")
                f.write("=" * 60 + "\n")
            
            print(f"✅ 文本报告已保存至: {filepath}")
            return filepath
        except Exception as e:
            print(f"❌ 生成文本报告失败: {str(e)}")
            return ""
    
    def generate_html_report(self, result: Dict[str, Any]) -> str:
        """生成HTML格式报告 - 支持Markdown渲染"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"research_report_{result['symbol']}_{timestamp}.html"
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            analysis_html = self._render_markdown_to_html(result['analysis'])
            
            html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>投资分析报告 - {result['symbol']}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f7fa;
            padding: 20px;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 20px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .basic-info {{
            background: #f8f9fa;
            padding: 20px;
            border-bottom: 1px solid #e9ecef;
        }}
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }}
        .info-item {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }}
        .analysis-section {{
            padding: 30px;
        }}
        .analysis-content {{
            background: #f8f9fa;
            padding: 25px;
            border-radius: 8px;
            border-left: 4px solid #28a745;
            margin-top: 15px;
        }}
        .analysis-content h1, .analysis-content h2, .analysis-content h3 {{
            margin: 20px 0 10px 0;
            color: #2c3e50;
            border-bottom: 1px solid #eaecef;
            padding-bottom: 5px;
        }}
        .analysis-content p {{ margin: 10px 0; }}
        .analysis-content ul, .analysis-content ol {{
            margin: 10px 0 10px 20px;
        }}
        .analysis-content li {{ margin: 5px 0; }}
        .analysis-content blockquote {{
            border-left: 4px solid #dfe2e5;
            padding-left: 15px;
            margin: 15px 0;
            color: #6a737d;
        }}
        .analysis-content code {{
            background: #f6f8fa;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        .footer {{
            background: #343a40;
            color: white;
            text-align: center;
            padding: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 智能投研助手</h1>
            <p>投资分析报告 - 基于GPT-4</p>
        </div>
        
        <div class="basic-info">
            <div class="info-grid">
                <div class="info-item"><strong>股票代码</strong><br>{result['symbol']}</div>
                <div class="info-item"><strong>公司名称</strong><br>{result.get('company_name', 'N/A')}</div>
                <div class="info-item"><strong>分析时间</strong><br>{result['timestamp']}</div>
            </div>
        </div>
        
        <div class="analysis-section">
            <h2>🤖 AI分析结果</h2>
            <div class="analysis-content">{analysis_html}</div>
        </div>
        
        <div class="footer">
            <p>数据来源: AKShare | 分析模型: GPT-4</p>
            <p>注: 本报告仅供参考，不构成投资建议</p>
        </div>
    </div>
</body>
</html>"""
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"✅ HTML报告已保存至: {filepath}")
            return filepath
        except Exception as e:
            print(f"❌ 生成HTML报告失败: {str(e)}")
            return ""