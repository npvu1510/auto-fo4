import os
import cv2

from skimage.metrics import structural_similarity as compare_ssim

# my modules
from datetime import datetime
from src.winApi import *
from src.constants import *


def posToXYWH(pos):
    return pos[0], pos[1], pos[2] , pos[3]


def imageToArr(image):
    return np.array(image)

def saveImage(image, imageName):
    image.save(imageName)

def captureTemplate(position, templateName, subFolder="1600x900"):
    template = capture_window_region(TARGET_WINDOW, position[0], position[1], position[2], position[3])
    saveImage(template, f"./templates/{subFolder}/{templateName}")

# ---------------------------------------------------------------- CALCULATION FUNCTIONS ----------------------------------------------------------------
def absDiff(img1, img2, threshold = 30):
    diff = cv2.absdiff(img1, img2)
    _, thresh = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
    

    return np.count_nonzero(thresh) > 0, diff

def compareImage(img1, img2, threshold = 50, showDiff = False):
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    isDifferent, diff = absDiff(img1, img2, threshold)

    if showDiff:
        cv2.imshow("difference", diff)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    return isDifferent

def compareImage_v2(img1, img2, threshold=0.95, showDiff=False, showScore = False):
    # Chuyển ảnh sang grayscale
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # So sánh hai hình ảnh với SSIM
    score, diff = compare_ssim(img1, img2, full=True)
    diff = (diff * 255).astype("uint8")

    # Kiểm tra xem score có nhỏ hơn ngưỡng không
    # print(score)
    if showScore:
        print(score)

    if showDiff:
        cv2.imshow("difference", diff)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return score < threshold, score

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



# ---------------------------------------------------------------- FUNCTIONAL FUNCTIONS ---------------------------------------------------------------
def waitingFor(template, pos, appear = True, timeout = 1, threshold = 0.9, showScore = False):
    currentImg = capture_window_region(TARGET_WINDOW, pos)
    
    start = time.time()
    while (compareImage_v2(template, imageToArr(currentImg), threshold=threshold, showScore=showScore)[0]
           if appear else not compareImage_v2(template, imageToArr(currentImg), threshold=threshold, showScore=showScore)[0]):    
        if time.time() - start >= timeout:
            return False
            
        currentImg = capture_window_region(TARGET_WINDOW, pos)
        # print("Đang chờ modal mở...")

    return True    

def waitingForModalOpen(timeout=2):
    # single_click(TARGET_WINDOW, BUY_BUTTON_FAVORITES)
    isModalOpen = waitingFor(BUY_MODAL_OPEN_1600_1900, BUY_MODAL_OPEN_POS, threshold=OPEN_MODAL_THRESHOLD, timeout=timeout)

    # Nếu modal chưa mở => có thể do lỗi spam hoặc timeout
    if not isModalOpen:
        spamCheck()
        return False

    return True

def waitingForModalClose(timeout=2):
    # single_click(TARGET_WINDOW, BUY_BUTTON_FAVORITES)
    isModalClose = waitingFor(SELL_MODAL_OPEN_1600_1900, SELL_MODAL_OPEN_POS, threshold=OPEN_MODAL_THRESHOLD, timeout=timeout)

    # Nếu modal chưa mở => có thể do lỗi spam hoặc timeout
    if not isModalClose:
        spamCheck()
        return False

    return True


def isInFirst10Seconds():
    second = datetime.now().second
    if second not in range(0, 11):
        print(f'⌛ Chỉ nhảy giá vào 10 giây đầu tiên của phút (hiện tại: {second}s)')
        return False
    
    return True

def spamCheck(delayDurationInMinutes = 10):
    # Kiểm tra lỗi spam
    if not (compareImage_v2(imageToArr(capture_window_region(TARGET_WINDOW, SPAM_ERROR_POS)), SPAM_ERROR_1600_1900, threshold=0.8, showScore=False)[0]):
        print(f"⌚ ĐANG GẶP LỖI SPAM CHỜ {delayDurationInMinutes} PHÚT...")
        time.sleep(delayDurationInMinutes * 60)

        closeAndWait()
        time.sleep(1)
        
    # Kiểm tra lỗi timeout
    else:
        print('⏰ TIMEOUT KHI MỞ MODAL')
        closeAndWait()

def delayAfterDuration(start, intervalInMinutes = 1, durationInSeconds = 5):
    currentSecond = datetime.now().second
    
    if currentSecond not in range(0,10) and currentSecond not in range(59 - durationInSeconds, 59) and time.time() - start > intervalInMinutes * 60:
        print(f'🫸 TẠM DỪNG {durationInSeconds} GIÂY SAU MỖI {intervalInMinutes} PHÚT TRÁNH SPAM...')
        time.sleep(durationInSeconds)
        os.system('cls')
        return time.time()
    return start

def slotCheck(grade = 1, slotType = 'buy'):
    slot_check_pos = BUY_SLOT_CHECK_POS if slotType == 'buy' else SELL_SLOT_CHECK_POS
    currentSlot = capture_window_region(TARGET_WINDOW, [slot_check_pos[0], slot_check_pos[1] + 34 * (grade - 1) - int(0.5 * grade), slot_check_pos[2], slot_check_pos[3]])
    # saveImage(currentSlot, f'{slotType}_slot_{grade}.png')

    folder = 'buySlots' if slotType == 'buy' else 'sellSlots'
    # print(f'./templates/1600x900/{folder}/{slotType}_slot_{grade}.png')
    template = cv2.imread(f'./templates/1600x900/{folder}/{slotType}_slot_{grade}.png')
    return not compareImage_v2(template, imageToArr(currentSlot), threshold=0.95, showScore=True)[0]

def checkNotification():
    currentBadge = capture_window_region(TARGET_WINDOW, 785, 165, 11, 10)
    res = compareImage_v2(BADGE_1600_1900, imageToArr(currentBadge))[0]
    if not res:
        print('🎉 Cầu thủ đã về')
        single_click(TARGET_WINDOW, 828, 178)
        time.sleep(5)
        single_click(TARGET_WINDOW, 665, 183)
    
    return res


# ---------------------------------------------------------------- CLICK/PRESSED FUNCTIONS ----------------------------------------------------------------
def cancelFirstOrder():
    single_click(TARGET_WINDOW, [828, 178])
    time.sleep(1)
    multi_click([1335, 256], rand_x=True)
    time.sleep(0.5)
    single_click(TARGET_WINDOW, [851, 622])
    time.sleep(0.5)
    send_key(TARGET_WINDOW, KEY_CODES['ESC'])
    time.sleep(0.5)
    single_click(TARGET_WINDOW, [665, 183])
    time.sleep(3)


def closeAndWait(timeout=1):
    # single_click(TARGET_WINDOW, 1214, 724)        
    send_key(TARGET_WINDOW, KEY_CODES['ESC'])
    waitingFor(MODAL_CLOSED_1600_1900,[523, 169, 23, 17], timeout=timeout, threshold=CLOSE_MODAL_THRESHOLD)



def buyAndCapture(list='favorites', quantity = 1, directory = 'results'):
    # Click vào giá
    single_click(TARGET_WINDOW, MAX_PRICE_BUY_MODAL)
    
    # Tăng số lượng
    if quantity - 1 > 0:
        multi_click(INC_QUANTITY_BUTTON_BUY_MODAL, quantity - 1, rand_x=True)
    
    # Bấm mua
    single_click(TARGET_WINDOW, BUY_BUTTON_BUY_MODAL)
    

    # Chup man hinh
    buyAt = datetime.now().strftime("%Hh%Mm%Ss-%Y-%m-%d")
    if list == 'favorites':
        saveImage(capture_window(TARGET_WINDOW), f'{directory}/before_{buyAt}.png')
        waitingFor(MODAL_CLOSED_1600_1900, MODAL_CLOSE_POS)
        time.sleep(3)
        saveImage(capture_window(TARGET_WINDOW), f'{directory}/after_{buyAt}.png')
    
    elif list == 'transactions':
        saveImage(capture_window(TARGET_WINDOW), f'{directory}/{buyAt}.png')
        waitingFor(MODAL_CLOSED_1600_1900, MODAL_CLOSE_POS)


def sellAndCapture(quantity = 1, directory = 'results'):
    # Bấm giá min
    single_click(TARGET_WINDOW, MIN_PRICE_SELL_MODAL)

    # #  quantities
    #  single_click(TARGET_WINDOW, [1286, 618])

    # Bấm bán
    single_click(TARGET_WINDOW, SELL_BUTTON_SELL_MODAL)


    buyAt = datetime.now().strftime("%Hh%Mm%Ss-%Y-%m-%d")
    saveImage(capture_window(TARGET_WINDOW), f'={directory}/sell_before_{buyAt}.png')
    waitingFor(MODAL_CLOSED_1600_1900, MODAL_CLOSE_POS)
    time.sleep(3)
    saveImage(capture_window(TARGET_WINDOW), f'={directory}/sell_after_{buyAt}.png')


# ---------------------------------------------------------------- TEST FUNCTIONS ----------------------------------------------------------------
def timing_capture(pos, duration = 5):
    start = time.time()
    index = 0
    while time.time() - start <= duration:
        image = capture_window_region(TARGET_WINDOW, [pos[0], pos[1], pos[2], pos[3]])
        saveImage(image, f'timing_captures/{index}.png')
        index +=1

def testImage(position, template = None, compareByVersion2 = True, threshold = 0.85):
    prevImage = False

    while True:
        currentImage = capture_window_region(TARGET_WINDOW, [position[0], position[1], position[2], position[3]])
        # saveImage(currentImage, 'currentImage.png')
        if template.any():
            isAppear = not compareImage(template, imageToArr(currentImage), threshold=threshold, showDiff=False) if not compareByVersion2 else not compareImage_v2(template, imageToArr(currentImage), threshold=threshold, showDiff=False, showScore=True)[0]
            if isAppear:
                print("Xuất hiện")
            else:
                print("Biến mất")

        else:
            if prevImage:
                isChange = compareImage(imageToArr(prevImage), imageToArr(currentImage), threshold=threshold, showDiff=False)
                if isChange:
                    print("Thay đổi")
                    time.sleep(2)
                    os.system('cls')
        
            prevImage = currentImage
        # time.sleep(0.15)

def openModalAnDoSth(openningThreshold = 0.95, save = False):
    while True:
        # CLICK MỞ MODAL 
        single_click(TARGET_WINDOW, BUY_BUTTON_FAVORITES)
        isModalOpen = waitingFor(BUY_MODAL_OPEN_1600_1900, BUY_MODAL_OPEN_POS, threshold= openningThreshold, showScore=False)
        # currentPrice = capture_window_region(TARGET_WINDOW, 1220, 382, 66, 22) old official
        # currentPrice = capture_window_region(TARGET_WINDOW, 1185, 382, 96, 22)
        # currentPrice = capture_window_region(TARGET_WINDOW, MAX_PRICE_IN_BUY_MODAL_POS)

        # CHUC NGHIN
        # currentPrice = capture_window_region(TARGET_WINDOW, [1209, 382, 45, 22])

        # NGHIN
        # currentPrice = capture_window_region(TARGET_WINDOW, [1214, 382, 55, 22])

        # Tram
        currentPrice = capture_window_region(TARGET_WINDOW, [1225, 382, 55, 22])


        # Nếu modal chưa mở => có thể do lỗi spam hoặc timeout
        if not isModalOpen:
            print('⏰ TIMEOUT KHI MỞ MODAL')
            # single_click(TARGET_WINDOW, 1214, 724)
            send_key(TARGET_WINDOW, KEY_CODES['ESC'])
            waitingFor(MODAL_CLOSED_1600_1900, MODAL_CLOSE_POS)
            continue
    
        # timing_capture([1239, 545, 37, 30])
        # timing_capture([1278, 566, 25, 16])
        # return 
    
        # KIỂM TRA THÔNG TIN MODAL (GIÁ)
        
        # CAPTURE DẤU HIỆU
        # timing_capture([1239, 545, 37, 30])
        # timing_capture([1278, 566, 25, 16])
        # return 

        # saveImage(prevPrice, f'prevPrice_{time.time()}.png')
        if save:
            imgName = f'currentPrice_{time.time()}.png'
            saveImage(currentPrice, imgName)

            send_key(TARGET_WINDOW, KEY_CODES['ESC'])

            return imgName
    
        send_key(TARGET_WINDOW, KEY_CODES['ESC'])
        return currentPrice

def compareTwoImgRead(imgPath1, imgPath2, threshold = 0.85, showDiff = False, showScore = True):
    img1 = cv2.imread(imgPath1)
    img2 = cv2.imread(imgPath2)

    _, score = compareImage_v2(img1, img2, threshold=threshold, showDiff=showDiff, showScore=showScore)
    return score

def compareTwoImgArr(img1, img2, threshold = 0.85, showDiff = False, showScore = True):
    _, score = compareImage_v2(imageToArr(img1), imageToArr(img2), threshold=threshold, showDiff=showDiff, showScore=showScore)
    return score

def compareContinousSamePrice(openningThreshold = 0.9,stoppingThreshold = 0.95):
    while True:
        img1 = openModalAnDoSth(openningThreshold=openningThreshold)
        time.sleep(0.25)
        img2 = openModalAnDoSth(openningThreshold=openningThreshold)

        score = compareTwoImgArr(img1, img2, showScore=False)
        print(f'Score: {score}')
        if score < stoppingThreshold:
            saveImage(img1, f'ccsimage1_{time.time()}.png')
            saveImage(img2, f'ccsimage2_{time.time()}.png')
            exit(1)