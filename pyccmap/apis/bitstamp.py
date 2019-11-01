from pyccmap import API

__all__ = ["BitStamp"]

class BitStamp(API):
    # Set the API URL
    url = "https://www.bitstamp.net/api/v2/"
    def values(self):
        output = {}
        response = self.get("trading-pairs-info/")
        if response.status_code is not 200:
            response.raise_for_status()
        pairs = response.json()
        for pair in pairs:
            symbol = pair["url_symbol"]
            if symbol.endswith("usd"):
                coin = symbol.strip("usd").upper()
                output[coin] = {key: value for key, value in filter(lambda x: x[0] in ("ask", "bid", "last"), self.get(f"/ticker/{symbol}/").json().items())}
        return output
