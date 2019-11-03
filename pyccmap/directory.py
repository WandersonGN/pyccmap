from pyccmap import apis

__all__ = ["Directory"]

class Directory(object):
    apis: tuple = tuple(sorted((getattr(apis, api) for api in apis.__all__), key = lambda x: x.__name__))
    def __init__(self):
        for api in self.apis:
            setattr(self, api.__name__.lower(), api())
        self.update()

    def update(self):
        self.dict = {}
        self.currencies = set()
        for api in self.apis:
            values = getattr(self, api.__name__.lower()).values()
            self.currencies.update(values.keys())
            self.dict[api.__name__] = {k: values[k] for k in sorted(values)}
        self.currencies = tuple(sorted(self.currencies))
        return self.dict

    def last(self):
        output = {cc: set() for cc in self.currencies}
        for currencies in self.dict.values():
            for currency, info in currencies.items():
                if "last" in info:
                    output[currency].add(float(info["last"]))
        return output

    def ask(self):
        output = {cc: set() for cc in self.currencies}
        for currencies in self.dict.values():
            for currency, info in currencies.items():
                for attr in ("ask", "lowestAsk"):
                    if attr in info:
                        output[currency].add(float(info[attr]))
        return output
