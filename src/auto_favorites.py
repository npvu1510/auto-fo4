import time

from src.utils import *
from src.timeFns import time_until_reset

def allInOnePlayer(resetTime = None, grade = None, priceType = PRICE_TYPES['0'] , autoCancel = True):
    grade = grade if grade else 1

    # # Khởi đầu với cầu thủ đầu tiên trong "DS yêu thích"
    # single_click(TARGET_WINDOW, 406, 254)

    statCountDown = time.time()
    prevPrice = currentPrice = updated = needToCancel = None
    while True:
        os.system('cls')
        print(f"🔃 ĐANG CHÈN CẦU THỦ...")
                
        # RESET CHỈ DIỄN RA TRONG KHOẢNG 55s phút trước -> 10s phút kế tiếp
        now = datetime.now()
        if now.second not in range(0, 11) and now.second not in range(55,61):
            print(f'⌛ Chỉ nhảy giá vào 10 giây đầu và 5 giây cuối của phút (hiện tại: giây thứ {now.second})')
            continue

        # statCountDown = delayAfterDuration(statCountDown, intervalInMinutes=DELAY_INTERVAL_IN_MINUTE, durationInSeconds=DELAY_DURATION_IN_SECOND)


        #  KIỂM TRA RESET TIME
        if resetTime:
            message = time_until_reset(resetTime, offset=OFFSET)
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
        single_click(TARGET_WINDOW, BUY_BUTTON_FAVORITES)
        isModalOpen = waitingForModalOpen()
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




def getPlayersInResetTime(players, offset = 5):
    res = []
    for player in players:
        isInReset = time_until_reset(player['resetTime'], offset=offset)

        if not isinstance(isInReset, str): # Chưa tới giờ
            res.append(player)

    return res

def multiPlayersWithPriority(players, autoDelay = False):
    prevPrices = [None] * len(players)
    updateds = [False] * len(players)
    selected = -1
    
    # # Khởi đầu với cầu thủ đầu tiên trong "DS yêu thích"
    # single_click(TARGET_WINDOW, 406, 254)

    statCountDown = time.time()

    idx = 0
    while True:
        os.system('cls')
        print(f"🔃 ĐANG CHÈN CẦU THỦ #{idx + 1}...")

        # if autoDelay:
        #     statCountDown = delayAfterDuration(statCountDown, intervalInMinutes=DELAY_INTERVAL_IN_MINUTE, durationInSeconds=DELAY_DURATION_IN_SECOND)

        # RESET CHỈ DIỄN RA TRONG KHOẢNG 55s phút trước -> 10s phút kế tiếp
        now = datetime.now()
        if now.second not in range(0, 11) and now.second not in range(55,61):
            print(f'⌛ Chỉ nhảy giá vào 10 giây đầu và 5 giây cuối của phút (hiện tại: giây thứ {now.second})')
            continue

        # KIỂM TRA THẺ ĐANG ĐƯỢC ƯU TIÊN CHÈN => NẾU CHƯA TỒN TẠI THỲ BYPASS
        if selected != -1 and idx != selected:
            idx = idx + 1 if idx < len(players) - 1 else 0
            continue

        #  KIỂM TRA RESET TIME
        if players[idx]['resetTime']:
            message = time_until_reset(players[idx]['resetTime'], offset=OFFSET)
            # Ngoài giờ reset
            if isinstance(message, str):
                print(f'⌚ {message}')
                time.sleep(1)

                prevPrices[idx] = currentPrice = None
                updateds[idx] = False
                selected = -1
                
                idx = idx + 1 if idx < len(players) - 1 else 0
                continue
            
            # Trong giờ reset và cập nhật trong đợt này rồi
            if updateds[idx]:
                idx = idx + 1 if idx < len(players) - 1 else 0
                continue
        

        # CHỌN RA CẦU THỦ ĐƯỢC ƯU TIÊN CHÈN (PHẢI TRONG GIỜ RESET + CHƯA UPDATED TRONG ĐỢT NÀY)
        if selected == -1:
            selected = idx
            single_click(TARGET_WINDOW, [406, 254 +  (players[idx]['row'] - 1) * 40])
            time.sleep(3)
        
        # CLICK MỞ MODAL 
        single_click(TARGET_WINDOW, BUY_BUTTON_FAVORITES)
        isModalOpen = waitingForModalOpen()
        currentPrice = capture_window_region(TARGET_WINDOW, players[idx]['priceType'])
        if not isModalOpen:
            continue
        

        # KIỂM TRA THÔNG TIN MODAL (GIÁ)
        if prevPrices[idx]:
            isDiff = compareImage_v2(imageToArr(prevPrices[idx]), imageToArr(currentPrice), threshold=COMPARE_PRICE_THRESHOLD, showScore=True)[0]
            # saveImage(currentPrice, f'currentPrice_{time.time()}.png')

            # Giá đã thay đổi
            if isDiff:
                buyAndCapture(quantity=players[idx]['quantity'], directory='results/favorites')

                # Nếu có reset time => đánh dấu đã cập nhật trong lần này
                if players[idx]['resetTime']:
                    updateds[idx] = True  

                selected = -1

        
        prevPrices[idx] = currentPrice
        
        # Tắt modal
        closeAndWait()

        idx = idx + 1 if idx < len(players) - 1 else 0