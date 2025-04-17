import pandas as pd
import numpy as np
from typing import Tuple
import yfinance as yf

# trade_cost: float = 0.0003
class Backtester:
    def __init__(self, strategy, symbol: str, start_date: str, end_date: str,
                 capital: float = 1e6, position_ratio: float = 0.2, 
                 slippage: float = 0.0001):
        """
        简化版回测引擎（专注收益率和总权益计算）
        :param strategy: 交易策略实例
        :param symbol: 股票代码 (e.g. '000001.SZ')
        :param start_date: 回测开始日期 (YYYY-MM-DD)
        :param end_date: 回测结束日期 (YYYY-MM-DD)
        :param capital: 初始资金 (默认100万)
        :param position_ratio: 每次开仓比例 (默认20%)
        :param slippage: 滑点比例 (默认0.01%)
        :param trade_cost: 交易手续费率 (默认0.03%) 无
        """
        self.strategy = strategy
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.initial_capital = capital
        self.position_ratio = position_ratio
        self.slippage = slippage
        #self.trade_cost = trade_cost

    def load_data(self) -> pd.DataFrame:
        """加载股票数据（示例需替换为真实数据源）"""
        # 实际数据接口 用appl做测试
        #stock= yf.Ticker(self.symbol)
        #stock_historical = stock.history(start=self.start_date, end=self.end_date, interval="1d")
        #data=stock_historical
        #需要跳过  data.set_index('date', inplace=True)

        #暂时只用本地上传csv文件
        data = pd.read_csv('000001历史数据.csv')
        data.set_index('date', inplace=True)
        return data

    def run_backtest(self) -> Tuple[float, float]:
        """
        运行回测并返回关键结果
        :return: (总收益率, 最终总权益)
        """
        data = self.load_data()
        data = self.strategy.generate_history_signals(data)  # 生成交易信号
        
        # 初始化账户状态
        cash = self.initial_capital
        shares = 0
        portfolio_value = [cash]  # 记录每日权益
        
        for date, row in data.iterrows():
            current_price = row['close']
            
            # 执行交易信号
            if row['signal'] > 0 and shares == 0:  # 买入
                trade_shares = int((cash * self.position_ratio) / (current_price * (1 + self.slippage)))
                cost = trade_shares * current_price * (1 + self.slippage)
                if cost <= cash:
                    shares = trade_shares
                    cash -= cost
                    
            elif row['signal'] < 0 and shares > 0:  # 卖出
                value = shares * current_price * (1 - self.slippage)
                cash += value
                shares = 0
            
            # 记录当日总权益
            portfolio_value.append(cash + shares * current_price)
        
        # 计算结果指标
        final_value = portfolio_value[-1]
        total_return = (final_value - self.initial_capital) / self.initial_capital
        
        return portfolio_value,total_return, final_value

# # 使用示例
# if __name__ == "__main__":
#     from strategy import MovingAverageCrossStrategy
    
#     strategy = MovingAverageCrossStrategy(short_window=12, long_window=26)
#     backtester = Backtester(
#         strategy=strategy,
#         symbol="000001.SZ",
#         start_date="2024-01-17",
#         end_date="2025-04-16"
#     )
    
#     portfolio_value,return_rate, final_equity = backtester.run_backtest()
#     print(f"每日金额{portfolio_value}")
#     print(f"总收益率: {return_rate:.2%}")
#     print(f"最终总权益: {final_equity:,.2f} 元")