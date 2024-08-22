import os
import time
# import cv2
# import playsound

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

# ---------------------------------------------------------------- FAVORORITES FUNCTIONS ----------------------------------------------------------------

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

# ---------------------------------------------------------------- TRANSACTION FUNCTIONS ----------------------------------------------------------------
     
def waitModal_v4(template, pos):
    currentImg = capture_window_region(TARGET_WINDOW, pos[0], pos[1], pos[2], pos[3])
    
    start = time.time()
    while compareImage_v2(template, imageToArr(currentImg), threshold=0.95):
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
    
# buyModalImage_1600x900 = cv2.imread('./templates/1600x1900/163.png') 

def runOnTransactions_v4(resetTimes=[]):
    numRow = len(resetTimes)

    prevPrice = [None] * numRow
    currentPrice = None

    updated = [False] * numRow

    row = 0
    while True:
        # KHỞI ĐẦU MỖI DÒNG
        os.system('cls')
        print(f"👉 Dòng {row + 1}")

        # KIỂM TRA CÓ GẶP LỖI KHÔNG ?
        if not (compareImage(imageToArr(capture_window_region(TARGET_WINDOW, 782, 422, 118, 22)), SPAM_ERROR_1600_1900)):
            single_click(TARGET_WINDOW, 902, 590)
            time.sleep(300)
            return

        # KIỂM TRA CÓ ĐANG TRONG GIỜ RESET KHÔNG ?
        message = time_until_reset(resetTimes[row], offset=10)
        if isinstance(message, str):
            print(message)

            updated[row] = False
            
            row = row + 1 if row < numRow - 1 else 0
            continue

        # KIỂM TRA ĐÃ CẬP NHẬT GIÁ Ở ĐỢT RESET NÀY CHƯA ?
        if updated[row]:
            print("Giá đã được cập nhật rồi")

            row = row + 1 if row < numRow - 1 else 0
            continue


        # Click vào row
        # single_click(TARGET_WINDOW, 1249, 258 + row * 52, draw=f'row_{row}.png')
        multi_click(1249, 258 + row * 52, 2, rand_x=True, rand_y=False)

        # Chờ Modal mở
        currentPrice = waitModal_v4(BUY_MODAL_1600_1900, [1270, 536, 35, 44])
        if not currentPrice:
            single_click(TARGET_WINDOW, 1214, 724)

            time.sleep(0.2)
            continue

        # timing_capture([1270, 536, 35, 44])

        # testRow = row + 1 if row + 1 < numRow else 0
        if prevPrice[row]:
            isDiff = compareImage_v2(imageToArr(prevPrice[row]), imageToArr(currentPrice), threshold=0.8, showScore=True)
            # print(f'{row+1}: Thay đổi' if isDiff else f'{row+1}: Không thay đổi')

            # Giá đã thay đổi
            if isDiff:
                
                single_click(TARGET_WINDOW, 1284, 395)
                time.sleep(0.075)
                single_click(TARGET_WINDOW, 1034, 725)
                saveImage(capture_window(TARGET_WINDOW), f'updated_{time.time()}.png')
                time.sleep(0.1)

                send_key(TARGET_WINDOW, KEY_CODES['ESC'])

                updated[row] = True
                

                # FOR DEBUGGING
                saveImage(prevPrice[row], f'prevPrice_{row}_{time.time()}.png')
                saveImage(currentPrice, f'currentPrice_{time.time()}.png')
                # return 
                pass
        
        prevPrice[row] = currentPrice
        
        # Tắt modal
        single_click(TARGET_WINDOW, 1214, 724)           

        row = row + 1 if row < numRow - 1 else 0
        time.sleep(0.2)


a = 1.25
def main():
    # resetTimes = [RESET_TIME['Scamacca'], RESET_TIME['Correa'], RESET_TIME['Unal']]
    # resetTimes = [RESET_TIME['Rowe'], RESET_TIME['Guedes'], RESET_TIME['Milik'], RESET_TIME['Correa'], RESET_TIME['Unal']]
    resetTimes = [RESET_TIME['Muani'] , RESET_TIME['Sangare'] , RESET_TIME['Awoniyi'] , RESET_TIME['Correa']]
    # runOnTransactions_v4(resetTimes)




    img1 = cv2.imread('./currentPrice_1724305748.6365743.png')
    img2 = cv2.imread('./prevPrice_1_1724305748.61563.png')
    # currentPrice = capture_window_region(TARGET_WINDOW, int(576 * a), int(ORDER_ROW_POS[0] * a) - 6, int(80 * a), int(16 * a))

    # print(compareImage_v2(imageToArr(currentPrice), HYPHEN_BIGGER_IMAGE, threshold=0.85, showScore=True))
    print(compareImage_v2(imageToArr(img1), imageToArr(img2), threshold=0.75, showScore=True))


    # for y in ORDER_ROW_POS:
    #     # single_click(TARGET_WINDOW, int(576 * a), int(y * a), draw=f'row_{y}.png')
    #     saveImage(capture_window_region(TARGET_WINDOW, int(576 * a), int(y * a) - 6, int(80 * a), int(16 * a)), f'row_{y}.png')

    # NEW TEMPLATE
    # captureTemplate([int(576 * a), int(ORDER_ROW_POS[0] * a) - 6, int(80 * a), int(16 * a)], 'hyphen.png')
    # captureTemplate([782, 422, 118, 22], 'spam_error.png')

    # TEST TEMPLATE
    # testImage([782, 422, 118, 22], SPAM_ERROR_1600_1900)

    


if __name__ == '__main__':
    main()
