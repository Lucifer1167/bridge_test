from backtester import Backtester

# 使用示例
if __name__ == "__main__":
    from strategy import MovingAverageCrossStrategy
    
    strategy = MovingAverageCrossStrategy(short_window=12, long_window=26)
    backtester = Backtester(
        strategy=strategy,
        symbol="000001.SZ",
        start_date="2024-01-17",
        end_date="2025-04-16"
    )
    
    portfolio_value,return_rate, final_equity = backtester.run_backtest()
    print(f"当日总权益{portfolio_value}")
    print(f"总收益率: {return_rate:.2%}")
    print(f"最终总权益: {final_equity:,.2f} 元")