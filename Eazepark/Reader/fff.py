import cv2
import pytesseract
import mysql.connector
import re
from datetime import datetime
import subprocess as s
from tkinter import Tk, simpledialog
import pyautogui as p
import time
from selenium import webdriver
import pygetwindow as gw

pytesseract.pytesseract.tesseract_cmd = r'C:\\Tesseract\\tesseract.exe'
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="dpsbn",
    database="cars"
)

dri = webdriver.Chrome()
dri.get('file:///C:/EazePark/Reader/templates/some.html')
window = gw.getWindowsWithTitle('Eazepark - Park with Ease - Google Chrome')[0]
window.maximize()

driver_thank_you = webdriver.Chrome()

def get_manual_car_number():
    root = Tk()
    root.withdraw()
    car_number = simpledialog.askstring("Car Number", "Enter the car number:")
    return car_number
def extract_car_number(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    thresholded = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    car_number = pytesseract.image_to_string(thresholded)
    return car_number.strip()
car_number_detected = False
state_patterns = {
    'AN': r'AN\s\d{1,2}\s[A-Z]{1,2}\s\d{4}$',  # Andaman and Nicobar Islands
    'AP': r'AP\s\d{1,2}\s[A-Z]{1,2}\s\d{4}$',  # Andhra Pradesh
    'AR': r'AR\s\d{1,2}\s[A-Z]{1,2}\s\d{4}$',  # Arunachal Pradesh
    'AS': r'AS\s\d{1,2}\s[A-Z]{1,2}\s\d{4}$',  # Assam
    'BR': r'BR\s\d{1,2}\s[A-Z]{1,2}\s\d{4}$',  # Bihar
    'CH': r'CH\s\d{1,2}\s[A-Z]{1,2}\s\d{4}$',  # Chandigarh
    'CT': r'CT\s\d{1,2}\s[A-Z]{1,2}\s\d{4}$',  # Chhattisgarh
    'DD': r'DD\s\d{1,2}\s[A-Z]{1,2}\s\d{4}$',  # Dadra and Nagar Haveli and Daman and Diu
    'DL': r'DL\s\d{1,2}\s[A-Z]{1,2}\s\d{4}$',  # Delhi
    'DN': r'DN\s\d{1,2}\s[A-Z]{1,2}\s\d{4}$',  # Dadra and Nagar Haveli and Daman and Diu
    'GA': r'GA\s\d{1,2}\s[A-Z]{1,2}\s\d{4}$',  # Goa
    'GJ': r'GJ\s\d{1,2}\s[A-Z]{1,2}\s\d{4}$',  # Gujarat
    'HP': r'HP\s\d{1,2}\s[A-Z]{1,2}\s\d{4}$',  # Himachal Pradesh
    'HR': r'HR\s\d{1,2}\s[A-Z]{1,2}\s\d{4}$',  # Haryana
    'JH': r'JH\s\d{1,2}\s[A-Z]{1,2}\s\d{4}$',  # Jharkhand
    'JK': r'JK\s\d{1,2}\s[A-Z]{1,2}\s\d{4}$',  # Jammu and Kashmir
    'KA': r'KA\s\d{1,2}\s[A-Z]{1,2}\s\d{4}$',  # Karnataka
    'KL': r'KL\s\d{1,2}\s[A-Z]{1,2}\s\d{4}$',  # Kerala
    'LA': r'LA\s\d{1,2}\s[A-Z]{1,2}\s\d{4}$',  # Ladakh
    'LD': r'LD\s\d{1,2}\s[A-Z]{1,2}\s\d{4}$',  # Lakshadweep
    'MH': r'MH\s\d{1,2}\s[A-Z]{1,2}\s\d{4}$',  # Maharashtra
    'ML': r'ML\s\d{1,2}\s[A-Z]{1,2}\s\d{4}$',  # Meghalaya
    'MN': r'MN\s\d{1,2}\s[A-Z]{1,2}\s\d{4}$',  # Manipur
    'MP': r'MP\s\d{1,2}\s[A-Z]{1,2}\s\d{4}$',  # Madhya Pradesh
    'MZ': r'MZ\s\d{1,2}\s[A-Z]{1,2}\s\d{4}$',  # Mizoram
    'NL': r'NL\s\d{1,2}\s[A-Z]{1,2}\s\d{4}$',  # Nagaland
    'OD': r'OD\s\d{1,2}\s[A-Z]{1,2}\s\d{4}$',  # Odisha
    'PB': r'PB\s\d{1,2}\s[A-Z]{1,2}\s\d{4}$',  # Punjab
    'PY': r'PY\s\d{1,2}\s[A-Z]{1,2}\s\d{4}$',  # Puducherry
    'RJ': r'RJ\s\d{1,2}\s[A-Z]{1,2}\s\d{4}$',  # Rajasthan
    'SK': r'SK\s\d{1,2}\s[A-Z]{1,2}\s\d{4}$',  # Sikkim
    'TN': r'TN\s\d{1,2}\s[A-Z]{1,2}\s\d{4}$',  # Tamil Nadu
    'TR': r'TR\s\d{1,2}\s[A-Z]{1,2}\s\d{4}$',  # Tripura
    'TS': r'TS\s\d{1,2}\s[A-Z]{1,2}\s\d{4}$',  # Telangana
    'UK': r'UK\s\d{1,2}\s[A-Z]{1,2}\s\d{4}$',  # Uttarakhand
    'UP': r'UP\s\d{1,2}\s[A-Z]{1,2}\s\d{4}$',  # Uttar Pradesh
    'WB': r'WB\s\d{1,2}\s[A-Z]{1,2}\s\d{4}$',  # West Bengal
    'AN1': r'AN\d{1,2}[A-Z]{1,2}\d{4}$',  # Andaman and Nicobar Islands
    'AP1': r'AP\d{1,2}[A-Z]{1,2}\d{4}$',  # Andhra Pradesh
    'AR1': r'AR\d{1,2}[A-Z]{1,2}\d{4}$',  # Arunachal Pradesh
    'AS1': r'AS\d{1,2}[A-Z]{1,2}\d{4}$',  # Assam
    'BR1': r'BR\d{1,2}[A-Z]{1,2}\d{4}$',  # Bihar
    'CH1': r'CH\d{1,2}[A-Z]{1,2}\d{4}$',  # Chandigarh
    'CT1': r'CT\d{1,2}[A-Z]{1,2}\d{4}$',  # Chhattisgarh
    'DD1': r'DD\d{1,2}[A-Z]{1,2}\d{4}$',  # Dadra and Nagar Haveli and Daman and Diu
    'DL1': r'DL\d{1,2}[A-Z]{1,2}\d{4}$',  # Delhi
    'DN1': r'DN\d{1,2}[A-Z]{1,2}\d{4}$',  # Dadra and Nagar Haveli and Daman and Diu
    'GA1': r'GA\d{1,2}[A-Z]{1,2}\d{4}$',  # Goa
    'GJ1': r'GJ\d{1,2}[A-Z]{1,2}\d{4}$',  # Gujarat
    'HP1': r'HP\d{1,2}[A-Z]{1,2}\d{4}$',  # Himachal Pradesh
    'HR1': r'HR\d{1,2}[A-Z]{1,2}\d{4}$',  # Haryana
    'JH1': r'JH\d{1,2}[A-Z]{1,2}\d{4}$',  # Jharkhand
    'JK1': r'JK\d{1,2}[A-Z]{1,2}\d{4}$',  # Jammu and Kashmir
    'KA1': r'KA\d{1,2}[A-Z]{1,2}\d{4}$',  # Karnataka
    'KL1': r'KL\d{1,2}[A-Z]{1,2}\d{4}$',  # Kerala
    'LA1': r'LA\d{1,2}[A-Z]{1,2}\d{4}$',  # Ladakh
    'LD1': r'LD\d{1,2}[A-Z]{1,2}\d{4}$',  # Lakshadweep
    'MH1': r'MH\d{1,2}[A-Z]{1,2}\d{4}$',  # Maharashtra
    'ML1': r'ML\d{1,2}[A-Z]{1,2}\d{4}$',  # Meghalaya
    'MN1': r'MN\d{1,2}[A-Z]{1,2}\d{4}$',  # Manipur
    'MP1': r'MP\d{1,2}[A-Z]{1,2}\d{4}$',  # Madhya Pradesh
    'MZ1': r'MZ\d{1,2}[A-Z]{1,2}\d{4}$',  # Mizoram
    'NL1': r'NL\d{1,2}[A-Z]{1,2}\d{4}$',  # Nagaland
    'OD1': r'OD\d{1,2}[A-Z]{1,2}\d{4}$',  # Odisha
    'PB1': r'PB\d{1,2}[A-Z]{1,2}\d{4}$',  # Punjab
    'PY1': r'PY\d{1,2}[A-Z]{1,2}\d{4}$',  # Puducherry
    'RJ1': r'RJ\d{1,2}[A-Z]{1,2}\d{4}$',  # Rajasthan
    'SK1': r'SK\d{1,2}[A-Z]{1,2}\d{4}$',  # Sikkim
    'TN1': r'TN\d{1,2}[A-Z]{1,2}\d{4}$',  # Tamil Nadu
    'TR1': r'TR\d{1,2}[A-Z]{1,2}\d{4}$',  # Tripura
    'TS1': r'TS\d{1,2}[A-Z]{1,2}\d{4}$',  # Telangana
    'UK1': r'UK\d{1,2}[A-Z]{1,2}\d{4}$',  # Uttarakhand
    'UP1': r'UP\d{1,2}[A-Z]{1,2}\d{4}$',  # Uttar Pradesh
    'WB1': r'WB\d{1,2}[A-Z]{1,2}\d{1,4}$',  # West Bengal
    'BH': r'\d{2}BH\d{4}[A-Z]{1,2}$'      ,  #BH Registration
    'BH11': r'\d{2}\sBH\s\d{4}\s[A-Z]{1,2}$',
    'BH1': r'\d{2}BH\d{4}\s[A-Z]{1,2}$',
    'DL3':r'DL\d{1}[A-Z]{1}\s[A-Z]{2}\s\d{4}$',#Delhi1
    'DL2':r'DL\d{1}[A-Z]{2}\s\d{4}$' 
    }
all_states_pattern = '|'.join(state_patterns.values())
all_regex = re.compile(all_states_pattern)
cap = cv2.VideoCapture(0)
manual_entry = False  # Flag to indicate if manual entry mode is active

while True:
    ret, frame = cap.read()    
    if not ret:
        break
    if manual_entry:
        manual_car_number = get_manual_car_number()
        if manual_car_number:
            car_number = manual_car_number.strip()
            print("Manual Car Number:", car_number)
            manual_entry = False  # Disable manual entry mode
    else:
        car_number = extract_car_number(frame)
        print("OCR Output:", car_number)
    if car_number and all_regex.match(car_number):
        dri.quit()
        cursor = db.cursor()
        cursor.execute('select * from car_no')
        a=cursor.fetchall()
        for i in a:
            if car_number in i:
                s.run(["python","C:\\EazePark\\Reader\\Reader.py"]) 
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query = "INSERT INTO car_no (car_number, timestamp) VALUES (%s, %s)"
        values = (car_number, timestamp)
        cursor.execute(query, values)
        db.commit()
        print("Detected Car Number:", car_number)
        print("Timestamp:", timestamp)
        car_number_detected = True
        if car_number_detected:
            driver_thank_you.get('file:///C:/EazePark/Reader/templates/thank_you.html')
            window_thank_you = gw.getWindowsWithTitle('Thank You - Google Chrome')[0]
            window_thank_you.maximize()
            time.sleep(5)
            driver_thank_you.quit()
            break
    cv2.imshow('Car Number Detection', frame)
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q') or car_number_detected:
        break
    if key == ord('m') or key == ord('M'):
        manual_entry = True
cap.release()
cv2.destroyAllWindows()
s.run(["python", "C:\\EazePark\\Reader\\Reader.py"])