from flask import Flask, request, jsonify
from backtester import Backtester
from strategy import MovingAverageCrossStrategy


app = Flask(__name__)
backtester = None

# 是 Flask 框架中的一个路由装饰器，用于定义 API 端点（Endpoint）的行为。
@app.route('/backtest', methods=['POST'])
def set_backtest():
    global backtester
    params = request.json
    
    # 初始化回测器
    strategy = MovingAverageCrossStrategy(
        short_window=12,
        long_window=26
    )
    backtester = Backtester(
        strategy=strategy,
        **params
    )
    backtester.run_backtest()
    
    return jsonify({"status": "Backtest parameters set successfully"})

@app.route('/results', methods=['GET'])
def get_results():
    if not backtester:
        return jsonify({"error": "Backtest not initialized"}), 400
    
    results = {
        "total_return": backtester.total_return,
        "final_equity": backtester.final_equity,
        # 其他指标...
    }
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)