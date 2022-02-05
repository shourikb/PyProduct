import pytesseract
import cv2

breaking_news = cv2.imread('images/breakingnews.png')

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Shourik\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

text = pytesseract.image_to_string(breaking_news)

bitcoin = cv2.imread('images/bitcoin.jpeg')

text = pytesseract.image_to_string(bitcoin)

print(text)
