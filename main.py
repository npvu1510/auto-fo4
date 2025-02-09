from src.constants import *
from src.auto_favorites import allInOnePlayer, buyMultiPlayers, sellPlayer
from src.utils import *
from src.reset_times import RESET_TIME

def main():
    # time.sleep(1800)

    # BUY
    # allInOnePlayer(RESET_TIME['Suarez'], grade= 5, priceType = PRICE_TYPES['100'])
    # allInOnePlayer(False, grade=8, priceType = PRICE_TYPES['100'], autoCancel=False, quantity=3)


    players = [{'row': 8, 'resetTime': RESET_TIME['Blind'], 'quantity': 3,'priceType': PRICE_TYPES['100']}
               , {'row': 1, 'resetTime': RESET_TIME['Carrasco'], 'quantity': 3,'priceType': PRICE_TYPES['100']}
               , {'row':10, 'resetTime': RESET_TIME['Vitinha'], 'quantity': 3,'priceType': PRICE_TYPES['100']}
               , {'row': 7, 'resetTime': RESET_TIME['Ginola'], 'quantity': 3,'priceType': PRICE_TYPES['100']}]

    buyMultiPlayers(players, autoDelay=False)


    # SELL
    # sellPlayer(RESET_TIME['Antony'], grade = 6, priceType=SELL_PRICE_TYPES['100'])
    pass


if __name__ == '__main__':
    main()
