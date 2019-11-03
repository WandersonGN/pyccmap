from pyccmap import API

__all__ = ["Cex"]

class Cex(API):
    url = "https://cex.io/api/"
    def values(self, coins: tuple = ("LTC", "XRP", "DASH", "BCH", "ETH")):
        output = {}
        for coin in map(str.upper, coins):
            try:
                output[coin] = self.get(f"ticker/{coin}/USD").json()
            except Exception as e:
                raise e
        return output
