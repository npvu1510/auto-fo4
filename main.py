from src.constants import *
from src.auto_favorites import allInOnePlayer, multiPlayersWithPriority
from src.reset_times import RESET_TIME

def main():
    # time.sleep(1800)
    # allInOnePlayer(RESET_TIME['Suarez'], grade= 5, priceType = PRICE_TYPES['100'])
    # allInOnePlayer(RESET_TIME['Xabi Alonso'], grade= 8, priceType = PRICE_TYPES['10000'])


    players = [{'row': 9, 'resetTime': RESET_TIME['Ayoub'], 'quantity': 3,'priceType': PRICE_TYPES['100']}, {'row': 7, 'resetTime': RESET_TIME['Guedes'], 'quantity': 3,'priceType': PRICE_TYPES['100']}, {'row': 10, 'resetTime': RESET_TIME['Banega'], 'quantity': 3,'priceType': PRICE_TYPES['100']}, {'row': 4, 'resetTime': RESET_TIME['Suarez'],'quantity': 1,'priceType': PRICE_TYPES['100']}]
    multiPlayersWithPriority(players, autoDelay=True)

    pass


if __name__ == '__main__':
    main()
