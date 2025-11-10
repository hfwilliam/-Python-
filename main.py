#!/usr/bin/env python3
"""
智能投研助手 - 主程序
面向金融的Python课程大作业项目
"""

import time
import pandas as pd
from typing import List, Dict, Any
from datetime import datetime

# 导入自定义模块
from config import OPENAI_API_KEY, DEFAULT_STOCKS
from data_fetcher import FinancialDataFetcher
from llm_analyst import OpenAIAnalyst
from report_generator import ReportGenerator

class InvestmentResearchAssistant:
    """
    智能投研助手主类
    协调数据获取、分析和报告生成
    """
    
    def __init__(self):
        print("🚀 初始化智能投研助手...")
        
        # 初始化各个模块
        self.data_fetcher = FinancialDataFetcher()
        self.analyst = OpenAIAnalyst()
        self.report_generator = ReportGenerator()
        
        # 存储分析历史
        self.analysis_history = []
        
        print("✅ 智能投研助手初始化完成!")
        # 修复这里：确保report_generator有output_dir属性
        if hasattr(self.report_generator, 'output_dir'):
            print(f"📝 配置信息: OpenAI模型={self.analyst.model}, 输出目录={self.report_generator.output_dir}")
        else:
            print(f"📝 配置信息: OpenAI模型={self.analyst.model}, 输出目录=reports")
    
    def analyze_single_stock(self, symbol: str, company_name: str = "") -> Dict[str, Any]:
        """分析单个股票"""
        print(f"\n{'='*50}")
        print(f"开始分析: {symbol} {company_name}")
        print(f"{'='*50}")
        
        start_time = time.time()
        
        try:
            # 1. 获取数据
            raw_data = self.data_fetcher.get_all_data(symbol)
            
            # 2. AI分析
            analysis_result = self.analyst.analyze_company(
                raw_data["company_data"],
                raw_data["financial_data"], 
                raw_data["price_data"],
                raw_data["macro_data"]
            )
            
            # 3. 构建结果
            result = {
                "symbol": symbol,
                "company_name": company_name or raw_data["company_data"].get("company_name", ""),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "raw_data": raw_data,
                "analysis": analysis_result
            }
            
            # 4. 生成报告
            text_report_path = self.report_generator.generate_text_report(result)
            html_report_path = self.report_generator.generate_html_report(result)
            
            result["report_paths"] = {
                "text": text_report_path,
                "html": html_report_path
            }
            
            # 5. 保存到历史
            self.analysis_history.append(result)
            
            elapsed_time = time.time() - start_time
            print(f"✅ 分析完成! 耗时: {elapsed_time:.2f}秒")
            
            return result
            
        except Exception as e:
            print(f"❌ 分析 {symbol} 时出现错误: {str(e)}")
            return {
                "symbol": symbol,
                "company_name": company_name,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "error": str(e),
                "analysis": f"分析过程中出现错误: {str(e)}"
            }
    
    def analyze_multiple_stocks(self, stock_list: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """批量分析多个股票"""
        print(f"\n📊 开始批量分析 {len(stock_list)} 个股票...")
        
        results = []
        for i, stock in enumerate(stock_list, 1):
            print(f"\n[{i}/{len(stock_list)}] 分析 {stock['symbol']} - {stock.get('name', '')}")
            
            result = self.analyze_single_stock(stock['symbol'], stock.get('name', ''))
            results.append(result)
            
            # 添加延迟，避免请求过于频繁
            if i < len(stock_list):
                print("⏳ 等待3秒后继续...")
                time.sleep(3)
        
        # 生成对比报告
        if len(results) > 1:
            self.report_generator.generate_comparison_report(results)
        
        return results
    
    def display_analysis_result(self, result: Dict[str, Any]):
        """在控制台显示分析结果"""
        print(f"\n{'='*60}")
        print(f"📊 分析报告 - {result['symbol']} {result.get('company_name', '')}")
        print(f"{'='*60}")
        print(f"⏰ 分析时间: {result['timestamp']}")
        
        # 显示关键数据
        if 'raw_data' in result and 'price_data' in result['raw_data']:
            price_data = result['raw_data']['price_data']
            if 'latest_price' in price_data:
                change_symbol = "📈" if price_data.get('price_change_percent', 0) >= 0 else "📉"
                print(f"{change_symbol} 最新股价: {price_data['latest_price']} "
                      f"({price_data.get('price_change_percent', 0)}%)")
        
        print(f"\n🤖 AI分析摘要:")
        print("-" * 40)
        
        # 显示分析结果的前几行作为摘要
        analysis_lines = result['analysis'].split('\n')
        for line in analysis_lines[:10]:  # 只显示前10行
            if line.strip():
                print(f"  {line}")
        
        if len(analysis_lines) > 10:
            print("  ... (详细内容请查看报告文件)")
        
        print(f"\n💾 报告文件:")
        if 'report_paths' in result:
            for report_type, path in result['report_paths'].items():
                if path:
                    print(f"  {report_type.upper()}报告: {path}")
        
        print(f"{'='*60}\n")
    
    def run_interactive_mode(self):
        """交互式运行模式"""
        print("\n🎮 进入交互式分析模式")
        print("你可以选择:")
        print("1. 分析默认股票列表")
        print("2. 分析单个自定义股票")
        print("3. 批量分析自定义股票")
        print("4. 退出")
        
        while True:
            try:
                choice = input("\n请选择操作 (1-4): ").strip()
                
                if choice == "1":
                    # 分析默认股票
                    self.analyze_multiple_stocks(DEFAULT_STOCKS)
                    break
                    
                elif choice == "2":
                    # 分析单个股票
                    symbol = input("请输入股票代码 (如: 000001): ").strip()
                    name = input("请输入公司名称 (可选，按回车跳过): ").strip()
                    result = self.analyze_single_stock(symbol, name)
                    self.display_analysis_result(result)
                    break
                    
                elif choice == "3":
                    # 批量分析自定义股票
                    stocks = []
                    print("请输入股票信息 (输入空行结束):")
                    while True:
                        symbol = input("股票代码: ").strip()
                        if not symbol:
                            break
                        name = input("公司名称: ").strip()
                        stocks.append({"symbol": symbol, "name": name})
                    
                    if stocks:
                        self.analyze_multiple_stocks(stocks)
                    else:
                        print("❌ 未输入任何股票")
                    break
                    
                elif choice == "4":
                    print("👋 再见!")
                    return
                    
                else:
                    print("❌ 无效选择，请重新输入")
                    
            except KeyboardInterrupt:
                print("\n👋 用户中断操作，再见!")
                return
            except Exception as e:
                print(f"❌ 发生错误: {str(e)}")

def main():
    """主函数"""
    print("=" * 60)
    print("            🤖 智能投研助手 v1.0")
    print("        面向金融的Python课程大作业")
    print("=" * 60)
    
    # 检查API密钥配置
    if not OPENAI_API_KEY or OPENAI_API_KEY == "sk-your-openai-api-key-here":
        print("❌ 警告: 请先在 config.py 中配置正确的OpenAI API密钥!")
        print("   当前将使用模拟分析结果进行演示")
    
    # 创建助手实例
    assistant = InvestmentResearchAssistant()
    
    # 运行交互模式
    assistant.run_interactive_mode()
    
    # 显示分析历史摘要
    if assistant.analysis_history:
        print(f"\n📈 本次会话共完成 {len(assistant.analysis_history)} 个分析")
        print("所有报告已保存至 'reports' 目录")

if __name__ == "__main__":
    main()