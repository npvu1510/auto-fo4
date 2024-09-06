import os
import time

# my modules
from constants import *
from utils import *
from timeCheck import time_until_reset


# ---------------------------------------------------------------- DEVELOPMENT FUNCTIONS ----------------------------------------------------------------
def timing_capture(pos):
    start = time.time()
    index = 0
    while time.time() - start <= 5:
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
        if compareImage_v2(imageToArr(currentPrice), HYPHEN_IMAGE, showDiff=False, threshold=0.85):
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


def waitingForModal(template, pos, appear = True, timeout = 2, threshold = 0.85, showScore = False):
    currentImg = capture_window_region(TARGET_WINDOW, pos[0], pos[1], pos[2], pos[3])
    
    start = time.time()
    while (compareImage_v2(template, imageToArr(currentImg), threshold=threshold, showScore=showScore)
           if appear else not compareImage_v2(template, imageToArr(currentImg), threshold=threshold, showScore=showScore)):
    # while compareImage(template, imageToArr(currentImg), threshold=30):
    
        if time.time() - start >= timeout:
            return False
            
        currentImg = capture_window_region(TARGET_WINDOW, pos[0], pos[1], pos[2], pos[3])
        # print("Đang chờ modal mở...")
    
    # maxPriceImage = capture_window_region(TARGET_WINDOW, 1240, 382, 43, 24)
    maxPriceImage = capture_window_region(TARGET_WINDOW, 1220, 382, 66, 22)
    # saveImage(maxPriceImage, 'maxPriceImage.png')

    return maxPriceImage
    
# ---------------------------------------------------------------- FAVORORITES FUNCTIONS ----------------------------------------------------------------
def runOnFavourite(resetTimes = None, autoCancel = False , grades = None):
    if autoCancel and len(resetTimes) > 1:
        print('⚠️ Chức năng auto cancel phải được bật để có thể chèn nhiều hơn 1 cầu thủ !')
        exit(1)

    prevPrice = currentPrice = updated = None
    failed = False
    playerIdx = 0

    # Khởi đầu với cầu thủ đầu tiên trong "DS yêu thích"
    single_click(TARGET_WINDOW, 406, 254)
    while True:
        # KIỂM TRA CẦU THỦ ĐÃ VỀ HÀNG CHƯA ?
        isFinishedOrder = checkNotification()
        if not isFinishedOrder:
            playerIdx+=1

            if playerIdx == len(resetTimes):
                os.system('shutdown -s')

            # Chuyển sang cầu thủ tiếp theo
            single_click(TARGET_WINDOW, 406, 254 + playerIdx * 40)
            prevPrice = currentPrice = updated = None
            failed = False


        # os.system('cls')
        # print(f"🔃 ĐANG CHÈN CẦU THỦ THỨ #{playerIdx}...")

        # KIỂM TRA CÓ GẶP LỖI KHÔNG ?
        if not (compareImage(imageToArr(capture_window_region(TARGET_WINDOW, 782, 422, 118, 22)), SPAM_ERROR_1600_1900)):
            single_click(TARGET_WINDOW, 902, 590)
            time.sleep(300)
            return
        
        # KIỂM TRA CÓ ĐANG TRONG GIỜ RESET KHÔNG ?
        if resetTimes[playerIdx]:
            message = time_until_reset(resetTimes[playerIdx], offset=10)
            if isinstance(message, str):
                print(f'⌚ {message}')

                updated = False
                time.sleep(30)
                continue
            else:
                if autoCancel and failed:
                    cancelFirstOrder()
                    failed = False

         # KIỂM TRA ĐÃ CẬP NHẬT GIÁ Ở ĐỢT  NÀY CHƯA ?
        if updated:
            print("✅ GIÁ ĐÃ ĐƯỢC CẬP NHẬT")
            continue
        
        # CLICK MỞ MODAL
        single_click(TARGET_WINDOW, 1110, 828)
        currentPrice = waitingForModal(BUY_MODAL_1600_1900, [1278, 566, 25, 16])
        if not currentPrice:
            print('⏰ TIMEOUT KHI MỞ MODAL')
            # single_click(TARGET_WINDOW, 1214, 724)
            send_key(TARGET_WINDOW, KEY_CODES['ESC'])
            waitingForModal(BUY_MODAL_CLOSED_1600_1900,[523, 169, 23, 17])
            continue
    
        # timing_capture([1239, 545, 37, 30])
        # timing_capture([1278, 566, 25, 16])
        # return 
    
        # KIỂM TRA GIÁ
        if prevPrice:
            isDiff = compareImage_v2(imageToArr(prevPrice), imageToArr(currentPrice), threshold=0.8, showScore=True)
            # saveImage(prevPrice, f'prevPrice_{time.time()}.png')
            # saveImage(currentPrice, f'currentPrice_{time.time()}.png')
            # print(f'Thay đổi' if isDiff else f'Không thay đổi')
            if isDiff:
                exit()

            # if isDiff:
            # # if True:
            #     # Giá đã thay đổi
            #     single_click(TARGET_WINDOW, 1284, 395)
            #     single_click(TARGET_WINDOW, 1034, 725)
            #     waitingForModal(BUY_MODAL_CLOSED_1600_1900,[523, 169, 23, 17], timeout=10)
            #     time.sleep(3)

            #     saveImage(capture_window(TARGET_WINDOW), f'updated_{time.time()}.png')

            #     # Kiểm tra xem có tranh được slot 1 không ? Nếu không lát sẽ hủy, để có lại BP
            #     failed = not checkingToCancelOrder(grades[playerIdx])

            #     # Đánh dấu là đã cập nhật ở lần reset này rồi
            #     if resetTimes[playerIdx]:
            #         updated = True   
        
        prevPrice = currentPrice
        
        # Tắt modal
        # single_click(TARGET_WINDOW, 1214, 724)        
        send_key(TARGET_WINDOW, KEY_CODES['ESC'])
        waitingForModal(BUY_MODAL_CLOSED_1600_1900,[523, 169, 23, 17])

def checkingToCancelOrder(grade = 1):
    templateSlot = cv2.imread(f'./templates/1600x900/slot_1.png')

    currentSlotImage = capture_window_region(TARGET_WINDOW, 1159, 464 + 34 * (grade - 1) - int(0.5 * grade), 22, 34)
    saveImage(currentSlotImage, 'currentSlotImage.png')

    return not compareImage_v2(templateSlot, imageToArr(currentSlotImage), threshold=0.75)

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
    res = compareImage_v2(BADGE_1600_1900, imageToArr(currentBadge))
    if not res:
        print('🎉 Cầu thủ đã về')
        single_click(TARGET_WINDOW, 828, 178)
        time.sleep(5)
        single_click(TARGET_WINDOW, 665, 183)
    
    return res


# ---------------------------------------------------------------- TRANSACTION FUNCTIONS ----------------------------------------------------------------


def runOnTransactions_v4(resetTimes=[]):
    numRow = len(resetTimes)

    prevPrice = [None] * numRow
    currentPrice = None

    updated = [False] * numRow

    row = 0
    # startCountdown = time.time()
    while True:
        # if time.time() - startCountdown >= 300:
        #     print("Đang tạm dừng tránh spam...")
        #     time.sleep(30)
        #     startCountdown = time.time()

        # KHỞI ĐẦU MỖI DÒNG
        os.system('cls')
        print(f"👉 Dòng {row + 1}")

        # KIỂM TRA CÓ GẶP LỖI KHÔNG ?
        if not (compareImage(imageToArr(capture_window_region(TARGET_WINDOW, 782, 422, 118, 22)), SPAM_ERROR_1600_1900)):
            single_click(TARGET_WINDOW, 902, 590)
            time.sleep(300)
            return

        # KIỂM TRA CÓ ĐANG TRONG GIỜ RESET KHÔNG ?
        if resetTimes[row]:
            message = time_until_reset(resetTimes[row], offset=10)
            if isinstance(message, str):
                print(message)

                updated[row] = False
                
                row = row + 1 if row < numRow - 1 else 0
                continue

        # KIỂM TRA ĐÃ CẬP NHẬT GIÁ Ở ĐỢT RESET NÀY CHƯA ?
        if resetTimes[row] and updated[row]:
            print("Giá đã được cập nhật rồi")

            row = row + 1 if row < numRow - 1 else 0
            continue


        # Click vào row
        # single_click(TARGET_WINDOW, 1249, 258 + row * 52, draw=f'row_{row}.png')
        multi_click(1249, 258 + row * 52, 2, rand_x=True, rand_y=False)

        # Chờ Modal mở
        currentPrice = waitingForModal(BUY_MODAL_1600_1900, [1270, 536, 35, 44])
        if not currentPrice:
            single_click(TARGET_WINDOW, 1214, 724)

            time.sleep(0.25)
            continue

        # timing_capture([1270, 536, 35, 44])
        # return 

        # testRow = row + 1 if row + 1 < numRow else 0
        if prevPrice[row]:
            isDiff = compareImage_v2(imageToArr(prevPrice[row]), imageToArr(currentPrice), threshold=0.95, showScore=True)
            # print(f'{row+1}: Thay đổi' if isDiff else f'{row+1}: Không thay đổi')

            # Giá đã thay đổi
            if  isDiff:                
                single_click(TARGET_WINDOW, 1284, 395)
                time.sleep(0.01)
                single_click(TARGET_WINDOW, 1034, 725)
                saveImage(capture_window(TARGET_WINDOW), f'updated_{time.time()}.png')
                time.sleep(0.1)

                send_key(TARGET_WINDOW, KEY_CODES['ESC'])

                updated[row] = True
                

                # FOR DEBUGGING
                saveImage(prevPrice[row], f'prevPrice_{row}_{time.time()}.png')
                saveImage(currentPrice, f'currentPrice_{time.time()}.png')
                # return 
                time.sleep(2)
                pass
        
        prevPrice[row] = currentPrice
        
        # Tắt modal
        single_click(TARGET_WINDOW, 1214, 724)           

        row = row + 1 if row < numRow - 1 else 0
        time.sleep(0.25)


def main():
    # time.sleep(1800)
    # resetTimes = [RESET_TIME['Banega'], RESET_TIME['Nunes']]
    
    # runOnTransactions_v4(resetTimes)
    # runOnFavourite(RESET_TIME['Suarez'])
    runOnFavourite([RESET_TIME['Suarez'], False], grades= [4,4], autoCancel= True)


    # NEW TEMPLATE
    # captureTemplate([int(576 * a), int(ORDER_ROW_POS[0] * a) - 6, int(80 * a), int(16 * a)], 'hyphen.png')
    # captureTemplate([782, 422, 118, 22], 'spam_error.png')
    # captureTemplate([1159, 464, 22, 34], 'slot_1.png')
    # captureTemplate([785, 165, 11, 10], 'badge.png')

    # TEST TEMPLATE
    # testImage([785, 165, 11, 10], BADGE_1600_1900, threshold=0.7)
    

    # grade = 10
    # res = checkingToCancelOrder(grade)
    # print('Đã chèn slot 1' if res else 'Không chèn được slot 1')
    # if not res:
        # cancelFirstOrder()





if __name__ == '__main__':
    main()
