import alpaca_trade_api as tradeapi
import pandas as pd
import time

# 设置API密钥和秘密密钥
API_KEY = 'PKAZBO9BQ86OOVMOAPJP'
API_SECRET = '9p52uhbX4atgTzXsAhR1HsGMa8WWcmjLarfIIf23'
BASE_URL = 'https://paper-api.alpaca.markets'  # 使用模拟交易API

# 初始化API连接
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

# 交易参数
symbol = 'AAPL'
buy_threshold = 0.05
sell_threshold = -0.05
quantity = 10


# 获取历史数据
def get_historical_data(symbol, start_date, end_date):
    barset = api.get_barset(symbol, 'day', start=start_date, end=end_date)
    return barset[symbol]


# 计算动量指标
def calculate_momentum(data):
    data['pct_change'] = data['close'].pct_change(periods=10)
    return data


# 获取最新的账户状态
def get_account():
    return api.get_account()


# 执行交易
def trade(action, symbol, quantity):
    if action == 'buy':
        api.submit_order(symbol=symbol, qty=quantity, side='buy', type='market', time_in_force='gtc')
    elif action == 'sell':
        api.submit_order(symbol=symbol, qty=quantity, side='sell', type='market', time_in_force='gtc')


# 交易策略实现
def momentum_strategy():
    # 获取历史数据
    data = get_historical_data(symbol, '2022-01-01', '2024-01-01')
    df = pd.DataFrame({
        'close': [bar.c for bar in data]
    })
    df = calculate_momentum(df)

    # 最新的动量值
    latest_momentum = df['pct_change'].iloc[-1]
    print(f'Latest momentum: {latest_momentum}')

    # 获取当前持仓
    positions = api.list_positions()
    current_position = 0
    for position in positions:
        if position.symbol == symbol:
            current_position = int(position.qty)

    # 根据动量值执行交易
    if latest_momentum > buy_threshold and current_position == 0:
        print('Buying')
        trade('buy', symbol, quantity)
    elif latest_momentum < sell_threshold and current_position > 0:
        print('Selling')
        trade('sell', symbol, quantity)


# 运行策略
while True:
    try:
        print('Running momentum strategy')
        momentum_strategy()
        time.sleep(86400)  # 每天运行一次
    except Exception as e:
        print(f'Error: {e}')
        time.sleep(60)  # 如果发生错误，等待1分钟再尝试
