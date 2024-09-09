import time

from utils import *
from timeFns import time_until_reset

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
            message = time_until_reset(resetTimes[row], offset=OFFSET)
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
                buyAndCapture(list='transactions')

                # # FOR DEBUGGING
                # saveImage(prevPrice[row], f'prevPrice_{row}_{time.time()}.png')
                # saveImage(currentPrice, f'currentPrice_{time.time()}.png')
                                
                updated[row] = True

        prevPrice[row] = currentPrice
        
        # Tắt modal
        # single_click(TARGET_WINDOW, 1214, 724)           
        closeAndWait()

        row = row + 1 if row < numRow - 1 else 0