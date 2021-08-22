import asyncio
import pyupbit
import datetime
import pandas as pd
from upbit import get_ohlcv


async def volatility_breakout(ticker, wallet, ma_days=5, k=0.5):
    """Larry Williams volatility breakout strategy

    Args:
        ticker (str): Single coin
        wallet (myUpbit): myUpbit class
        k (float, optional): constant k. Defaults to 0.5.
    """
    async def get_target_price():
        data = await get_ohlcv(ticker, 'days', 2)

        today_open = data[1]['tradePrice']
        yesterday_high = data[1]['highPrice']
        yesterday_low = data[1]['lowPrice']
        target = today_open + (yesterday_high - yesterday_low) * k

        return target

    async def prev_ma():
        data = await get_ohlcv(ticker, 'days', ma_days)
        df = pd.DataFrame(data)

        close = df['tradePrice']
        ma = close.rolling(window=5).mean()

        return ma[1], df['tradePrice'][0]

    now = datetime.datetime.now()
    mid = datetime.datetime(now.year, now.month, now.day) \
        + datetime.timedelta(days=1)
    target_price = await get_target_price()

    while True:
        try:
            now = datetime.datetime.now()
            if mid < now < mid + datetime.delta(second=5):
                target_price = await get_target_price()
                mid = datetime.datetime(now.year, now.month, now.day) \
                    + datetime.timedelta(days=1)
                order = wallet.sell_market_order(ticker)
                while order is None:
                    order = wallet.sell_market_order(ticker)

            current_price, ma = await prev_ma()
            if (current_price > target_price) and (current_price > ma):
                krw = wallet.get_balance('KRW')
                orderbook = pyupbit.get_orderbook(ticker)
                sell_price = orderbook['asks'][0]['price']
                unit = krw * 0.5 / float(sell_price)
                order = wallet.buy_market_order(ticker, unit)
                while order is None:
                    order = wallet.buy_market_order(ticker, unit)

        except Exception as e:
            print(f'Error {e}!!!')

        await asyncio.sleep(0.5)
