from re import search
from requests import Session
from urllib.parse import urljoin
from urllib3.util.url import parse_url, Url

__all__ = ["API"]

class API(Session):
    # Pre-define the API URL
    url: str = ""
    def __init__(self):
        super().__init__()
        # Validate and split URL using urllib3's Url class util
        url = parse_url(self.url)
        path = url.path
        # Add a / to the end of 'path' if it doesn't already have it
        if not path.endswith("/"):
            path += "/"
        # Set API URL to this version's root path
        self.url = Url(url.scheme, url.auth, url.host, url.port, path)

    def __repr__(self):
        return f"API({', '.join(f'{attr} = {getattr(self.url, attr)}' for attr in ('scheme', 'auth', 'host', 'port', 'path'))})"

    def __str__(self):
        return str(self.url)

    def request(self, method: str, path: str, *args, **kwargs):
        # Reimplementing the request function we are now able to request API endpoints by only specifying their relative path
        if path.startswith("/"):
            # If path starts with /, strip it off
            path = path[1:]
        # Join the base API path together with the desired endpoint and send the request, returning a Response object
        return super().request(method, parse_url(urljoin(str(self.url), path)), *args, **kwargs)
