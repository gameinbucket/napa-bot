package trader

type Macd struct {
    EmaShort *ExponentialMovingAverage
    EmaLong *ExponentialMovingAverage
    Current float64
    Signal string
}

func NewMacd(short int64, long int64, initial float64) (*Macd) {
    macd := &Macd{}
    macd.EmaShort = NewEma(short, initial)
    macd.EmaLong = NewEma(long, initial)
    macd.Current = 0
    macd.Signal = "new"
    return macd
}

func (macd *Macd) Update(closing float64) {
    macd.EmaShort.Update(closing)
    macd.EmaLong.Update(closing)
    before := macd.Current
    macd.Current = macd.EmaShort.Current - macd.EmaLong.Current
    if before < 0 && macd.Current > 0 {
        macd.Signal = "sell"
    } else if before > 0 && macd.Current < 0 {
        macd.Signal = "buy"
    } else {
        macd.Signal = "wait"
    }
}