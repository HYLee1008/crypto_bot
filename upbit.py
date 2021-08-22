# import json
# import pandas as pd
# from datetime import datetime
# import pandas as pd
import pyupbit
import aiohttp


class myUpbit():
    def __init__(self, access_key, secret_key):
        self.wallet = pyupbit.Upbit(access_key, secret_key)

    def get_balance(self, ticker):
        """Show balance of single ticker

        Args:
            ticker (str): Single coin or KRW

        Returns:
            (float): Balance
        """
        return self.wallet.get_balance(ticker)

    def get_balances(self):
        """Show balance of entire wallet

        Returns:
            list(dict): Entire balance. list of dictionaries
        """
        return self.wallet.get_balances()

    def sell_limit_order(self, market, price, volume):
        """limit sell order

        Args:
            market (str): Single coin
            price (float): Order price
            volume (float): Order quantity

        Returns:
            (dict): Order result. Return None when fail
        """
        return self.wallet.sell_limit_order(market, price, volume)

    def sell_market_order(self, market, volume):
        """Market sell order

        Args:
            market (str): Simgel coin
            volume (float): Order qunatity

        Returns:
            (dict): Order result. Return None when fail
        """
        print(f"sell {market} !!!")
        return self.wallet.sell_market_order(market, volume)

    def buy_limit_order(self, market, price, volume):
        """limit buy order

        Args:
            market (str): Single coin
            price (float): Order price
            volume (float): Order quantity

        Returns:
            (dict): Order result. Return None when fail
        """
        return self.wallet.buy_limit_order(market, price, volume)

    def buy_market_order(self, market, volume):
        """Market buy order

        Args:
            market (str): Simgel coin
            volume (float): Order qunatity

        Returns:
            (dict): Order result. Return None when fail
        """
        print(f'buy {market} !!!')
        return self.wallet.buy_market_order(market, volume)

    def get_order(self, ticker):
        """Return undone order list

        Args:
            ticker (str): Single ticker

        Returns:
            list(dict): list of undone order list
        """
        return self.wallet.get_order(ticker)

    def cancel_order(self, uuid):
        """Cancle order

        Args:
            uuid (str): single uuid

        Returns:
            (dict): State of the order. Return None when fail
        """
        return self.wallet.cancel_order(uuid)

    def get_chance(self, ticker):
        """[summary]

        Args:
            ticker ([type]): [description]

        Returns:
            [type]: [description]
        """
        return self.wallet.get_chance(ticker)

    def get_tickers(self, fiat='KRW'):
        """get every available market

        Args:
            fiat (str, optional): market type. Defaults to 'KRW'.

        Returns:
            (list): list of market
        """
        return pyupbit.get_tickers(fiat)


async def get_ohlcv(market, interval, count, interval_min=''):
    """get ohlcv dataframe with async-programming.

    Args:
        market (str): single market
        interval (str): ohlcv interval type. (minutes, days, weeks, months)
        count (str): Number of rows
        interval_min (str, optional): minute interval. Defaults to ''.

    Raises:
        Exception: interval_min not provided when interval is minutes

    Returns:
        (list[dict]): list of ohlcv dict
    """
    if interval == 'minute' and interval_min == '':
        raise Exception('minute interval is not provided.')

    url = "https://crix-api-endpoint.upbit.com/v1/crix/candles/" + \
        f"{interval}/{interval_min}?code=CRIX.UPBIT.{market}&count={count}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            return await res.json()


if __name__ == "__main__":
    access_key = 'XS5bMcecpljFvMJcQJxBkIK3a64Xw8VwQxcdrZWT'
    secret_key = '5M6DE5VRKUzFM237jVDFZcAQdVsPaZxrSzNXURbL'
    upbit = myUpbit(access_key, secret_key)

    print(upbit.get_chance('KRW-BTC'))
