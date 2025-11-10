import akshare as ak
import pandas as pd
from typing import Dict, List, Any
import time

class FinancialDataFetcher:
    """
    金融数据获取类
    使用AKShare获取股票数据、财务数据和宏观数据
    """
    
    def __init__(self):
        self.stock_data = {}
        print("✅ 数据获取器初始化完成")
    
    def get_company_profile(self, symbol: str) -> Dict[str, Any]:
        """获取公司基本信息"""
        print(f"📋 正在获取 {symbol} 的公司信息...")
        try:
            # 尝试多种方式获取公司信息
            stock_info = {}
            
            # 方法1: 获取股票基本信息
            try:
                stock_individual_info = ak.stock_individual_info_em(symbol=symbol)
                if not stock_individual_info.empty:
                    stock_info = stock_individual_info.iloc[0].to_dict()
            except:
                pass
            
            # 方法2: 获取公司概况
            try:
                stock_profile = ak.stock_profile_cninfo(symbol=symbol)
                if not stock_profile.empty:
                    stock_info.update(stock_profile.iloc[0].to_dict())
            except:
                pass
            
            # 如果都失败了，返回模拟数据（用于测试）
            if not stock_info:
                stock_info = {
                    "symbol": symbol,
                    "company_name": f"公司{symbol}",
                    "industry": "金融",
                    "listing_date": "2020-01-01",
                    "province": "北京",
                    "note": "模拟数据 - 实际数据获取失败"
                }
            
            return stock_info
            
        except Exception as e:
            print(f"❌ 获取公司信息失败: {str(e)}")
            return {"error": f"获取公司信息失败: {str(e)}", "symbol": symbol}
    
    def get_financial_indicators(self, symbol: str) -> Dict[str, Any]:
        """获取财务指标"""
        print(f"💰 正在获取 {symbol} 的财务指标...")
        try:
            # 获取财务指标数据
            financial_data = ak.stock_financial_analysis_indicator(symbol=symbol)
            
            if not financial_data.empty:
                # 获取最新一期的财务数据
                latest_data = financial_data.iloc[0].to_dict()
                return latest_data
            else:
                # 返回模拟财务数据
                return {
                    "earnings_per_share": 2.5,
                    "net_profit_margin": 0.15,
                    "roe": 0.12,
                    "debt_to_asset_ratio": 0.4,
                    "revenue_growth": 0.08,
                    "note": "模拟财务数据 - 实际数据获取失败"
                }
                
        except Exception as e:
            print(f"❌ 获取财务指标失败: {str(e)}")
            return {"error": f"获取财务指标失败: {str(e)}"}
    
    def get_stock_price(self, symbol: str, period: str = "daily") -> Dict[str, Any]:
        """获取股价数据"""
        print(f"📈 正在获取 {symbol} 的股价数据...")
        try:
            # 获取历史股价数据
            price_data = ak.stock_zh_a_hist(symbol=symbol, period=period, adjust="")
            
            if not price_data.empty and len(price_data) > 1:
                # 计算价格变动
                latest_price = price_data.iloc[-1]['收盘']
                prev_price = price_data.iloc[-2]['收盘']
                price_change = ((latest_price - prev_price) / prev_price) * 100
                
                return {
                    "latest_price": round(latest_price, 2),
                    "price_change_percent": round(price_change, 2),
                    "data_period": f"最近{len(price_data)}个交易日",
                    "volume": price_data.iloc[-1]['成交量']
                }
            else:
                # 返回模拟股价数据
                return {
                    "latest_price": 50.0,
                    "price_change_percent": 1.5,
                    "data_period": "模拟数据",
                    "volume": 1000000,
                    "note": "模拟股价数据 - 实际数据获取失败"
                }
                
        except Exception as e:
            print(f"❌ 获取股价数据失败: {str(e)}")
            return {"error": f"获取股价数据失败: {str(e)}"}
    
    def get_macro_data(self) -> Dict[str, Any]:
        """获取宏观经济数据"""
        print("🌍 正在获取宏观经济数据...")
        try:
            macro_data = {}
            
            # 获取CPI数据
            try:
                cpi_data = ak.macro_china_cpi()
                if not cpi_data.empty:
                    macro_data["cpi"] = cpi_data.iloc[-1].to_dict()
            except:
                macro_data["cpi"] = {"value": 2.5, "note": "模拟CPI数据"}
            
            # 获取PMI数据
            try:
                pmi_data = ak.macro_china_pmi()
                if not pmi_data.empty:
                    macro_data["pmi"] = pmi_data.iloc[-1].to_dict()
            except:
                macro_data["pmi"] = {"value": 50.5, "note": "模拟PMI数据"}
            
            return macro_data
            
        except Exception as e:
            print(f"❌ 获取宏观数据失败: {str(e)}")
            return {
                "cpi": {"value": 2.5, "note": "模拟数据"},
                "pmi": {"value": 50.5, "note": "模拟数据"},
                "error": f"获取宏观数据失败: {str(e)}"
            }
    
    def get_all_data(self, symbol: str) -> Dict[str, Any]:
        """获取所有相关数据"""
        print(f"\n🔍 开始收集 {symbol} 的完整数据...")
        
        company_data = self.get_company_profile(symbol)
        financial_data = self.get_financial_indicators(symbol)
        price_data = self.get_stock_price(symbol)
        macro_data = self.get_macro_data()
        
        # 等待一下，避免请求过于频繁
        time.sleep(1)
        
        return {
            "company_data": company_data,
            "financial_data": financial_data,
            "price_data": price_data,
            "macro_data": macro_data
        }

if __name__ == "__main__":
    # 测试数据获取
    fetcher = FinancialDataFetcher()
    test_data = fetcher.get_all_data("000001")
    print("测试数据获取完成!")