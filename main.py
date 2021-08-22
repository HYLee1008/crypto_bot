import asyncio
from upbit import myUpbit
from upbit_tactics import volatility_breakout


class Client:
    def __init__(self, access_key, secret_key):
        self.ub = myUpbit(access_key, secret_key)
        self.loop = asyncio.get_event_loop()

    async def func(self, market):
        await volatility_breakout(market, self.ub)

    async def _gather(self, coins_list):
        await asyncio.gather(
            *[self.func(c) for c in coins_list]
            )

    def run(self):
        coins_list = self.ub.get_tickers()

        return self.loop.run_until_complete(
            self._gather(coins_list)
            )


def main():
    access_key = 'XS5bMcecpljFvMJcQJxBkIK3a64Xw8VwQxcdrZWT'
    secret_key = '5M6DE5VRKUzFM237jVDFZcAQdVsPaZxrSzNXURbL'

    client = Client(access_key, secret_key)
    client.run()


if __name__ == "__main__":
    main()
