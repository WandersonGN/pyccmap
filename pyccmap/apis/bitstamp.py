from pyccmap import API

__all__ = ["BitStamp"]

class BitStamp(API):
    # Set the API URL
    url = "https://www.bitstamp.net/api/v2/"
    def values(self, coins: tuple = ()):
        coins = tuple(map(str.upper, coins))
        output = {}
        response = self.get("trading-pairs-info/")
        if response.status_code is not 200:
            response.raise_for_status()
        pairs = response.json()
        for pair in pairs:
            symbol = pair["url_symbol"]
            if symbol.endswith("usd"):
                coin = symbol.strip("usd").upper()
                if (coin in coins) or (not coins):
                    output[coin] = self.get(f"/ticker/{symbol}/").json()
        return output
