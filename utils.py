import os
import cv2

from skimage.metrics import structural_similarity as compare_ssim

# my modules
from winApi import *
from constants import *


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


# ---------------------------------------------------------------- TEST FUNCTIONS ----------------------------------------------------------------
def testImage(position, template = None, compareByVersion2 = True, threshold = 0.85):
    prevImage = False

    while True:
        currentImage = capture_window_region(TARGET_WINDOW, position[0], position[1], position[2], position[3])
        # saveImage(currentImage, 'currentImage.png')
        if template.any():
            isAppear = not compareImage(template, imageToArr(currentImage), threshold=threshold, showDiff=False) if not compareByVersion2 else not compareImage_v2(template, imageToArr(currentImage), threshold=threshold, showDiff=False)
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
            waitingFor(MODAL_CLOSED_1600_1900, BUY_MODAL_CLOSE_POS)
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