from pyupbit import WebSocketManager

if __name__ == "__main__":
    wm = WebSocketManager("ticker", ["KRW-BTC", "KRW-XRP"])
    for i in range(10):
        data = wm.get()
        print(data)
    wm.terminate()
