import cv2

# ---------------------------------------------------------------- TEMPLATES ----------------------------------------------------------------
# 1600x900
BUY_MODAL_OPEN_1600_1900 = cv2.imread('./templates/1600x900/buy_modal_opened.png') 
# SELL_MODAL_OPENED_1600_1900 = cv2.imread('./templates/1600x900/sell_modal_opened.png') 
MODAL_CLOSED_1600_1900 = cv2.imread('./templates/1600x900/modal_closed.png') 

SPAM_ERROR_1600_1900 = cv2.imread('./templates/1600x900/spam_error.png')
SLOT_1_1600_1900 = cv2.imread('./templates/1600x900/slot_1.png')
BADGE_1600_1900 = cv2.imread('./templates/1600x900/badge.png')


# ----------------------------------------------------------------  CLICK POSITIONS ----------------------------------------------------------------
BUY_BUTTON_FAVORITES = [1110, 828]
MAX_PRICE_BUTTON_BUY_MODAL = [1284, 395]
INC_QUANTITY_BUTTON_BUY_MODAL = [1284, 551]
BUY_BUTTON_BUY_MODAL = [1034, 725]


# ----------------------------------------------------------------  CAPTURE POSITIONS ----------------------------------------------------------------
# MODAL
BUY_MODAL_OPEN_POS = [1278, 566, 25, 16]
BUY_MODAL_CLOSE_POS = [523, 169, 23, 17]

# PRICES
MAX_PRICE_IN_BUY_MODAL_POS = [1195, 382, 86, 22]

# chục nghìn tỷ
CHUC_NGHIN_MAX_PRICE_IN_BUY_MODAL_POS = [1209, 382, 45, 22]
# nghìn tỷ
NGHIN_MAX_PRICE_IN_BUY_MODAL_POS = [1214, 382, 55, 22]
# trăm tỷ
TRAM_MAX_PRICE_IN_BUY_MODAL_POS = [1225, 382, 55, 22]


SPAM_ERROR_POS = [782, 422, 118, 22]
ORDER_SLOT_RESULT = [1159, 464, 22, 34]


# ----------------------------------------------------------------  PRICES  ----------------------------------------------------------------
PRICE_TYPES={'0': MAX_PRICE_IN_BUY_MODAL_POS,'100': TRAM_MAX_PRICE_IN_BUY_MODAL_POS, '1000':NGHIN_MAX_PRICE_IN_BUY_MODAL_POS , '10000': CHUC_NGHIN_MAX_PRICE_IN_BUY_MODAL_POS}


# ----------------------------------------------------------------  THRESHOLDS  ----------------------------------------------------------------
OPEN_MODAL_THRESHOLD = 0.85
CLOSE_MODAL_THRESHOLD = 0.9
COMPARE_PRICE_THRESHOLD = 0.8


# ----------------------------------------------------------------  TIMES  ----------------------------------------------------------------
DELAY_INTERVAL_IN_MINUTE = 5
DELAY_DURATION_IN_SECOND = 30
OFFSET = 0







