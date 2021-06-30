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
