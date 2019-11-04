from pyccmap import API

__all__ = ["BitFinex"]


class BitFinex(API):
    url = "https://api-pub.bitfinex.com/v2/"

    def values(self):
        output = {s[0][1:].strip("USD"): dict(zip(("bid", "bid_size", "ask", "ask_size", "daily_change",
                                                   "daily_change_perc", "last", "volume", "high", "low"), s[1:]))
                  for s in self.get('tickers?symbols=tBTCUSD,tLTCUSD,tETHUSD,tXRPUSD').json()}
        return output


