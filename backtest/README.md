# 量化交易回测系统 API
基于均线交叉策略的股票回测系统，提供收益率和权益计算功能。

## 安装依赖
```bash
pip install -r requirements.txt
```
## 准备数据
目前是在backtest/目录下放置股票数据文件,格式示例：  
date|close  
2023-01-03,15.20

(由于平安银行数据好像没办法通过yfinance获取，因此设置文件。若需要每股数据，则可以取消注释backtester.py以下代码并稍作修改)  
```python
#stock= yf.Ticker(self.symbol)
#stock_historical = stock.history(start=self.start_date, end=self.end_date, interval="1d")
#data=stock_historical
```
## 启动服务
```bash
python app.py
```
## API文档
POST /backtest 设置回测参数

请求示例：
```
curl -X POST http://localhost:5000/backtest \
-H "Content-Type: application/json" \
-d '{
  "symbol": "appl",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31",
  "capital": 1000000,
  "position_ratio": 0.2
  "slippage":0.0001
}'
```
| 参数 | 类型 | 默认值 | 描述 |
|-------|-------|-------|-------|
| symbol | string |- | 股票简称 |
| start_date | string |-| 格式：YYYY-MM-DD |
| start_date | string |-| 格式：YYYY-MM-DD |
| capital | float |1e6| 初始资金| 
| position_ratio | float |0.2 | 每次建仓资金比例|
| slippage | float |0.0001| 交易滑点比例|

GET /results 获取回测结果

```
当日总权益：[...]
总收益率: -3.04%
最终总权益: 969,628.68 元
```

## 项目结构
```
backtest/
├── app.py                 # Flask应用入口
├── backtester.py          # 回测引擎核心
├── strategy.py            # 交易策略实现
├── 000001历史数据.csv      # 示例数据文件
├── test_backtester.py     # 测试api
├── requirements.txt       # 依赖清单
├── requirements1.txt      # 所有依赖清单
└── README.md              # 本文档
```