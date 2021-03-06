from trends import MovingAverage


class OnBalanceVolume:
    def __init__(self):
        self.current = None

    def update(self, candles):
        end = len(candles)
        previous = candles[0].closing
        self.current = 0.0
        for index in range(1, end):
            candle = candles[index]
            if candle.closing > previous:
                self.current += candle.volume
            elif candle.closing < previous:
                self.current -= candle.volume
            previous = candle.closing


class MoneyFlow:
    def __init__(self, periods):
        self.signal = 'wait'
        self.periods = periods
        self.current = None

    def update(self, candles):
        positive = 0.0
        negative = 0.0
        end = len(candles)
        start = end - self.periods
        previous = candles[start].typical_price()
        start += 1
        for index in range(start, end):
            candle = candles[index]
            typical_price = candle.typical_price()
            money_flow = typical_price * candle.volume
            if typical_price > previous:
                positive += money_flow
            elif typical_price < previous:
                negative += money_flow
            previous = typical_price
        self.current = positive / (positive + negative)
        if self.current >= 0.8:
            self.signal = 'sell'
        elif self.current <= 0.2:
            self.signal = 'buy'
        else:
            self.signal = 'wait'


class RelativeStrength:
    def __init__(self, periods):
        self.signal = 'wait'
        self.periods = periods
        self.current = None

    def update(self, candles, end):
        positive = MovingAverage(self.periods, 0.0)
        negative = MovingAverage(self.periods, 0.0)
        start = end - self.periods + 1
        for index in range(start, end):
            prev = candles[index - 1].closing
            now = candles[index].closing
            if now > prev:
                positive.update(now - prev)
            else:
                negative.update(prev - now)
        total = positive.current + negative.current
        if total == 0:
            self.signal = 'wait'
            return
        self.current = positive.current / total
        if self.current >= 0.8:
            self.signal = 'sell'
        elif self.current <= 0.2:
            self.signal = 'buy'
        else:
            self.signal = 'wait'