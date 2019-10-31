from re import search
from pprint import pprint
from requests import Session
from requests.exceptions import HTTPError
from urllib.parse import urljoin
from urllib3.util.url import parse_url, Url

class API(Session):
    # Pre-define the API URL
    url: str = ""
    def __init__(self):
        super().__init__()
        # Validate and split URL using urllib3's Url class util
        url = parse_url(self.url)
        # Regular Expression to extract the base/root API path & its version
        matches = search("(\/api(\/v\d+([\.]\d+|)(\/|$)|\/|$))", url.path).groups()
        # Get the API version and root path
        path, version, *_ = matches
        if not path.endswith("/"):
            # Add a / to the end of 'path' if it doesn't already have it
            path += "/"
        # Set version to None if version's not specified in the path
        self.version = version.strip("/") or None
        # Set API URL to this version's root path
        self.url = Url(url.scheme, url.auth, url.host, url.port, path)

    def __repr__(self):
        return f"API(version = {self.version}, {', '.join(f'{attr} = {getattr(url, attr)}' for attr in ('scheme', 'auth', 'host', 'port', 'path'))})"

    def __str__(self):
        return str(self.url)

    def request(self, method: str, path: str, *args, **kwargs):
        # Reimplementing the request function we are now able to request API endpoints by only specifying their relative path
        if path.startswith("/"):
            # If path starts with /, strip it off
            path = path[1:]
        # Join the base API path together with the desired endpoint and send the request, returning a Response object
        return super().request(method, parse_url(urljoin(str(self.url), path)), *args, **kwargs)

class BitStamp(API):
    # Set the API URL
    url = "https://www.bitstamp.net/api/v2/"
    def values(self):
        output = {}
        response = self.get("trading-pairs-info/")
        if response.status_code is not 200:
            # Raise an HTTPError if we do not receive status 200 (OK)
            raise HTTPError(f"Didn't receive expected response ({response.status_code} {response.reason})")
        pairs = response.json()
        for pair in pairs:
            symbol = pair["url_symbol"]
            if symbol.endswith("usd"):
                coin = symbol.strip("usd").upper()
                output[coin] = {key: value for key, value in filter(lambda x: x[0] in ("ask", "bid", "last"), self.get(f"/ticker/{symbol}/").json().items())}
        return output

class BitRex(API):
    url = "https://bittrex.com/api/v1.1/"
    def values(self, coins: tuple = ("LTC", "XRP", "DASH", "BCH", "ETH")):
        output = {}
        for coin in coins:
            try:
                output[coin] = {key.lower(): value for key, value in self.get(f"public/getticker?market=USD-{coin}").json()["result"].items()}
            except Exception as e:
                pass
        return output

class Cex(API):
    url = "https://cex.io/api/"
    def values(self, coins: tuple = ("LTC", "XRP", "DASH", "BCH", "ETH")):
        output = {}
        for coin in coins:
            try:
                output[coin] = {key: value for key, value in filter(lambda x: x[0] in ("ask", "bid", "last"), self.get(f"ticker/{coin}/USD").json().items())}
            except Exception as e:
                print(e)
        return output

class CryptoList(object):
    apis: tuple = (BitStamp, BitRex, Cex)
    def __init__(self):
        for api in self.apis:
            setattr(self, api.__name__.lower(), api())

    def dict(self):
        return {api.__name__: getattr(self, api.__name__.lower()).values() for api in self.apis}

    def last(self):
        floats = set()
        for api in map(lambda x: getattr(x, __name__), self.apis):
            info = self.dict[api]
            if "last" in info:
                floats.add(info["last"])
        return tuple(sorted(floats)[::-1])

    def high_last(self): return max(self.last())
    def low_last(self): return min(self.last())

    def ask(self):
        floats = set()
        for api in map(lambda x: getattr(x, __name__), self.apis):
            info = self.dict[api]
            for attr in ("ask", "lowestAsk"):
                if attr in info:
                    floats.add(info[attr])
        return tuple(sorted(floats)[::-1])

    def high_ask(self): return max(self.ask())
    def low_ask(self): return min(self.ask())

    @staticmethod
    def cost(coinprice, wanted):
        return f'Cost {coinprice * wanted}'

if __name__ == "__main__":
    pprint(CryptoList().dict())
