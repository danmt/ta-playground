import random


def generateRandomRange(max: int, durationCap: int):
    open = random.randrange(0, max - 1, 1)
    durationCap = durationCap if (
        max - open) > durationCap else max - open
    duration = random.randrange(1, durationCap, 1)
    close = open + duration
    return [open, close, duration]


def percentage(part, whole):
    return 100 * part / whole
