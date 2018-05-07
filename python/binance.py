import time
import http.client
import hmac
import hashlib
import time
import base64
import json

SITE = 'api.binance.com'


def request(method, site, path, body):
    con = http.client.HTTPSConnection(site, 443)
    if body:
        con.putrequest(method, path, body)
        con.putheader('Content-Type', 'application/json')
    else:
        con.putrequest(method, path)
    con.putheader('Accept', 'application/json')
    con.endheaders()
    response = con.getresponse()
    raw_js = response.read()
    status = response.status
    con.close()
    time.sleep(0.5)
    try:
        return json.loads(raw_js.decode()), status
    except Exception:
        return raw_js, status


class Candle:
    def __init__(self, data):
        self.open_time = int(data[0])
        self.open = float(data[1])
        self.high = float(data[2])
        self.low = float(data[3])
        self.closing = float(data[4])
        self.volume = float(data[5])
        self.close_time = int(data[6])
        self.quote_asset_volume = float(data[7])
        self.number_of_trades = int(data[8])
        self.taker_buy_base_asset_volume = float(data[9])
        self.taker_buy_quote_asset_volume = float(data[10])


def get_candles(symbol, interval, start, end):
    path = '/api/v1/klines?symbol={}&interval={}&startTime={}&endTime={}'.format(
        symbol, interval, start, end)
    read, status = request('GET', SITE, path, '')
    if status != 200 or not isinstance(read, list):
        return read, status
    candles = []
    for read_candle in read:
        candles.append(Candle(read_candle))
    return candles, status