
from indicators import getBollingerBandWidth, getBollingerLowerBand, getBollingerUpperBand, getEMA, getMACD, getRSI, getSMA
from utils import generateRandomRange, percentage
import pandas as pd
from pandas.core.frame import DataFrame
from consts import pricesFileName, fileName, maxPositionDuration, quantityOfPositions, positionsColumns


def createPosition(openDay: int, closeDay: int, duration: int, indicators: DataFrame):
    """ 
    Create a position based on an open day, a close day, a duration and a list of 
    historical indicators

    Parameters:
        openDay(int): Open day relative to start
        closeDay(int): Close day relative to start
        duration(int): Duration of the position
        indicators(DataFrame): List of indicators pre-calculated

    Returns
        Position: a newly created position
    """

    openDayEntry = indicators.iloc[openDay]
    closeDayEntry = indicators.iloc[closeDay]

    return {
        'OPEN_DAY': openDay,
        'CLOSE_DAY': closeDay,
        'POSITION_DURATION': duration,
        'PROFIT': closeDayEntry['CLOSE'] - openDayEntry['CLOSE'],
        'PROFIT_PERCENT': percentage(closeDayEntry['CLOSE'] - openDayEntry['CLOSE'], openDayEntry['CLOSE']),
        'OPEN_PRICE': openDayEntry['CLOSE'],
        'CLOSE_PRICE': closeDayEntry['CLOSE'],
        'OPEN_RSI': openDayEntry['RSI'],
        'CLOSE_RSI': closeDayEntry['RSI'],
        'OPEN_SMA_20': openDayEntry['SMA_20'],
        'CLOSE_SMA_20': closeDayEntry['SMA_20'],
        'OPEN_SMA_50': openDayEntry['SMA_50'],
        'CLOSE_SMA_50': closeDayEntry['SMA_50'],
        'OPEN_SMA_100': openDayEntry['SMA_100'],
        'CLOSE_SMA_100': closeDayEntry['SMA_100'],
        'OPEN_SMA_200': openDayEntry['SMA_200'],
        'CLOSE_SMA_200': closeDayEntry['SMA_200'],
        'OPEN_EMA_20': openDayEntry['EMA_20'],
        'CLOSE_EMA_20': closeDayEntry['EMA_20'],
        'OPEN_EMA_50': openDayEntry['EMA_50'],
        'CLOSE_EMA_50': closeDayEntry['EMA_50'],
        'OPEN_EMA_100': openDayEntry['EMA_100'],
        'CLOSE_EMA_100': closeDayEntry['EMA_100'],
        'OPEN_EMA_200': openDayEntry['EMA_200'],
        'CLOSE_EMA_200': closeDayEntry['EMA_200'],
        'OPEN_BB_HIGH_1': openDayEntry['BB_HIGH_1'],
        'CLOSE_BB_HIGH_1': closeDayEntry['BB_HIGH_1'],
        'OPEN_BB_HIGH_2': openDayEntry['BB_HIGH_2'],
        'CLOSE_BB_HIGH_2': closeDayEntry['BB_HIGH_2'],
        'OPEN_BB_LOW_1': openDayEntry['BB_LOW_1'],
        'CLOSE_BB_LOW_1': closeDayEntry['BB_LOW_1'],
        'OPEN_BB_LOW_2': openDayEntry['BB_LOW_2'],
        'CLOSE_BB_LOW_2': closeDayEntry['BB_LOW_2'],
        'OPEN_BB_WIDTH_1': openDayEntry['BB_WIDTH_1'],
        'CLOSE_BB_WIDTH_1': closeDayEntry['BB_WIDTH_1'],
        'OPEN_BB_WIDTH_2': openDayEntry['BB_WIDTH_2'],
        'CLOSE_BB_WIDTH_2': closeDayEntry['BB_WIDTH_2'],
        'OPEN_MACD_DEFAULT': openDayEntry['MACD_DEFAULT'],
        'CLOSE_MACD_DEFAULT': closeDayEntry['MACD_DEFAULT'],
        'OPEN_MACD_200_50_20': openDayEntry['MACD_200_50_20'],
        'CLOSE_MACD_200_50_20': closeDayEntry['MACD_200_50_20'],
        'CLASS': 'green' if openDayEntry['CLOSE'] <= closeDayEntry['CLOSE'] else 'red',
    }


def generatePositions(quantity: int, totalIndicators: int, maxDuration: int, indicators: DataFrame):
    """ 
    Generate a set of positions randomly without duplications.

    Parameters:
        quantity(int): Number of positions to generate
        totalIndicators(int): Number of indicators available
        maxDuration(int): Maximum duration for a position
        indicators(DataFrame): List of indicators available

    Returns:
        [Position]: List of positions randomly generated
    """

    if (totalIndicators <= 1):
        raise Exception('Total indicators must be more than 1')

    positions = {}

    for _ in range(0, quantity):
        generated = False

        # Ensure there's no duplicate positions
        while (not generated):
            [openDay, closeDay, positionDuration] = generateRandomRange(
                totalIndicators, maxDuration)

            positionFound = positions.get(f'{openDay}-{closeDay}')

            if (not positionFound):
                generated = True  # Exit if a position was added
                positions[f'{openDay}-{closeDay}'] = createPosition(
                    openDay, closeDay, positionDuration, indicators)

    return positions.values()


def getIndicators(fileName: str):
    """ 
    Read a JSON file, save it into a DataFrame and calculate a set of indicators

    Parameters:
        fileName(str): Name of the json file stored in /data

    Returns: 
        [DataFrame, int]: Returns DataFrame with all the indicators and its length
    """
    df = pd.read_json(f'data/{fileName}')
    df.columns = ['TIMESTAMP', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME']
    df['PROFIT_TOTAL'] = df['CLOSE'] - df['OPEN']
    df['PROFIT_PERCENTAGE'] = percentage(df['PROFIT_TOTAL'], df['OPEN'])
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

    return [df, len(df)]


def main():
    [indicatorsDf, totalIndicators] = getIndicators(pricesFileName)
    positionsDf = pd.DataFrame(
        generatePositions(
            quantityOfPositions,
            totalIndicators,
            maxPositionDuration,
            indicatorsDf
        ),
        columns=positionsColumns)
    positionsDf.to_csv(f'{fileName}.csv', index=False)


main()
