from pyccmap import API

__all__ = ["Cex"]

class Cex(API):
    url = "https://cex.io/api/"
    def values(self, coins: tuple = ("LTC", "XRP", "DASH", "BCH", "ETH")):
        output = {}
        for coin in coins:
            try:
                output[coin] = {key: value for key, value in filter(lambda x: x[0] in ("ask", "bid", "last"), self.get(f"ticker/{coin}/USD").json().items())}
            except Exception as e:
                pass
        return output
