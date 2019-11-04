from pyccmap import API

__all__ = ["Cex"]

class Cex(API):
    url = "https://cex.io/api/"
    def values(self, coins: tuple = ("LTC", "XRP", "DASH", "BCH", "ETH")):
        output = {}
        for coin in map(str.upper, coins):
            try:
                output[coin] = {k: (float(v) if (isinstance(v, str) and (v.isdecimal() or v.isdigit())) else v) for k, v in self.get(f"ticker/{coin}/USD").json().items()}
            except Exception as e:
                raise e
        return output
