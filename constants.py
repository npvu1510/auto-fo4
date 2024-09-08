import cv2

# ---------------------------------------------------------------- TEMPLATES ----------------------------------------------------------------
# MODAL
# BUY_MODAL_IMAGE = cv2.imread('./templates/buy_modal.png') 
# BUY_MODAL_BIGGER_IMAGE = cv2.imread('./templates/buy_modal_bigger.png')
# BUY_MODAL_BACKUP_IMAGE = cv2.imread('./templates/1600x1900/buy_modal_backup.png') 

# SELL_MODAL_IMAGE = cv2.imread('./templates/sell_modal.png') 
# BOUGHT_MODAL_IMAGE = cv2.imread('./templates/bought_modal.png')
# SOLD_MODAL_IMAGE = cv2.imread('./templates/sold_modal.png')
# SOLD_MULTI_MODAL_IMAGE = cv2.imread('./templates/sold_multi_modal.png')
# CLOSE_MODAL_IMAGE = cv2.imread('./templates/close_modal.png') 
# # RESET_MODAL_IMAGE = cv2.imread('./templates/reset_modal.png') 
# # CANCEL_MODAL_IMAGE = cv2.imread('./templates/cancel_modal.png') 

# # TRANSACTIONS
HYPHEN_IMAGE = cv2.imread('./templates/hyphen.png') 


# # FAVORITES
# PRICE_UPDATING_IMAGE = cv2.imread('./templates/price_updating.png') 


# 1600x900
# BUY_MODAL_1600_1900 = cv2.imread('./templates/1600x900/buy_modal_opened.png') 
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
# # TRANSACTIONS
# TRANSACTION_POS = [276, 191, 103, 459]

# # ORDER TABLE
# ORDER_ROW_POS = [377, 361, 344, 327, 310, 294, 277, 260]

# # MODAL STATUS

# SELL_MODAL_POS = [850, 295, 22, 14]
# BOUGHT_MODAL_POS = [615, 414, 36, 16]
# SOLD_MODAL_POS = [402, 184, 68, 17]
# SOLD_MULTI_MODAL_POS = [197, 128, 61, 19]

# CLOSE_MODAL_POS = [636, 142, 20, 13]

# PRICE



# MIN_PRICE_IN_SELL_MODAL_POS = [900, 320, 142, 22]


# # IN MODAL
# IN_BUY_MODAL_NAME_POS = 300, 345, 77, 14
# IN_SELL_MODAL_NAME_POS = 300, 375, 77, 14


# LATEST
BUY_MODAL_OPEN_POS = [1278, 566, 25, 16]
BUY_MODAL_CLOSE_POS = [523, 169, 23, 17]

# PRICES
MAX_PRICE_IN_BUY_MODAL_POS = [1195, 382, 86, 22]

# chục nghìn tỷ
CHUC_NGHIN_MAX_PRICE_IN_BUY_MODAL_POS = [1209, 382, 45, 22]
# nghìn tỷ
NGHIN_MAX_PRICE_IN_BUY_MODAL_POS = [1214, 382, 55, 22]
# tram tỷ
TRAM_MAX_PRICE_IN_BUY_MODAL_POS = [1225, 382, 55, 22]


SPAM_ERROR_POS = [782, 422, 118, 22]
ORDER_SLOT_RESULT = [1159, 464, 22, 34]


# ----------------------------------------------------------------  PRICES  ----------------------------------------------------------------
PRICE_TYPES={'0': MAX_PRICE_IN_BUY_MODAL_POS,'100': TRAM_MAX_PRICE_IN_BUY_MODAL_POS, '1000':NGHIN_MAX_PRICE_IN_BUY_MODAL_POS , '10000': CHUC_NGHIN_MAX_PRICE_IN_BUY_MODAL_POS}


# ----------------------------------------------------------------  THRESHOLDS  ----------------------------------------------------------------
OPEN_MODAL_THRESHOLD = 0.85
CLOSE_MODAL_THRESHOLD = 0.85
COMPARE_PRICE_THRESHOLD = 0.8


# ----------------------------------------------------------------  TIMES  ----------------------------------------------------------------





# ---------------------------------------------------------------- RESET TIME ----------------------------------------------------------------
from timeFns import  toResetTime


RESET_TIME = {
    "Scamacca": toResetTime("Chẵn 18 - Chẵn 38"),
    "Correa": toResetTime("Chẵn 15 - Chẵn 35"),
    "Unal": toResetTime("Chẵn 01 - Chẵn 21"),
    "Anguissa": toResetTime("Chẵn 20 - Chẵn 40"),
    "Awoniyi": toResetTime("Chẵn 06 - Chẵn 26"),
    "Rowe": toResetTime("Chẵn 30 - Chẵn 50"),
    "Guedes": toResetTime("Chẵn 15 - Chẵn 35"),
    "Milik": toResetTime("Lẻ 59 - Chẵn 19"),
    "Muani": toResetTime("Chẵn 18 - Chẵn 38"),
    "Bravo": toResetTime("Chẵn 00-25"),
    "Sangare": toResetTime("Chẵn 24 - Chẵn 44"),
    "Benítez": toResetTime("Chẵn 31 - Chẵn 51"),
    "Gordon": toResetTime("Chẵn 36 - Chẵn 56"),
    "Matić": toResetTime("Lẻ 54 - Chẵn 14"),
    'Bremer': toResetTime("Chẵn 00-25"),
    'Nunes': toResetTime("Chẵn 56 - Lẻ 16"),
    "Jose": toResetTime("Chẵn 09 - Chẵn 29"),
    "Kampl": toResetTime("Chẵn 30-59"),
    "Chandler": toResetTime("Chẵn 30-59"),
    "Saponara": toResetTime("Chẵn 30-59"),
    "Iwobi": toResetTime("Chẵn 00-25"),
    "Patricio": toResetTime("Chẵn 00-25"),
    "Banega": toResetTime("Chẵn 30-59"),
    "Grifo": toResetTime("Chẵn 30-59"),
    "Anderson": toResetTime("Chẵn 30-59"),
    "Kaka": toResetTime("Chẵn 00-25"),
    "Henry": toResetTime("Chẵn 20-40"),
    "Pirlo": toResetTime("Chẵn 20-40"),
    "Mathu": toResetTime("Chẵn 00-25"),
    "Bergkamp": toResetTime("Chẵn 00-25"),
    "Illarramendi": toResetTime("Chẵn 00-25"),
    "Inaki": toResetTime("Chẵn 30-59"),
    'Suarez': toResetTime("Lẻ 00 - Lẻ 25"),
    "Vieira": toResetTime("Chẵn 15-35"),
    "Xabi Alonso": toResetTime("Chẵn 29-49"),
    "Gerrard": toResetTime("Chẵn 24-45"),
    "Torres": toResetTime("Chẵn 50 - Lẻ 20"),

}


# SPAM ERROR
# a
# TUYỆT ĐỐI: 861, 481
# TƯƠNG ĐỐI: 782, 422


# a
# TUYỆT ĐỐI: 979, 503        
# TƯƠNG ĐỐI: 900, 444,118, 22