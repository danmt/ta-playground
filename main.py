import pandas as pd
from pandas.core.frame import DataFrame
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands
from ta.trend import SMAIndicator, EMAIndicator, MACD


def getRSI(df: DataFrame, window: int):
    return RSIIndicator(df['CLOSE'], window, True).rsi()


def getBollingerBands(df: DataFrame, std: int, window: int):
    return BollingerBands(df['CLOSE'], window, std, True)


def getBollingerUpperBand(df: DataFrame, std: int, window: int):
    return getBollingerBands(df, std, window).bollinger_hband()


def getBollingerLowerBand(df: DataFrame, std: int, window: int):
    return getBollingerBands(df, std, window).bollinger_lband()


def getBollingerBandWidth(df: DataFrame, std: int, window: int):
    return getBollingerBands(df, std, window).bollinger_wband()


def getSMA(df: DataFrame, window: int):
    return SMAIndicator(df['CLOSE'], window, True).sma_indicator()


def getEMA(df: DataFrame, window: int):
    return EMAIndicator(df['CLOSE'], window, True).ema_indicator()


def getMACD(df: DataFrame, window_slow: int, window_fast: int, window_signal: int):
    return MACD(df['CLOSE'], window_slow, window_fast, window_signal, True).macd()


def main():
    df = pd.read_json('data/BTC_USDT-1d.json')
    df.columns = ['TIMESTAMP', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME']
    df['PROFIT_TOTAL'] = df['CLOSE'] - df['OPEN']
    df['PROFIT_PERCENTAGE'] = (df['PROFIT_TOTAL'] * 100) / df['OPEN']
    df['DATE'] = pd.to_datetime(df['TIMESTAMP'], unit='ms')
    df['RSI'] = getRSI(df, 20)
    df['SMA_20'] = getSMA(df, 20)
    df['SMA_50'] = getSMA(df, 50)
    df['SMA_100'] = getSMA(df, 100)
    df['SMA_200'] = getSMA(df, 200)
    df['EMA_20'] = getEMA(df, 20)
    df['EMA_50'] = getEMA(df, 50)
    df['EMA_100'] = getEMA(df, 100)
    df['EMA_200'] = getEMA(df, 200)
    df['BB_HIGH_1'] = getBollingerUpperBand(df, 1, 20)
    df['BB_LOW_1'] = getBollingerLowerBand(df, 1, 20)
    df['BB_WIDTH_1'] = getBollingerBandWidth(df, 1, 20)
    df['BB_HIGH_2'] = getBollingerUpperBand(df, 2, 20)
    df['BB_LOW_2'] = getBollingerLowerBand(df, 2, 20)
    df['BB_WIDTH_2'] = getBollingerBandWidth(df, 2, 20)
    df['MACD_DEFAULT'] = getMACD(df, 26, 12, 9)
    df['MACD_200_50_20'] = getMACD(df, 200, 50, 20)

    rsiMedian = df['RSI'].median()
    rsiQuantile1 = df['RSI'].quantile(0.25)
    rsiQuantile2 = df['RSI'].quantile(0.5)
    rsiQuantile3 = df['RSI'].quantile(0.75)

    print(rsiMedian)
    print(rsiQuantile1)
    print(rsiQuantile2)
    print(rsiQuantile3)

    print(df[['DATE', 'RSI']].head(30).to_string())


main()
