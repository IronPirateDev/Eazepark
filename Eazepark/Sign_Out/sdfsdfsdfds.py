def payment_verification(car_number, total_charge):
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
payment_verification('Tst', '2')
