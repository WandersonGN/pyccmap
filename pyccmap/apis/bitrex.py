from pyccmap import API

__all__ = ["BitRex"]

class BitRex(API):
    url = "https://bittrex.com/api/v1.1/"
    def values(self, coins: tuple = ("LTC", "XRP", "DASH", "BCH", "ETH")):
        output = {}
        for coin in map(str.upper, coins):
            try:
                output[coin] = {key.lower(): value for key, value in self.get(f"public/getticker?market=USD-{coin}").json()["result"].items()}
            except Exception as e:
                pass
        return output
