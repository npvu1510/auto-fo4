import os
import time

# my modules
from constants import *
from utils import *
from timeCheck import time_until_reset


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


def waitingForBuyModal(template, pos, appear = True, timeout = 2, threshold = 0.85, showScore = False):
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
def checkParamsFavorites(resetTimes, grades, quantities, autoCancel):
    if not resetTimes:
        raise ValueError("⚠️ Giờ reset của các thẻ không tồn tại")

    if not type(resetTimes) == list:
        raise TypeError("⚠️ Giờ reset các thẻ cần chèn phải là mảng")
    
    playerLength = len(resetTimes)

    if not quantities:
        quantities = [1] * playerLength
    else:
        if not type(quantities) == list:
            raise TypeError("⚠️ Số lượng cần chèn phải là mảng")
        
        if len(quantities)!= playerLength:
            raise ValueError(f"⚠️ Có {playerLength} thẻ cần chèn, nhưng số lượng cần chèn là {len(quantities)}")
        

    isAllQuantitiesEqualOne = False
    if autoCancel is None:
        raise ValueError("⚠️ Chưa chỉ định chế độ tự động hủy đặt thẻ")
    else:
        if autoCancel:
            for i in range(0, playerLength - 1):
                if not resetTimes[i]:
                    raise ValueError(f"⚠️ Chế độ auto cancel yêu cầu các thẻ (trừ thẻ cuối) phải cung cấp giờ reset")
            
            if playerLength > 1:
                for i in range(0, playerLength - 1):
                    if quantities[i] > 1:
                        raise ValueError(f"⚠️ Chế độ auto cancel yêu cầu các thẻ (trừ thẻ cuối) chỉ mua số lượng là 1 hoặc chỉ được chèn duy nhất 1 thẻ !")
                isAllQuantitiesEqualOne = True
                
    
    if not grades:
        grades = [1] * playerLength
    else:
        if not type(grades) == list:
            raise TypeError("⚠️ Số lượng cộng các thẻ phải là mảng")
        
        if len(grades)!= playerLength:
            raise ValueError(f"⚠️ Có {playerLength} thẻ cần chèn, nhưng số lượng cộng là {len(grades)}")
    
    
    return grades, quantities, isAllQuantitiesEqualOne

def initFavorites(hasCancelFlag = False):
    prevPrice = currentPrice = updated = None

    if not hasCancelFlag:
        return prevPrice, currentPrice, updated
    else:
        return prevPrice, currentPrice, updated, False

def buyOnFavorites(resetTimes, grades = None, quantities = None, autoCancel = True, intervalDelay= 300,delayDuration = 30):
    grades, quantities, isAllQuantitiesEqualOne = checkParamsFavorites(resetTimes  , grades , quantities  , autoCancel)
    prevPrice, currentPrice, updated, needToCancel = initFavorites(hasCancelFlag=True)

    # # Khởi đầu với cầu thủ đầu tiên trong "DS yêu thích"
    # single_click(TARGET_WINDOW, 406, 254)

    playerIdx = 0
    start = time.time()
    while True:
        
        # NẾU SĂN MỖI THẺ 1 CON ĐỂ BUILD ĐỘI HÌNH => KIỂM TRA VỀ HÀNG => CHUYỂN SANG CON TIẾP THEO
        if isAllQuantitiesEqualOne: 
            isFinishedOrder = checkNotification()
            if not isFinishedOrder:
                playerIdx+=1

                if playerIdx == len(resetTimes):
                    os.system('shutdown -s')

                # Chuyển sang cầu thủ tiếp theo
                single_click(TARGET_WINDOW, 406, 254 + playerIdx * 40)
                prevPrice, currentPrice, updated, needToCancel = initFavorites(hasCancelFlag=True)
            

        os.system('cls')
        print(f"🔃 ĐANG CHÈN CẦU THỦ THỨ #{playerIdx + 1}...")

        
        # NẾU CÓ RESET TIME => KIỂM TRA CÓ ĐANG TRONG GIỜ RESET KHÔNG ?
        if resetTimes and resetTimes[playerIdx]:
            message = time_until_reset(resetTimes[playerIdx], offset=10)

            # Ngoài giờ reset
            if isinstance(message, str):
                print(f'⌚ {message}')

                prevPrice, currentPrice, updated = initFavorites()

                time.sleep(30)
                continue
            
            # Trong giờ reset và cập nhật trong đợt này rồi
            if updated:
                print("✅ GIÁ ĐÃ ĐƯỢC CẬP NHẬT")
                continue
        
        # NẾU KHÔNG CÓ RESET TIME => DELAY SAU MỘT KHOẢNG => TRÁNH SPAM
        else:
            if time.time() - start >= intervalDelay:
                time.sleep(delayDuration)
                start = time.time()

         # NẾU CÓ BẬT AUTO CANCEL VÀ CÓ CỜ CANCEL (CHỈ TỒN TẠI KHI ĐÃ CẬP NHẬT)
        if autoCancel and needToCancel:
            needToCancel = False
            cancelFirstOrder()
        

        # CLICK MỞ MODAL 
        single_click(TARGET_WINDOW, 1110, 828)
        currentPrice = waitingForBuyModal(BUY_MODAL_1600_1900, [1278, 566, 25, 16])

        # Nếu modal chưa mở => có thể do lỗi spam hoặc timeout
        if not currentPrice:
            # Kiểm tra lỗi spam
            if not (compareImage_v2(imageToArr(capture_window_region(TARGET_WINDOW, 782, 422, 118, 22)), SPAM_ERROR_1600_1900, threshold=0.7, showScore=True)):
                # single_click(TARGET_WINDOW, 902, 590)
                print("⌚ ĐANG GẶP LỖI SPAM CHỜ 60 GIÂY...")
                time.sleep(300)

                send_key(TARGET_WINDOW, KEY_CODES['ESC'])
                time.sleep(0.2)
                
            # Kiểm tra lỗi timeout
            else:
                print('⏰ TIMEOUT KHI MỞ MODAL')
                # single_click(TARGET_WINDOW, 1214, 724)
                send_key(TARGET_WINDOW, KEY_CODES['ESC'])
                waitingForBuyModal(MODAL_CLOSED_1600_1900,[523, 169, 23, 17])
            continue
    
        # timing_capture([1239, 545, 37, 30])
        # timing_capture([1278, 566, 25, 16])
        # return 
    
        # KIỂM TRA THÔNG TIN MODAL (GIÁ)
        if prevPrice:
            isDiff = compareImage_v2(imageToArr(prevPrice), imageToArr(currentPrice), threshold=0.8, showScore=True)
            # saveImage(prevPrice, f'prevPrice_{time.time()}.png')
            # saveImage(currentPrice, f'currentPrice_{time.time()}.png')
            # print(f'Thay đổi' if isDiff else f'Không thay đổi')

            # Giá đã thay đổi
            if isDiff:
            # if True:
                # Chọn giá
                single_click(TARGET_WINDOW, 1284, 395)
                # single_click(TARGET_WINDOW, 1245, 556)
                
                # Nếu mua nhiều
                if quantities[playerIdx] - 1 > 0:
                    multi_click(1284, 551, quantities[playerIdx] - 1, rand_x=True)
                
                # Bấm mua
                single_click(TARGET_WINDOW, 1034, 725)

                saveImage(capture_window(TARGET_WINDOW), f'before_{time.time()}.png')
                waitingForBuyModal(MODAL_CLOSED_1600_1900,[523, 169, 23, 17], timeout=10)
                time.sleep(3)
                saveImage(capture_window(TARGET_WINDOW), f'after_{time.time()}.png')


                # Nếu có reset time => đánh dấu đã cập nhật trong lần này
                if resetTimes[playerIdx]:
                    updated = True  

                # nếu có auto cancel => kiểm tra có cần phải cancel order trong lần reset kế hay không ?
                if autoCancel:
                    needToCancel = not checkingToCancelOrder(grades[playerIdx])
        
        prevPrice = currentPrice
        
        # Tắt modal
        # single_click(TARGET_WINDOW, 1214, 724)        
        send_key(TARGET_WINDOW, KEY_CODES['ESC'])
        waitingForBuyModal(MODAL_CLOSED_1600_1900,[523, 169, 23, 17])


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


# ---------------------------------------------------------------- SELL ON FAVOURITES FUNCTIONS ----------------------------------------------------------------
def waitingForSellModal(template, pos, appear = True, timeout = 2, threshold = 0.85, showScore = False):
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
    priceImage = capture_window_region(TARGET_WINDOW, 1211, 390, 78, 28)
    # saveImage(priceImage, 'maxPriceImage.png')

    return priceImage

# def sellOnFavorites(resetTime, grade = 1):
#     prevPrice = currentPrice = updated = None
#     cancelFirstOrder = False


#     while True:
#         os.system('cls')
#         print(f"🔃 ĐANG BÁN CẦU THỦ...")

        
#         # KIỂM TRA CÓ ĐANG TRONG GIỜ RESET KHÔNG ?
#         if resetTime:
#             message = time_until_reset(resetTime, offset=10)
#             if isinstance(message, str):
#                 print(f'⌚ {message}')

#                 prevPrice, currentPrice, updated = initFavorites()

#                 time.sleep(30)
#                 continue


#          # KIỂM TRA ĐÃ CẬP NHẬT GIÁ Ở ĐỢT NÀY CHƯA ?
#         if updated:
#             print("✅ ĐÃ CHÈN RỒI !")
#             continue
#         else:
#             if cancelfirstOrder:
#                 cancelfirstOrder = False
#                 cancelFirstOrder()
        

#         # Click vào row
#         multi_click(1249, 258 + row * 52, 2, rand_x=True, rand_y=False)
#         # timing_capture([941, 519, 34, 19])

#         currentPrice = waitingForSellModal(SELL_MODAL_OPENED_1600_1900, [941, 519, 34, 19], threshold=0.95)
#         if not currentPrice:
#             # KIỂM TRA CÓ GẶP LỖI KHÔNG ?
#             if not (compareImage_v2(imageToArr(capture_window_region(TARGET_WINDOW, 782, 422, 118, 22)), SPAM_ERROR_1600_1900, threshold=0.7, showScore=True)):
#                 # single_click(TARGET_WINDOW, 902, 590)
#                 print("⌚ ĐANG GẶP LỖI SPAM CHỜ 60 GIÂY...")
#                 time.sleep(300)

#                 send_key(TARGET_WINDOW, KEY_CODES['ESC'])
#                 time.sleep(0.2)
                
#             # KHÔNG GẶP LỖI => TIMEOUT
#             else:
#                 print('⏰ TIMEOUT KHI MỞ MODAL')
#                 # single_click(TARGET_WINDOW, 1214, 724)
#                 send_key(TARGET_WINDOW, KEY_CODES['ESC'])
#                 waitingForBuyModal(MODAL_CLOSED_1600_1900,[523, 169, 23, 17])
#             continue
        
#         if prevPrice:
#             isDiff = compareImage_v2(imageToArr(prevPrice), imageToArr(currentPrice), threshold=0.75, showScore=True)
#             saveImage(prevPrice, f'prevPrice_{time.time()}.png')
#             saveImage(currentPrice, f'currentPrice_{time.time()}.png')

#             print('Nhảy giá' if isDiff else 'Chưa nhảy giá')
#             if isDiff:
#                 single_click(TARGET_WINDOW, 1264, 404)
#                 single_click(TARGET_WINDOW, 1046, 762)

#                 saveImage(capture_window(TARGET_WINDOW), f'before_{time.time()}.png')

#                 waitingForSellModal(MODAL_CLOSED_1600_1900,[523, 169, 23, 17], timeout=1)
#                 time.sleep(3)

#                 saveImage(capture_window(TARGET_WINDOW), f'after_{time.time()}.png') 
                
#                 # Cập nhật biến
#                 if resetTime:
#                     updated = True
#                 cancelFirstOrder = True

#         prevPrice = currentPrice
        
#         send_key(TARGET_WINDOW, KEY_CODES['ESC'])
#         waitingForSellModal(MODAL_CLOSED_1600_1900,[523, 169, 23, 17], timeout=1)



# ---------------------------------------------------------------- TRANSACTION FUNCTIONS ----------------------------------------------------------------
def runOnMyTransactions(resetTimes=[], intervalDelay= 300,delayDuration=30):
    numRow = len(resetTimes)

    prevPrice = [None] * numRow
    currentPrice = None

    updated = [False] * numRow

    row = 0
    start = time.time()
    while True:
        # KHỞI ĐẦU MỖI DÒNG
        os.system('cls')
        print(f"👉 Dòng {row + 1}")

        # NẾU CÓ RESET TIME => KIỂM TRA CÓ ĐANG TRONG GIỜ RESET KHÔNG ?
        if resetTimes and resetTimes[row]:
            message = time_until_reset(resetTimes[row], offset=10)

            # Ngoài giờ reset
            if isinstance(message, str):
                print(f'⌚ {message}')

                prevPrice, currentPrice, updated = initFavorites()

                row = row + 1 if row < numRow - 1 else 0
                continue
            
            # Trong giờ reset và cập nhật trong đợt này rồi
            if updated:
                print("✅ GIÁ ĐÃ ĐƯỢC CẬP NHẬT")

                row = row + 1 if row < numRow - 1 else 0
                continue
        
        # NẾU KHÔNG CÓ RESET TIME => DELAY SAU MỘT KHOẢNG => TRÁNH SPAM
        else:
            if time.time() - start >= intervalDelay:
                time.sleep(delayDuration)
                start = time.time()

        # Click vào row
        multi_click(1249, 258 + row * 52, 2, rand_x=True, rand_y=False)

        # Chờ Modal mở
        currentPrice = waitingForBuyModal(BUY_MODAL_1600_1900, [1278, 566, 25, 16])
        if not currentPrice:
            # KIỂM TRA CÓ GẶP LỖI KHÔNG ?
            if not (compareImage_v2(imageToArr(capture_window_region(TARGET_WINDOW, 782, 422, 118, 22)), SPAM_ERROR_1600_1900, threshold=0.7, showScore=True)):
                # single_click(TARGET_WINDOW, 902, 590)
                print("⌚ ĐANG GẶP LỖI SPAM CHỜ 60 GIÂY...")
                time.sleep(300)

                send_key(TARGET_WINDOW, KEY_CODES['ESC'])
                time.sleep(0.2)
                
            # KHÔNG GẶP LỖI => TIMEOUT
            else:
                print('⏰ TIMEOUT KHI MỞ MODAL')
                # single_click(TARGET_WINDOW, 1214, 724)
                send_key(TARGET_WINDOW, KEY_CODES['ESC'])
                waitingForBuyModal(MODAL_CLOSED_1600_1900,[523, 169, 23, 17])
            continue

        # timing_capture([1270, 536, 35, 44])
        # return 

        # testRow = row + 1 if row + 1 < numRow else 0
        if prevPrice[row]:
            isDiff = compareImage_v2(imageToArr(prevPrice[row]), imageToArr(currentPrice), threshold=0.8, showScore=True)
            # print(f'{row+1}: Thay đổi' if isDiff else f'{row+1}: Không thay đổi')

            # Giá đã thay đổi
            if  isDiff:                
                single_click(TARGET_WINDOW, 1284, 395)
                single_click(TARGET_WINDOW, 1034, 725)

                time.sleep(0.1)
                saveImage(capture_window(TARGET_WINDOW), f'updated_{time.time()}.png')
                waitingForBuyModal(MODAL_CLOSED_1600_1900,[523, 169, 23, 17])                

                # FOR DEBUGGING
                saveImage(prevPrice[row], f'prevPrice_{row}_{time.time()}.png')
                saveImage(currentPrice, f'currentPrice_{time.time()}.png')
                
                time.sleep(2)

                
                updated[row] = True

        
        prevPrice[row] = currentPrice
        
        # Tắt modal
        # single_click(TARGET_WINDOW, 1214, 724)           
        send_key(TARGET_WINDOW, KEY_CODES['ESC'])
        waitingForBuyModal(MODAL_CLOSED_1600_1900,[523, 169, 23, 17])

        row = row + 1 if row < numRow - 1 else 0



def main():
    # time.sleep(1800)
    # resetTimes = [RESET_TIME['Banega'], RESET_TIME['Nunes']]
    
    # runOnMyTransactions([False])
    # runOnFavourite(RESET_TIME['Suarez'])
    # runOnFavourite([RESET_TIME['Suarez'], False], grades= [4,4], autoCancel= True)
    buyOnFavorites([False, False], grades= [4,4], autoCancel= False)


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
