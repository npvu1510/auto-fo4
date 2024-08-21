import os
import time
# import cv2
# import playsound

# my modules
from constants import *
from utils import *
from timeCheck import  isResetTime_v2, toResetTime, time_until_reset


# ---------------------------------------------------------------- OTHERS ----------------------------------------------------------------
def isAvailableBuySlot():
    # Lấy giá đầu tiên
    initPrice = capture_window_region(TARGET_WINDOW, 930, 500, 106, 30)

    i = 0
    while i < 8:
        # Lấy giá dòng hiện tại
        currentPrice = capture_window_region(TARGET_WINDOW, 576, ORDER_ROW_POS[i], 80, 16)
        
        # Nếu gặp dòng đầu tiên không phải gạch nối
        if compareImage(imageToArr(currentPrice), HYPHEN_IMAGE, showDiff=False, threshold=100):
            break

        i+=1
    
    # Nếu chưa có ai đặt => còn slot
    if i == 8:
        return True
    
    single_click(TARGET_WINDOW , 576, ORDER_ROW_POS[i] + 8)
    time.sleep(0.1)

    currentPrice = capture_window_region(TARGET_WINDOW, 930, 500, 106, 30)

    # Nếu true => còn slot , ngược lại => hết slot
    res = compareImage(imageToArr(initPrice), imageToArr(currentPrice), threshold=100)

    # if res:
    #     saveImage(initPrice, f'init_{time.time()}.png')
    #     saveImage(currentPrice, f'current_{time.time()}.png')

    return res


def isAvailableSellSlot():
    # click gia min nguoi ta dat
    single_click(TARGET_WINDOW, 619, 434)
    time.sleep(0.1)

    # o gia
    firstPic = capture_window_region(TARGET_WINDOW,  770, 444, 264, 28)
    # saveImage(firstPic, 'a1.png')

    # click gia min hien tai
    single_click(TARGET_WINDOW, 1020, 330)
    time.sleep(0.1)

    # o gia
    secondPic = capture_window_region(TARGET_WINDOW,  770, 444, 264, 28)
    # saveImage(secondPic, 'a2.png')

    res = compareImage(imageToArr(firstPic), imageToArr(secondPic), threshold=100)
    return res


# def checkSpamError():
#     error = capture_window_region(TARGET_WINDOW, 562, 335, 485, 284)
    
#     if not compareImage(SPAM_ERROR_IMAGE, imageToArr(error), threshold=120):
#         time.sleep(120)
#         single_click(TARGET_WINDOW, 905, 590)
#         return True
    
#     return False


# ---------------------------------------------------------------- FAVORORITES FUNCTIONS ----------------------------------------------------------------
def updateCurrentPlayerBySwitchTab(row=0, prevPlayer=None):
    single_click(TARGET_WINDOW, 269, 205 + row * 32)
    time.sleep(0.1)

    currentPlayer, timeout = waitForChangePlayer(prevPlayer)
    if timeout:
        return currentPlayer, True
    # time.sleep(0.5)
        
    single_click(TARGET_WINDOW, 669, 149)
    time.sleep(0.1)
    single_click(TARGET_WINDOW, 530, 148)
    # time.sleep(1)

    return currentPlayer, False

def waitForChangePlayer(prevPlayer, timeout=10):
    start = time.time()

    currentPlayer = capture_window_region(TARGET_WINDOW, 716, 202, 104, 21)

    while prevPlayer and not compareImage(imageToArr(currentPlayer), imageToArr(prevPlayer)):
        if time.time() - start >= timeout:
            return None, True
        
        currentPlayer = capture_window_region(TARGET_WINDOW, 716, 202, 104, 21)
    
    return currentPlayer, False

def buyMaxOnFavorite(prevPrice):
    currentPrice = capture_window_region(TARGET_WINDOW, 962, 281, 77, 54)

    if prevPrice:
        if compareImage(imageToArr(prevPrice), imageToArr(currentPrice), showDiff=False, threshold=100):
        # if True:
            res = isAvailableBuySlot()
            print(f'còn slot' if res else f'hết slot')
            if res:
                buy(quantity=2)

        else:
            print("Chưa reset giá")
    
    else:
        res = isAvailableBuySlot()
        print(f'còn slot' if res else f'hết slot')
        if res:
            buy(quantity=2)

    
    return currentPrice

def buy(priceType='max', quantity=1):
    # Click vào giá
    if priceType == 'max':
        single_click(TARGET_WINDOW, 831, 586)
        # multi_click(1267, 395, times=2)
        time.sleep(0.05)

    # Set số lượng
    quantity = 10 if quantity > 10 else quantity
    quantity = 1 if quantity < 1 else quantity

    single_click(TARGET_WINDOW,  1004, 453)
    time.sleep(0.1)
    send_key(TARGET_WINDOW, KEY_CODES[str(quantity)])
    time.sleep(0.1)

    # Click để mua
    single_click(TARGET_WINDOW, 831, 586)

    finish_capture = capture_window(TARGET_WINDOW)
    saveImage(finish_capture, f'buy_{time.time()}.png')


# ---------------------------------------------------------------- TRANSACTION FUNCTIONS ----------------------------------------------------------------
def waitModal_v3(until='open', timeout = 15):
    threshold = 120

    startCountdown = time.time()
    while True:
        if time.time() - startCountdown >= timeout:
            return False
        if until == 'open':
            if not compareImage(BUY_MODAL_IMAGE, imageToArr(capture_window_region(TARGET_WINDOW, BUY_MODAL_POS[0], BUY_MODAL_POS[1], BUY_MODAL_POS[2], BUY_MODAL_POS[3])), threshold=threshold, showDiff=False):
                return 'buy'
            if not compareImage(SELL_MODAL_IMAGE, imageToArr(capture_window_region(TARGET_WINDOW,  SELL_MODAL_POS[0], SELL_MODAL_POS[1], SELL_MODAL_POS[2], SELL_MODAL_POS[3])), threshold=threshold, showDiff=False):
                return 'sell'
            if not compareImage(BOUGHT_MODAL_IMAGE, imageToArr(capture_window_region(TARGET_WINDOW,  BOUGHT_MODAL_POS[0], BOUGHT_MODAL_POS[1], BOUGHT_MODAL_POS[2], BOUGHT_MODAL_POS[3])), threshold=threshold, showDiff=False):
                return 'bought'
            if not compareImage(SOLD_MODAL_IMAGE, imageToArr(capture_window_region(TARGET_WINDOW,  SOLD_MODAL_POS[0], SOLD_MODAL_POS[1], SOLD_MODAL_POS[2], SOLD_MODAL_POS[3])), threshold=threshold, showDiff=False) or not compareImage(SOLD_MULTI_MODAL_IMAGE, imageToArr(capture_window_region(TARGET_WINDOW,  SOLD_MULTI_MODAL_POS[0], SOLD_MULTI_MODAL_POS[1], SOLD_MULTI_MODAL_POS[2], SOLD_MULTI_MODAL_POS[3])), threshold=threshold, showDiff=False):
                return 'sold'
            
        elif until == 'close':
            if not compareImage(CLOSE_MODAL_IMAGE, imageToArr(capture_window_region(TARGET_WINDOW, CLOSE_MODAL_POS[0], CLOSE_MODAL_POS[1], CLOSE_MODAL_POS[2], CLOSE_MODAL_POS[3])), threshold=threshold, showDiff=False):
                return True  
    # time.sleep(0.25)


def reBuy():
    # Click vào giá
    single_click(TARGET_WINDOW, 1031, 322)

    # Click mua
    single_click(TARGET_WINDOW, 830, 586)

    # Lưu kết quả
    saveImage(capture_window(TARGET_WINDOW), f'updated_{time.time()}.png')


def findPlayerIndex(playerName, players):
    for i in range(len(players)):
        if players[i]:
            if not compareImage(imageToArr(players[i]['name']), imageToArr(playerName), threshold=100):
                return i
    return -1


def buyMaxOnTransaction_v3(prevPrice):
    resetFlag = False

    currentPrice = capture_window_region(TARGET_WINDOW, MAX_PRICE_POS[0], MAX_PRICE_POS[1], MAX_PRICE_POS[2], MAX_PRICE_POS[3])

    if prevPrice:
        # print('Thay đổi giá: ')
        # print(compareImage(imageToArr(prevPrice), imageToArr(currentPrice), threshold=100, showDiff=False))
        # time.sleep(5)
        
        if compareImage(imageToArr(prevPrice), imageToArr(currentPrice), threshold=80, showDiff=False):
        # if True:
            
            reBuy()
            print('Cập nhật thành công !!')

            # isAvailable = isAvailableBuySlot()
            # print(f'còn slot' if isAvailable else f'hết slot')
            # if isAvailable:
            #     reBuy()
            #     print('Cập nhật thành công !!')
            # else:
            #     saveImage(capture_window(TARGET_WINDOW), f'failed_{time.time()}.png')
            #     single_click(TARGET_WINDOW, 971, 587)
            
            # resetFlag = True

        else:
            print("Chưa reset giá")
    
    else:
        isAvailable = isAvailableBuySlot()
        print(f'còn slot' if isAvailable else f'hết slot')
        if isAvailable:
            reBuy()
            print('Cập nhật thành công !!')

            # resetFlag = True

    
    return currentPrice, resetFlag


def sellMinOnTransaction_v3(prevPrice):
    resetFlag = False

    currentPrice = capture_window_region(TARGET_WINDOW, MIN_PRICE_POS[0], MIN_PRICE_POS[1], MIN_PRICE_POS[2], MIN_PRICE_POS[3])

    if prevPrice:
        # print('Thay đổi giá: ')
        # res = compareImage(imageToArr(prevPrice), imageToArr(currentPrice), threshold=100, showDiff=True)
        # print(res)

        # if res:
        #     saveImage(prevPrice, 'prevPrice.png')
        #     saveImage(prevPrice, 'currentPrice.png')
        #     exit()
        if compareImage(imageToArr(prevPrice), imageToArr(currentPrice), threshold=100, showDiff=False):
        # if True:
            single_click(TARGET_WINDOW, 773, 619)
            saveImage(capture_window(TARGET_WINDOW), f'updated_{time.time()}.png')
            return currentPrice, resetFlag
            isAvailable = isAvailableSellSlot()
            print(f'còn slot' if isAvailable else f'hết slot')
            if isAvailable:
                single_click(TARGET_WINDOW, 773, 619)
                print('Cập nhật thành công !!')
            else:
                saveImage(capture_window(TARGET_WINDOW), f'failed_{time.time()}.png')
                single_click(TARGET_WINDOW,  908, 617)
            
            # resetFlag = True

        else:
            print("Chưa reset giá")
    
    else:
        # single_click(TARGET_WINDOW, 773, 619)
        # return currentPrice, resetFlag
        isAvailable = isAvailableSellSlot()
        print(f'còn slot' if isAvailable else f'hết slot')
        if isAvailable:
            single_click(TARGET_WINDOW, 773, 619)
            print('Cập nhật thành công !!')

            # resetFlag = True

    return currentPrice, resetFlag


def isTransactionChanged(prevTransactions):
    currentTransactions = capture_window_region(TARGET_WINDOW, TRANSACTION_POS[0], TRANSACTION_POS[1], TRANSACTION_POS[2], TRANSACTION_POS[3])
    if prevTransactions == False or compareImage(imageToArr(prevTransactions), imageToArr(currentTransactions), showDiff=False):
        return True, currentTransactions
    return False, currentTransactions


def genTransactionData(numRow):
    newTransactions = []
    changeArr = []

    i = 0
    while i < numRow:
        # Cancel timeout modal đợt trước
        # send_key(TARGET_WINDOW, KEY_CODES['ESC'])
        # time.sleep(0.5)
        
        # Click đăng ký lại và xác định loại modal
        single_click(TARGET_WINDOW, 1000, 212 + i * 42, hover=True)
        modalType = waitModal_v3(until='open')

        if not modalType:
            # saveImage(capture_window(TARGET_WINDOW), f'timeout_{time.time()}.png')
            # error = checkSpamError()            
            # if error:
            #     time.sleep(60)
            continue
        
        # xác định vị trí player name của loại modal hiện tại
        if modalType == 'buy':
            prevPrice, isReset = buyMaxOnTransaction_v3(False)
            newTransactions.append({'prevPrice': prevPrice,'isReset': isReset, 'resetTime': False})
    
        elif modalType =='sell':
            prevPrice, isReset = sellMinOnTransaction_v3(False)
            newTransactions.append({'prevPrice': prevPrice,'isReset': isReset, 'resetTime': False})
        else:
            newTransactions.append(False)
        
        # ĐÓNG MODAL
        if modalType == 'buy':
            single_click(TARGET_WINDOW, 971, 587)
        elif modalType == 'sell':
            single_click(TARGET_WINDOW,  908, 617)
        else:
            send_key(TARGET_WINDOW, KEY_CODES['ESC'])
        

        # CHỜ ĐÓNG MODAL
        # print('truoc khi close')
        isClosed = waitModal_v3(until='close')
        # print('sau khi close')
        if not isClosed:
            saveImage(capture_window(TARGET_WINDOW), f'timeout_{time.time()}.png')
            if modalType == 'buy':
                if not newTransactions[i]['isReset']:
                    single_click(TARGET_WINDOW, 971, 587)
            else:
                if not newTransactions[i]['isReset']:
                    single_click(TARGET_WINDOW,  908, 617)
            waitModal_v3(until='close')
        # time.sleep(0.25)
        # time.sleep(0.05)
        i+=1

    # print('TRACKING')
    # print(changeArr)
    return newTransactions


def runOnTransactions_v3(numRow=4, resetTime=None):
    prevTransactions = False
    transactions = []

    start = time.time()
    i = 0
    while True:
        # time.sleep(0.25)
        # if time.time() - start > 300:
        #     time.sleep(15)
        #     start = time.time()
        #     continue

        # GIỚI HẠN SỐ LƯỢNG GIAO DỊCH
        if i == numRow:
            i = 0
            # print('SORTED TRANACTIONS')
            # print(transactions)

            # print('Đang chờ thay đổi transaction')
            # time.sleep(5)

            # transactions = sortTransactions(transactions)
            os.system('cls')
        
        # KIỂM TRA TRANSACTION CÓ XẢY RA THAY ĐỔI KHÔNG ?
        # SAU ĐÓ LƯU DỮ LIỆU TRANSACTION
        res, prevTransactions = isTransactionChanged(prevTransactions)
        if res:
            print("🔁 Đang cập nhật danh sách giao dịch..")
            transactions = genTransactionData(numRow)

            os.system('cls')
        # print('a')

        # CHỈ CHO PHÉP MUA HOẶC BÁN
        if not transactions[i]:
            i+=1
            continue
        # print('b')
        # KIỂM TRA TỚI GIỜ RESET CHƯA ?
        

        # KIỂM TRA CẦU THỦ ĐÃ RESET GIÁ TRONG ĐỢT RESET NÀY HAY CHƯA ?

        # ĐĂNG KÝ LẠI, CHỜ MODAL MỞ VÀ XÁC ĐỊNH LOẠI MODAL
        single_click(TARGET_WINDOW, 1000, 212 + i * 42, hover=True)
        modalType = waitModal_v3(until='open')
        # print(modalType)

        if not modalType:
            # saveImage(capture_window(TARGET_WINDOW), f'timeout_{time.time()}.png')
            continue
        
        # print(transactions)
        # Thực hiện chức năng chính và đóng modal
        if  modalType == 'buy':
            print(f"💵 Mua cầu thủ #{i+1}")
            transactions[i]['prevPrice'], transactions[i]['isReset'] = buyMaxOnTransaction_v3(transactions[i]['prevPrice'])

            # if not transactions[i]['isReset']:
            #     single_click(TARGET_WINDOW, 971, 587)
        else:
            print(f"🤑 Bán cầu thủ #{i+1}")
            transactions[i]['prevPrice'], transactions[i]['isReset'] = sellMinOnTransaction_v3(transactions[i]['prevPrice'])

            # if not transactions[i]['isReset']:
            #     single_click(TARGET_WINDOW,  908, 617)

        # ĐÓNG MODAL
        if modalType == 'buy':
            single_click(TARGET_WINDOW, 971, 587)
        elif modalType == 'sell':
            single_click(TARGET_WINDOW,  908, 617)
        else:
            send_key(TARGET_WINDOW, KEY_CODES['ESC'])
        

        # CHỜ ĐÓNG MODAL
        isClosed = waitModal_v3(until='close')
        if not isClosed:
            saveImage(capture_window(TARGET_WINDOW), f'timeout_{time.time()}.png')
            if modalType == 'buy':
                # if not transactions[i]['isReset']:
                single_click(TARGET_WINDOW, 971, 587)
            else:
                # if not transactions[i]['isReset']:
                single_click(TARGET_WINDOW,  908, 617)
            waitModal_v3(until='close')

        # print(transactions)
        # time.sleep(3)

        i+=1


def runOnFavourite(numRow=1):
    prevPrice = None
    currentPrice = None

    currentRow = 0
    while True:
        if currentRow == numRow:
            currentRow = 0
        
        # # Chuyển dòng
        # single_click(TARGET_WINDOW,466, 250 + currentRow * 41,draw=f'position_{currentRow}.png')
        # time.sleep(0.05)

        # Chuyển tab cập nhật
        single_click(TARGET_WINDOW,835, 179)
        time.sleep(0.05)
        single_click(TARGET_WINDOW,669, 178)
        time.sleep(0.2)

        # Làm gì đó.......
        # Kiểm tra giá trị cầu thủ đã thay đổi chưa?

        if prevPrice:
            currentPrice = capture_window_region(TARGET_WINDOW, 897, 379, 101, 31)

            start = time.time()
            while not compareImage(imageToArr(currentPrice), PRICE_UPDATING_IMAGE, threshold=30, showDiff=False) and time.time() - start <= 5:
                currentPrice = capture_window_region(TARGET_WINDOW, 897, 379, 101, 31)
                # print("🔃 Đang cập nhật giá...")
            
            res = compareImage(imageToArr(prevPrice), imageToArr(currentPrice), threshold=30, showDiff=False)

            print('Thay đổi' if res else 'Không thay đổi')
            # if res:
            #     return
            time.sleep(1)
            
            # single_click(TARGET_WINDOW, 1100, 828)

            # expandArrow = capture_window_region(TARGET_WINDOW, 536, 205, 26, 15)
            # timeout = False
            # start = time.time()
            # while not compareImage(imageToArr(expandArrow), BUY_MODAL_BIGGER_IMAGE, threshold=80, showDiff=False):
            #     if time.time() - start > 20:
            #         timeout = True
            #         break
            #     expandArrow = capture_window_region(TARGET_WINDOW, 536, 205, 26, 15)
            #     print("Chờ modal mở...")
            # if timeout:
            #     continue
            # single_click(TARGET_WINDOW, 1253, 393)
            # time.sleep(0.05)
            # single_click(TARGET_WINDOW, 1033, 722)


            # expandArrow = capture_window_region(TARGET_WINDOW, 536, 205, 26, 15)
            # start = time.time()
            # while compareImage(imageToArr(expandArrow), BUY_MODAL_BIGGER_IMAGE, threshold=80, showDiff=False):
            #     if time.time() - start > 10:
            #         single_click(TARGET_WINDOW, 1214, 725)
            #         break

            #     expandArrow = capture_window_region(TARGET_WINDOW, 536, 205, 26, 15)
            #     print("Chờ modal đóng...")
        
        else:
            currentPrice = capture_window_region(TARGET_WINDOW, 897, 379, 101, 31)


        prevPrice = currentPrice


def waitModal_v4(until='open', timeout=15):
    threshold = 50

    start = time.time()
    while time.time() - start >= timeout:        
        if until == 'open':
            if not compareImage(BUY_MODAL_IMAGE, imageToArr(capture_window_region(TARGET_WINDOW, BUY_MODAL_POS[0], BUY_MODAL_POS[1], BUY_MODAL_POS[2], BUY_MODAL_POS[3])), threshold=threshold, showDiff=False):
                return 'buy'
            if not compareImage(SELL_MODAL_IMAGE, imageToArr(capture_window_region(TARGET_WINDOW,  SELL_MODAL_POS[0], SELL_MODAL_POS[1], SELL_MODAL_POS[2], SELL_MODAL_POS[3])), threshold=threshold, showDiff=False):
                return 'sell'
            
        elif until == 'close':
            if not compareImage(CLOSE_MODAL_IMAGE, imageToArr(capture_window_region(TARGET_WINDOW, CLOSE_MODAL_POS[0], CLOSE_MODAL_POS[1], CLOSE_MODAL_POS[2], CLOSE_MODAL_POS[3])), threshold=threshold, showDiff=False):
                return True  
            
def timing_capture(pos):
    start = time.time()
    index = 0
    while time.time() - start <= 5:
        image = capture_window_region(TARGET_WINDOW, pos[0], pos[1], pos[2], pos[3])
        saveImage(image, f'timing_captures/{index}.png')
        index +=1

def waitModal_v4(template, pos):
    currentImg = capture_window_region(TARGET_WINDOW, pos[0], pos[1], pos[2], pos[3])
    
    start = time.time()
    while compareImage_v2(template, imageToArr(currentImg), threshold=0.85):
        if time.time() - start >= 2:
            return False
            
        currentImg = capture_window_region(TARGET_WINDOW, pos[0], pos[1], pos[2], pos[3])
        # print("Đang chờ modal mở...")
    # signatureImg = capture_window_region(TARGET_WINDOW, pos[0], pos[1], pos[2], pos[3])
    
    maxPriceImage = capture_window_region(TARGET_WINDOW, 1200, 382, 100, 24)
    # resultImg = capture_window(TARGET_WINDOW)
    # saveImage(signatureImg, 'templates/1600x1900/signatureImg.png')
    # saveImage(maxPriceImage, 'templates/1600x1900/maxPriceImage.png')
    return maxPriceImage
    


# 1265, 538, 40, 40
# buyModalImage_1600x900 = cv2.imread('./templates/1600x1900/buy_modal.png') 
# buyModalImage_1600x900 = cv2.imread('./templates/1600x1900/163.png') 
buyModalImage_1600x900 = cv2.imread('./templates/1600x1900/170.png') 

def runOnTransactions_v4(resetTimes=[]):
    numRow = len(resetTimes)

    prevPrice = [None] * numRow
    currentPrice = None

    updated = [False] * numRow

    row = 0
    while True:
        time.sleep(0.25)

        os.system('cls')
        print(f"👉 Dòng {row + 1}")

        # KIỂM TRA CÓ ĐANG TRONG GIỜ RESET KHÔNG ?
        message = time_until_reset(resetTimes[row], offset=20)
        # print(message, isinstance(message, str))
        if isinstance(message, str):
            print(message)

            updated[row] = False
            row = row + 1 if row < numRow - 1 else 0
            continue

        # KIỂM TRA ĐÃ CẬP NHẬT GIÁ Ở ĐỢT RESET NÀY CHƯA ?
        if updated[row]:
            row = row + 1 if row < numRow - 1 else 0
            continue


        # Click vào row
        # single_click(TARGET_WINDOW, 1249, 258 + row * 52, draw=f'row_{row}.png')
        multi_click(1249, 258 + row * 52, 2, rand_x=True, rand_y=False)

        # Chờ Modal mở
        currentPrice = waitModal_v4(buyModalImage_1600x900, [1270, 536, 35, 44])
        if not currentPrice:
            single_click(TARGET_WINDOW, 1214, 724)
            continue

        # timing_capture([1270, 536, 35, 44])

        # testRow = row + 1 if row + 1 < numRow else 0
        testRow = row
        if prevPrice[testRow]:
            isDiff = compareImage_v2(imageToArr(prevPrice[testRow]), imageToArr(currentPrice), threshold=0.75, showScore=True)
            # isDiff = compareImage(imageToArr(prevPrice[testRow]), imageToArr(currentPrice), threshold=80)
            # print(f'{row+1}: Thay đổi' if isDiff else f'{row+1}: Không thay đổi')

            # Giá đã thay đổi
            if isDiff:
                
                single_click(TARGET_WINDOW, 1284, 395)
                time.sleep(0.05)
                single_click(TARGET_WINDOW, 1034, 725)
                time.sleep(0.05)
                send_key(TARGET_WINDOW, KEY_CODES['ESC'])
                updated[testRow] = True

                # saveImage(prevPrice[testRow], 'DIFF_prevPrice.png')
                # saveImage(currentPrice, 'DIFF_currentPrice.png')
                # return 
                pass
        
        prevPrice[row] = currentPrice
        

        # Tắt modal
        single_click(TARGET_WINDOW, 1214, 724)

        # return 
        # waitModal_v3(until='close')

           
        row = row + 1 if row < numRow - 1 else 0

    pass


RESET_TIME = {
    "Scamacca": toResetTime("Chẵn 18 - Chẵn 38"),
    "Correa": toResetTime("Chẵn 15 - Chẵn 35"),
    "Unal": toResetTime("Chẵn 01 - Chẵn 21"),
    "Anguissa": toResetTime("Chẵn 20 - Chẵn 40"),
    "Awoniyi": toResetTime("Chẵn 06 - Chẵn 26")
}

def main():
    resetTimes = [RESET_TIME['Scamacca'], RESET_TIME['Correa'], RESET_TIME['Unal']]

    

    # for  rst in resetTime:
    #     print(time_until_reset(rst, offset=20))

    # runOnTransactions_v2(buyMaxOnTransaction, 'buy', len(resetTime), resetTime)
    # runOnTransactions_v3(numRow=3)
    # runOnFavourite(1)
    # captureTemplate([536, 205, 26, 15], 'buy_modal_bigger.png')


    runOnTransactions_v4(resetTimes)

    # img1 = cv2.imread('./DIFF_prevPrice.png') 
    # # img2 = cv2.imread('./prevPrice.png') 
    # img2 = cv2.imread('./DIFF_currentPrice.png') 

    # res = compareImage_v2(img1, img2, threshold=0.9, showDiff=False)
    # print(res)



    # NEW TEMPLATE
    # captureTemplate([1059, 314, 33, 20], 'buy_modal_backup.png')
    # captureTemplate([647, 344, 73, 16], 'spam_error.png')
    
    # TEST
    # testImage([962, 315, 77, 54], BUY_MODAL_IMAGE)


    # for i in range(0,5):
    #     single_click(TARGET_WINDOW,466, 250 + i * 41, draw=f'draw_{i}.png')

    
    pass


if __name__ == '__main__':
    main()
