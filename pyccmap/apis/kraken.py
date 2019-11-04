from pyccmap import API

__all__ = ["Kraken"]

class Kraken(API):
    url = "https://api.kraken.com/0/public/"
    def values(self):
        output = {s.strip("USD")[1 if s[0] is "X" else 0: -1 if s.endswith("ZUSD") else 5]:
                  dict(zip(("ask", "bid", "last", "volume", "vwavg", "num_trades", "low", "high", "open"),
                           map(lambda x: float(k.get(x)[0]), "abcvptlho")))
                  for s, k in self.get("Ticker?pair=ETHUSD,XRPUSD,BCHUSD,LTCUSD").json()["result"].items()}
        return output
