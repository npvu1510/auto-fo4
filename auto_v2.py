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
        if time.time() - start >= 10:
            return False
            
        currentImg = capture_window_region(TARGET_WINDOW, pos[0], pos[1], pos[2], pos[3])
        # print("Đang chờ modal mở...")
    # signatureImg = capture_window_region(TARGET_WINDOW, pos[0], pos[1], pos[2], pos[3])
    
    maxPriceImage = capture_window_region(TARGET_WINDOW, 1240, 382, 43, 24)
    saveImage(maxPriceImage, 'z.png')
    exit(0)
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

import numpy as np

def compareImage_template(img1, img2, threshold=0.8, showDiff=False):
    # Chuyển hình ảnh sang grayscale
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # So khớp mẫu
    result = cv2.matchTemplate(img1, img2, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    isDifferent = max_val < threshold

    print(max_val)

    if showDiff:
        h, w = img2.shape[:2]
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(img1, top_left, bottom_right, 255, 2)
        cv2.imshow("difference", img1)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return isDifferent

# # Ví dụ sử dụng
# result = compareImage_template(img1, img2, threshold=0.8, showDiff=True)
# print("Images are different:", result)

def compareImage_feature(img1, img2, showDiff=False):
    # Chuyển hình ảnh sang grayscale
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Tạo đối tượng SIFT
    sift = cv2.SIFT_create()

    # Phát hiện và tính toán các đặc trưng
    keypoints_1, descriptors_1 = sift.detectAndCompute(img1, None)
    keypoints_2, descriptors_2 = sift.detectAndCompute(img2, None)

    # So khớp các đặc trưng
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
    matches = bf.match(descriptors_1, descriptors_2)

    # Sắp xếp các so khớp theo khoảng cách
    matches = sorted(matches, key=lambda x: x.distance)
    print(len(matches), len(keypoints_1) *0.8)

    isDifferent = len(matches) < len(keypoints_1) * 0.8

    if showDiff:
        img_matches = cv2.drawMatches(img1, keypoints_1, img2, keypoints_2, matches, None)
        cv2.imshow("Matches", img_matches)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return isDifferent



def compareImage_moments(img1, img2):
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    moments1 = cv2.moments(img1_gray)
    moments2 = cv2.moments(img2_gray)

    hu_moments1 = cv2.HuMoments(moments1).flatten()
    hu_moments2 = cv2.HuMoments(moments2).flatten()

    # Tính sự khác biệt giữa các moments
    diff = np.sum(np.abs(hu_moments1 - hu_moments2))
    print(diff)
    
    return diff < 0.01  # Ngưỡng thấp cho thấy các ảnh rất giống nhau




a = 1.25
def main():
    # resetTimes = [RESET_TIME['Scamacca'], RESET_TIME['Correa'], RESET_TIME['Unal']]
    # resetTimes = [RESET_TIME['Rowe'], RESET_TIME['Guedes'], RESET_TIME['Milik'], RESET_TIME['Correa'], RESET_TIME['Unal']]
    # resetTimes = [RESET_TIME['Muani'] , RESET_TIME['Sangare'] , RESET_TIME['Correa'],  RESET_TIME['Awoniyi']]
    # runOnTransactions_v4(resetTimes)

    # waitModal_v4(BUY_MODAL_1600_1900, [1270, 536, 35, 44])
    # exit()


    # img1 = cv2.imread('./129.png')
    # img2 = cv2.imread('./133.png')
    img1 = cv2.imread('./129.png')
    img2 = cv2.imread('./133.png')
    # # currentPrice = capture_window_region(TARGET_WINDOW, int(576 * a), int(ORDER_ROW_POS[0] * a) - 6, int(80 * a), int(16 * a))

    # print(compareImage(imageToArr(img1), imageToArr(img2), threshold=80, showDiff=True))
    # print(compareImage_v2(imageToArr(img1), imageToArr(img2), threshold=0.75, showScore=True))
    # print(compareImage_template(imageToArr(img1), imageToArr(img2), threshold=0.75))
    # print(compareImage_feature(imageToArr(img1), imageToArr(img2)))
    print(compareImage_moments(imageToArr(img1), imageToArr(img2)))


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
