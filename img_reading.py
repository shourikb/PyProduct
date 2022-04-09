import pytesseract
import cv2
import numpy as np

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# noise removal
def remove_noise(image):
    return cv2.medianBlur(image, 5)


# thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


# dilation
def dilate(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(image, kernel, iterations=1)


# erosion
def erode(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(image, kernel, iterations=1)


# opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)


# canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)


# skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated


# template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

def str_to_num(str):
    numbers = []
    for num in str.split():
        if num.isdigit():
            numbers.append(num)
    return numbers

breaking_news = cv2.imread('images/breakingnews.png')

text = pytesseract.image_to_string(breaking_news)

# Thresh works best for room 1
# Everything but canny works for room 2
# All work for room 3
room = cv2.imread('images/digits.png')  #cv2.imread('images/room3.jpg') cv2.imread('images/room2.jpg')

gray = get_grayscale(room)
thresh = thresholding(gray)
opening = opening(gray)
canny = canny(gray)

text = pytesseract.image_to_string(room)

print("Original")
print(text)
print("Thresh")
print(pytesseract.image_to_string(thresh))
print("Opening")
print(pytesseract.image_to_string(opening))
print("Canny")
print(pytesseract.image_to_string(canny))

thresh_nums = str_to_num(pytesseract.image_to_string(thresh))
print("Only Numbers")
print(thresh_nums)