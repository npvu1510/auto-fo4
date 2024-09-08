import os
import time

# my modules
from constants import *
from utils import *
from timeFns import time_until_reset


# ---------------------------------------------------------------- DEVELOPMENT FUNCTIONS ----------------------------------------------------------------
def timing_capture(pos, duration = 5):
    start = time.time()
    index = 0
    while time.time() - start <= duration:
        image = capture_window_region(TARGET_WINDOW, pos[0], pos[1], pos[2], pos[3])
        saveImage(image, f'timing_captures/{index}.png')
        index +=1




# ---------------------------------------------------------------- OTHERS ----------------------------------------------------------------
def isAvailableBuySlot():
    # Lấy giá đầu tiên
    initPrice = capture_window_region(TARGET_WINDOW, 930, 500, 106, 30)

    i = 0
    while i < 8:
        # Lấy giá dòng hiện tại
        currentPrice = capture_window_region(TARGET_WINDOW, 576, ORDER_ROW_POS[i], 80, 16)
        # currentPrice = capture_window_region(TARGET_WINDOW, int(576 * a), int(ORDER_ROW_POS[i] * a) - 6, int(80 * a), int(16 * a))
        
        # Nếu gặp dòng đầu tiên không phải gạch nối
        # if compareImage(imageToArr(currentPrice), HYPHEN_IMAGE, showDiff=False, threshold=100):
        if compareImage_v2(imageToArr(currentPrice), HYPHEN_IMAGE, showDiff=False, threshold=0.85)[0]:
            break

        i+=1
    
    # Nếu chưa có ai đặt => còn slot
    if i == 8:
        return True
    
    print(i)
    single_click(TARGET_WINDOW , 576, ORDER_ROW_POS[i] + 8)
    time.sleep(0.075)

    currentPrice = capture_window_region(TARGET_WINDOW, 930, 500, 106, 30)

    # Nếu true => còn slot , ngược lại => hết slot
    res = compareImage(imageToArr(initPrice), imageToArr(currentPrice), threshold=100, showDiff=False)

    # saveImage(initPrice, f'init_{time.time()}.png')
    # saveImage(currentPrice, f'current_{time.time()}.png')

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



    
# ---------------------------------------------------------------- FAVORORITES FUNCTIONS ----------------------------------------------------------------

def spamCheck(delayDurationInMinutes = 10):
    # Kiểm tra lỗi spam
    if not (compareImage_v2(imageToArr(capture_window_region(TARGET_WINDOW, SPAM_ERROR_POS)), SPAM_ERROR_1600_1900, threshold=0.8, showScore=True)[0]):
        print(f"⌚ ĐANG GẶP LỖI SPAM CHỜ {delayDurationInMinutes} PHÚT...")
        time.sleep(delayDurationInMinutes * 60)

        closeAndWait()
        time.sleep(1)
        
    # Kiểm tra lỗi timeout
    else:
        print('⏰ TIMEOUT KHI MỞ MODAL')
        closeAndWait()

def waitingForModalOpen(openClick, timeout=2):
    # single_click(TARGET_WINDOW, BUY_BUTTON_FAVORITES)
    isModalOpen = waitingFor(BUY_MODAL_OPEN_1600_1900, BUY_MODAL_OPEN_POS, threshold=OPEN_MODAL_THRESHOLD, timeout=timeout)


    # Nếu modal chưa mở => có thể do lỗi spam hoặc timeout
    if not isModalOpen:
        spamCheck()

    return True

def closeAndWait(timeout=1):
    # single_click(TARGET_WINDOW, 1214, 724)        
    send_key(TARGET_WINDOW, KEY_CODES['ESC'])
    waitingFor(MODAL_CLOSED_1600_1900,[523, 169, 23, 17], timeout=timeout, threshold=CLOSE_MODAL_THRESHOLD)


def delayAfterDuration(start, intervalInMinutes = 1, durationInSeconds = 5):
    if time.time() - start > intervalInMinutes * 60:
        print(f'🫸 TẠM DỪNG {durationInSeconds} GIÂY SAU MỖI {intervalInMinutes} PHÚT TRÁNH SPAM...')
        time.sleep(durationInSeconds)
        os.system('cls')
        return time.time()
    return start

def buyAndCapture(type='favorites'):
    single_click(TARGET_WINDOW, MAX_PRICE_BUTTON_BUY_MODAL)
    
    # # Tăng số lượng
    # if quantities[playerIdx] - 1 > 0:
    #     multi_click(INC_QUANTITY_BUTTON_BUY_MODAL, quantities[playerIdx] - 1, rand_x=True)
    
    # Bấm mua
    single_click(TARGET_WINDOW, BUY_BUTTON_BUY_MODAL)

    if type == 'favorites':
        saveImage(capture_window(TARGET_WINDOW), f'before_{time.time()}.png')
        waitingFor(MODAL_CLOSED_1600_1900, BUY_MODAL_CLOSE_POS)
        time.sleep(3)
        saveImage(capture_window(TARGET_WINDOW), f'after_{time.time()}.png')
    
    elif type == 'transactions':
        time.sleep(0.1)
        saveImage(capture_window(TARGET_WINDOW), f'updated_{time.time()}.png')
        waitingFor(MODAL_CLOSED_1600_1900,[523, 169, 23, 17])  


def buyOnFavorites(resetTime = None, grade = None, priceType = PRICE_TYPES['0'] , autoCancel = True):
    grade = grade if grade else 1

    # # Khởi đầu với cầu thủ đầu tiên trong "DS yêu thích"
    # single_click(TARGET_WINDOW, 406, 254)

    statCountDown = time.time()
    prevPrice = currentPrice = updated = needToCancel = None
    while True:
        os.system('cls')
        statCountDown = delayAfterDuration(statCountDown, intervalInMinutes=120, durationInSeconds=10)

        print(f"🔃 ĐANG CHÈN CẦU THỦ...")

        #  KIỂM TRA RESET TIME
        if resetTime:
            message = time_until_reset(resetTime, offset=5)
            # Ngoài giờ reset
            if isinstance(message, str):
                print(f'⌚ {message}')

                prevPrice = currentPrice = updated = None
                
                # Tạm dừng hạn chế chạy quá nhiều
                time.sleep(30)
                continue
            
            # Trong giờ reset và cập nhật trong đợt này rồi
            if updated:
                print("✅ GIÁ ĐÃ ĐƯỢC CẬP NHẬT")
                continue


         # AUTO CANCEL (CHỈ CHẠY VÀO KHI ĐÃ CÓ ÍT NHẤT 1 LẦN CẬP NHẬT)
        if autoCancel and needToCancel:
            needToCancel = False
            cancelFirstOrder()
        
        # CLICK MỞ MODAL 
        isModalOpen = waitingForModalOpen(single_click(TARGET_WINDOW, BUY_BUTTON_FAVORITES))
        currentPrice = capture_window_region(TARGET_WINDOW, priceType)
        if not isModalOpen:
            continue
        

        # KIỂM TRA THÔNG TIN MODAL (GIÁ)
        if prevPrice:
            isDiff = compareImage_v2(imageToArr(prevPrice), imageToArr(currentPrice), threshold=COMPARE_PRICE_THRESHOLD, showScore=True)[0]

            # saveImage(prevPrice, f'prevPrice_{time.time()}.png')
            # saveImage(currentPrice, f'currentPrice_{time.time()}.png')

            # Giá đã thay đổi
            if isDiff:
                buyAndCapture()

                # Nếu có reset time => đánh dấu đã cập nhật trong lần này
                if resetTime:
                    updated = True  

                # nếu có auto cancel => kiểm tra có cần phải cancel order trong lần reset kế hay không ?
                if autoCancel:
                    needToCancel = not checkingToCancelOrder(grade)
        
        prevPrice = currentPrice
        
        # Tắt modal
        closeAndWait()


def checkingToCancelOrder(grade = 1):
    x = ORDER_SLOT_RESULT[0]
    y = ORDER_SLOT_RESULT[1] + 34 * (grade - 1) - int(0.5 * grade)
    w = ORDER_SLOT_RESULT[2]
    h = ORDER_SLOT_RESULT[3]

    # currentSlotImage = capture_window_region(TARGET_WINDOW, 1159, 464 + 34 * (grade - 1) - int(0.5 * grade), 22, 34)
    currentSlotImage = capture_window_region(TARGET_WINDOW, x, y , w, h)
    # saveImage(currentSlotImage, 'currentSlotImage.png')

    return not compareImage_v2(SLOT_1_1600_1900, imageToArr(currentSlotImage), threshold=0.75)[0]

def cancelFirstOrder():
    single_click(TARGET_WINDOW, 828, 178)
    time.sleep(0.5)
    multi_click(1335, 256, rand_x=True)
    time.sleep(0.5)
    single_click(TARGET_WINDOW, 851, 622)
    time.sleep(0.5)
    send_key(TARGET_WINDOW, KEY_CODES['ESC'])
    time.sleep(0.5)
    single_click(TARGET_WINDOW, 665, 183)

def checkNotification():
    currentBadge = capture_window_region(TARGET_WINDOW, 785, 165, 11, 10)
    res = compareImage_v2(BADGE_1600_1900, imageToArr(currentBadge))[0]
    if not res:
        print('🎉 Cầu thủ đã về')
        single_click(TARGET_WINDOW, 828, 178)
        time.sleep(5)
        single_click(TARGET_WINDOW, 665, 183)
    
    return res


# ---------------------------------------------------------------- SELL ON FAVOURITES FUNCTIONS ----------------------------------------------------------------


# ---------------------------------------------------------------- TRANSACTION FUNCTIONS ----------------------------------------------------------------
# ---------------------------------------------------------------- TRANSACTION FUNCTIONS ----------------------------------------------------------------
def runOnMyTransactions(resetTimes=[], priceType=PRICE_TYPES['0']):
    numRow = len(resetTimes)

    prevPrice = [None] * numRow
    updated = [False] * numRow


    currentPrice = None
    statCountDown = time.time()
    row = 0
    while True:
        os.system('cls')

        statCountDown = delayAfterDuration(statCountDown, intervalInMinutes=3, durationInSeconds=10)
        
        print(f"👉 Dòng {row + 1}")

        #  KIỂM TRA RESET TIME
        if resetTimes[row]:
            message = time_until_reset(resetTimes[row], offset=5)
            # Ngoài giờ reset
            if isinstance(message, str):
                print(f'⌚ {message}')

                prevPrice[row] = currentPrice = updated[row] = None
                
                row = row + 1 if row < numRow - 1 else 0
                continue
            
            # Trong giờ reset và cập nhật trong đợt này rồi
            if updated:
                print("✅ GIÁ ĐÃ ĐƯỢC CẬP NHẬT")
                continue

        # CLICK MỞ MODAL 


        # Click vào row
        multi_click(1249, 258 + row * 52, 2, rand_x=True, rand_y=False)
        isModalOpen = waitingForModalOpen()
        currentPrice = capture_window_region(TARGET_WINDOW, priceType)
        if not isModalOpen:
            continue

        # timing_capture([1270, 536, 35, 44])
        # return 

        # testRow = row + 1 if row + 1 < numRow else 0
        if prevPrice[row]:
            isDiff = compareImage_v2(imageToArr(prevPrice[row]), imageToArr(currentPrice), threshold=0.8, showScore=True)[0]


            # Giá đã thay đổi
            if  isDiff:                
                buyAndCapture(type='transactions')

                # # FOR DEBUGGING
                # saveImage(prevPrice[row], f'prevPrice_{row}_{time.time()}.png')
                # saveImage(currentPrice, f'currentPrice_{time.time()}.png')
                                
                updated[row] = True

        prevPrice[row] = currentPrice
        
        # Tắt modal
        # single_click(TARGET_WINDOW, 1214, 724)           
        closeAndWait()

        row = row + 1 if row < numRow - 1 else 0


def main():
    # time.sleep(1800)
    # resetTimes = [RESET_TIME['Banega'], RESET_TIME['Nunes']]
    
    runOnMyTransactions([False])
    buyOnFavorites(None, grade= 8, priceType = PRICE_TYPES['10000'], autoCancel= True)


    # NEW TEMPLATE
    # captureTemplate([782, 422, 118, 22], 'spam_error.png')
    # captureTemplate([1159, 464, 22, 34], 'slot_1.png')
    # captureTemplate([785, 165, 11, 10], 'badge.png')

    # TEST TEMPLATE
    # testImage([785, 165, 11, 10], BADGE_1600_1900, threshold=0.7)


    # Compare
    # openModalAnDoSth(save = True)
    
    # continous open modal and compare
    # compareContinousSamePrice(openningThreshold= 0.9, stoppingThreshold=0.8)

    # compare 2 images from files
    # img1 = 'currentPrice_1725770660.4104366.png'
    # img2 = 'currentPrice_1725770666.7193506.png'
    # compareTwoImgRead(img1, img2, threshold= 0.95)

    # compareForTesting('currentPrice_1725768021.0782712.png', 'currentPrice_1725768039.3890417.png')

    pass

    


if __name__ == '__main__':
    main()
