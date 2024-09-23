from src.constants import *
from src.auto_favorites import allInOnePlayer, buyMultiPlayers, sellPlayer
from src.utils import *
from src.reset_times import RESET_TIME

def main():
    # time.sleep(1800)

    # BUY
    # allInOnePlayer(RESET_TIME['Suarez'], grade= 5, priceType = PRICE_TYPES['100'])
    allInOnePlayer(False, grade= 8, priceType = PRICE_TYPES['1000'])


    # players = [{'row': 5, 'resetTime': RESET_TIME['Fekir'], 'quantity': 3,'priceType': PRICE_TYPES['100']}, {'row': 12, 'resetTime': RESET_TIME['Banega'], 'quantity': 3,'priceType': PRICE_TYPES['100']}, {'row': 4, 'resetTime': RESET_TIME['Suarez'],'quantity': 1,'priceType': PRICE_TYPES['100']}]

    # players = [{'row': 6, 'resetTime': RESET_TIME['Fekir'], 'quantity': 2,'priceType': PRICE_TYPES['100']}, {'row': 5, 'resetTime': RESET_TIME['Danjuma'], 'quantity': 2,'priceType': PRICE_TYPES['100']}, {'row': 7, 'resetTime': RESET_TIME['Inaki'],'quantity': 1,'priceType': PRICE_TYPES['100']}, {'row': 3, 'resetTime': RESET_TIME['Suarez'],'quantity': 1,'priceType': PRICE_TYPES['100']}, {'row': 8, 'resetTime': RESET_TIME['Abedi'],'quantity': 1,'priceType': PRICE_TYPES['100']}]
    
    
    # players = [{'row': 8, 'resetTime': RESET_TIME['Kewell'], 'quantity': 2,'priceType': PRICE_TYPES['100']}, {'row': 14, 'resetTime': RESET_TIME['Cristiano Ronaldo'], 'quantity': 1,'priceType': PRICE_TYPES['1000']},]
    # buyMultiPlayers(players, autoDelay=True)


    # SELL
    # sellPlayer(RESET_TIME['Antony'], grade = 6, priceType=SELL_PRICE_TYPES['100'])
    pass


if __name__ == '__main__':
    main()
