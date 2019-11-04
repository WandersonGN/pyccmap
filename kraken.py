from pyccmap import API


class Kraken(API):
    url = 'https://api.kraken.com/'

    def values(self):
        output = {s.strip("USD").rstrip('Z').replace('X', '', 1): dict(zip(('ask', 'bid', 'last', 'volume', 'vwavg',
                                                  'num_trades', 'low', 'high', 'open'), (k['a'][0], k['b'][0], k['c'][0], k['v'][0], k['p'][0],
                                                                                         k['t'][0], k['l'][0], k['h'][0], k['o'][0])))

                  for s, k in self.get('0/public/Ticker?pair=ETHUSD,XRPUSD,BCHUSD,LTCUSD').json()['result'].items()}
        return output




