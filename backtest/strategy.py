import pandas as pd

class MovingAverageCrossStrategy:
    def __init__(self, short_window=12, long_window=26):
        """
        初始化均线交叉策略
        :param short_window: 短期均线周期 (默认12日)
        :param long_window: 长期均线周期 (默认26日)
        """
        self.short_window = short_window
        self.long_window = long_window
        self.name = f"MA{short_window}_{long_window}_Cross"
        self.position = 0  # 0表示空仓，1表示持仓

    def generate_history_signals(self, data):
        """
        生成交易信号
        :param data: 包含股票价格数据的DataFrame (需包含'close'列)
        :return: 添加了信号列的DataFrame
        """
        # 计算均线
        data['short_ma'] = data['close'].rolling(window=self.short_window, min_periods=1).mean()
        data['long_ma'] = data['close'].rolling(window=self.long_window, min_periods=1).mean()
        
        # 初始化信号列
        data['signal'] = 0
        
        # 生成交易信号 (1: 买入, -1: 卖出, 0: 无操作)
        for i in range(1, len(data)):
            # 金叉条件：短期均线上穿长期均线且当前无持仓
            if (data['short_ma'].iloc[i] > data['long_ma'].iloc[i] and 
                data['short_ma'].iloc[i-1] <= data['long_ma'].iloc[i-1] and
                self.position == 0):
                data.loc[data.index[i], 'signal']= 1
                self.position = 1
                
            # 止损条件：收盘价跌破长期均线且当前持仓
            elif (data['close'].iloc[i] < data['long_ma'].iloc[i] and 
                  self.position == 1):
                 data.loc[data.index[i], 'signal']= -1
                 self.position = 0
        
        return data
    
    #实时交易 可注释掉
    def get_signal(self, current_data):
        """
        获取当前时刻的交易信号 (用于实时交易)
        :param current_data: 当前时刻的数据 (包含short_ma和long_ma)
        :return: 1 (买入), -1 (卖出), 0 (无操作)
        """
        if not hasattr(self, 'prev_short_ma'):
            self.prev_short_ma = current_data['short_ma']
            self.prev_long_ma = current_data['long_ma']
            return 0
            
        # 检查交叉
        if (current_data['short_ma'] > current_data['long_ma'] and 
            self.prev_short_ma <= self.prev_long_ma and
            self.position == 0):
            self.prev_short_ma = current_data['short_ma']
            self.prev_long_ma = current_data['long_ma']
            return 1
            
        # 检查止损
        elif (current_data['close'] < current_data['long_ma'] and 
              self.position == 1):
            self.prev_short_ma = current_data['short_ma']
            self.prev_long_ma = current_data['long_ma']
            return -1
            
        self.prev_short_ma = current_data['short_ma']
        self.prev_long_ma = current_data['long_ma']
        return 0