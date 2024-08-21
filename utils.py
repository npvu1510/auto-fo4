import os
import cv2

from skimage.metrics import structural_similarity as compare_ssim

# my modules
from winApi import *


def imageToArr(image):
    return np.array(image)

def saveImage(image, imageName):
    image.save(imageName)


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
    isDifferent = score < threshold

    if showDiff:
        cv2.imshow("difference", diff)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return isDifferent

# ---------------------------------------------------------------- TEST FUNCTIONS ----------------------------------------------------------------
def captureTemplate(position, templateName, subFolder="1600x900"):
    template = capture_window_region(TARGET_WINDOW, position[0], position[1], position[2], position[3])
    saveImage(template, f"./templates/{subFolder}/{templateName}")


def testImage(position, template = None):
    threshold = 50
    prevImage = False

    while True:
        currentImage = capture_window_region(TARGET_WINDOW, position[0], position[1], position[2], position[3])
        # saveImage(currentImage, 'currentImage.png')
        if template.any():
            isAppear = not compareImage(template, imageToArr(currentImage), threshold=threshold, showDiff=False)
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
