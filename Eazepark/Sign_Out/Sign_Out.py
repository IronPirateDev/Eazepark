import cv2
import pytesseract
import mysql.connector
import re
from datetime import datetime, timedelta
import subprocess as s
import webbrowser
import time
import pyautogui
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import threading
from selenium import webdriver
import psutil
import pygetwindow as gw
from tkinter import Tk, simpledialog
pytesseract.pytesseract.tesseract_cmd = r'C:\\Tesseract\\tesseract.exe'
money = False
manual_payment = False
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="dpsbn",
    database="cars")
import qrcode
from urllib.parse import urlencode, quote
def delete_car_number(car_number):
    cursor = db.cursor()
    query = "DELETE FROM car_no WHERE car_number = %s"
    cursor.execute(query, (car_number,))
    db.commit()
def adddup():
    import mysql.connector as ms
    db = ms.connect(
    host="localhost",
    user="root",
    password="dpsbn",
    database="cars")
    import datetime
    today = datetime.date.today()
    ll=today.strftime("%Y-%m-%d")
    print(ll)
    cursor=db.cursor()
    q1="INSERT INTO rep (car_number,timestamp,money_paid) VALUES (%s,%s,%s)"
    v1=(car_number,ll,total_charge)
    cursor.execute(q1,v1)
    db.commit()
    delete_car_number(car_number)
    db.close()
def get_manual_car_number():
    root = Tk()
    root.withdraw()
    car_number = simpledialog.askstring("Car Number", "Enter the car number:")
    return car_number
def generate_qr_code(car_number, money):
    # Encode car number and money as URL parameters
    params = {'car_number': car_number, 'money': money}
    url = 'https://eazepark.onrender.com/?' + urlencode(params, quote_via=quote)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1,)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save('C:\EazePark\Sign_Out\qr.png')
dbno=[]
payment_event=False
def is_edge_running():
    payment_confirmation_windows = [window for window in gw.getWindowsWithTitle('') if 'Payment Confirmation' in window.title]
    return len(payment_confirmation_windows) > 0
rr=False
def payment_verification():
    global rr,car_number_em,money_paid
    import re
    import imaplib
    import email
    from email.header import decode_header
    def extract_car_number_and_money_paid(email_content):
        car_number_em = ""
        money_paid = ""
        car_number_match = re.search(r"Car Number: ([\w\s]+)(?=\s*Money Paid:|$)", email_content)
        money_paid_match = re.search(r"Money Paid: (\d+)", email_content)
        if car_number_match:
            car_number_em = car_number_match.group(1)
        if money_paid_match:
            money_paid = money_paid_match.group(1)
        return car_number_em.strip(), money_paid.strip()
    username = "ineazepark@gmail.com"
    password = "hqkoabclvofhqlxt"
    rr = False
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(username, password)
    mail.select("inbox")
    status, messages = mail.search(None, "ALL")
    message_ids = messages[0].split()
    if message_ids:
        latest_message_id = message_ids[-1]
        _, msg_data = mail.fetch(latest_message_id, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode("utf-8")
                    body = body.split('<br>')
                    ft = body[0] + '\n' + body[1] + '\n'
                    car_number_em, money_paid = extract_car_number_and_money_paid(ft)
                    print(car_number,total_charge)
                    print(car_number_em,money_paid)
                    if car_number == car_number_em and money_paid == str(total_charge):
                        rr = True
                        break
        else:
            email_content = msg.get_payload(decode=True).decode("utf-8")
            car_number_em, money_paid = extract_car_number_and_money_paid(email_content)
            if car_number == car_number_em and money_paid == str(total_charge):
                rr = True
    mail.logout()
    print(rr)
    return rr
def prompt_manual_payment():
    global manual_payment
    answer = input("Was the payment made manually? (y/n): ").lower()
    if answer == 'y':
        manual_payment = True
def extract_car_number(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    thresholded = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    car_number = pytesseract.image_to_string(thresholded)
    return car_number.strip()
def calculate_charges(timestamp):
    current_time = datetime.now()
    time_difference = current_time - timestamp
    total_hours = int((time_difference.total_seconds() + 3599) / 3600)
    base_charge = 20
    additional_charge_per_hour = 10
    total_charge = base_charge + max(total_hours - 2, 0) * additional_charge_per_hour
    return total_hours, total_charge
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
manual_entry = False
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
        cursor = db.cursor()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query = "SELECT * from car_no where car_number=%s"
        cursor.execute(query, (car_number,))
        result = cursor.fetchone()
        payment_confirmation_event = threading.Event()
        if result:
            print("Detected Car Number:", car_number)
            db_timestamp = result[1]
            total_hours, total_charge = calculate_charges(db_timestamp)
            print(f"Total Hours: {total_hours}")
            print(f"Total Charges: {total_charge} Rs")
        break
    cv2.imshow('Car Number Detection', frame)
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q') or car_number_detected:
        break
    if key == ord('m') or key==ord('M'):
        manual_entry = True
cap.release()
cv2.destroyAllWindows()
cursor.execute('select * from car_no')
a = cursor.fetchall()
for i in a:
    for j in i:
        dbno.append(j)
        break
if car_number not in dbno:
    s.run(["python","C:\\EazePark\\Sign_Out\\Sign_Out.py"])
money=str(total_charge)
generate_qr_code(car_number, money)
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Payment Confirmation</title>
    <link rel="icon" href="static/favicon.ico">
    <style>
        body {{
            background-color: black;
            color: white;
            font-family: Arial, sans-serif;
            text-align: center;
            margin: 0;
            padding: 0;
        }}
        h1 {{
            font-size: 24px;
        }}
        p {{
            font-size: 18px;
        }}
        .container {{
            display: flex;
            justify-content: space-around;
            align-items: center;
            padding: 20px;
        }}
        .content {{
            max-width: 30%;
            text-align: center;
            margin-top: 0%;
        }}
        .images {{
            display: flex;
            flex-direction: column;
            max-width: 50%;
        }}
        img {{
            max-width: 100%;
            height: auto;
            margin-bottom: 20px;
        }}
        .left-image {{
            max-width: 100%;
            height: auto;
            margin-bottom: -10px;
            margin-left: -0%;
        }}
        .qr-code {{
            max-width: 200%;
            height: auto;
            /* Add any additional styles for the QR code image container */
        }}
        button#confirmBtn {{
            background-color: blue;
            color: white;
            font-size: 20px;
            padding: 10px 20px;
            border: none;
            cursor: pointer;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="content">
            <div class="left-image">
                <img src="static\ParkingIcon1.png" alt="Left Image">
            </div>
            <h1>Car Number and Charges</h1>
            <p>Car Number: {car_number}</p>
            <p>Total Charges: {total_charge} Rs</p>
        </div>
        <div class="images">
            <div class="qr-code">
                <img src="qr.png" alt="QR Code Image">
            </div>            
        </div>
    </div>
</body>
</html>
"""

import threading
def website():
    global money
    with open("C:\\EazePark\\Sign_Out\\payment_confirmation.html", "w") as html_file:
        html_file.write(html_content)
    time.sleep(3)
    import http.server
    import socketserver
    import webbrowser
    money = False
    class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            global money
            if "/payment_status" in self.path:
                money = True
                self.send_response(200)
                self.end_headers()
                return
            elif "/stop_server" in self.path:
                self.send_response(200)
                self.end_headers()
                self.server.shutdown()
            else:
                self.directory = "C:\\EazePark\\Sign_Out"
                super().do_GET()
    handler = MyRequestHandler
    port = 8080
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving at port {port}")
        webbrowser.open(f"http://localhost:8080/payment_confirmation.html")
        server_thread = threading.Thread(target=httpd.serve_forever)
        server_thread.start()
        while not rr:
            payment_verification()
            if rr:
                windows = [window for window in gw.getWindowsWithTitle('') if 'Payment Confirmation' in window.title]
                httpd.shutdown()
                money=True
                if windows:
                    windows[0].close()

    print(money)
website()
if money:
    adddup()
    time.sleep(5)
    payment_verification()
    if car_number_em==car_number and int(money_paid)==total_charge:
        payment_event=True
        driver=webdriver.Chrome()
        driver.get('file:///C:/EazePark/Sign_Out/templates/thank_you.html')
        import pygetwindow as gw
        window = gw.getWindowsWithTitle('Thank You - Google Chrome')[0]
        window.maximize()
        time.sleep(5)
        driver.quit()
    elif car_number_em==car_number and int(money_paid)!=total_charge:
        driver=webdriver.Chrome()
        driver.get('file:///C:/EazePark/Sign_Out/templates/moneyerr.html')
        import pygetwindow as gw
        window = gw.getWindowsWithTitle('Payment Error - Google Chrome')[0]
        window.maximize()
        time.sleep(20)
        driver.quit()
        website()
        payment_verification()
    elif car_number_em!=car_number:
        website()
        payment_verification()
    if payment_event:
        s.run(["python","C:\\EazePark\\Sign_Out\\Sign_Out.py"])
    else:
        website()
        payment_verification()