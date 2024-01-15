import imaplib
import email
from email.header import decode_header

username = "ineazepark@gmail.com"
password = "hqkoabclvofhqlxt"

# Connect to the Gmail server using IMAP
mail = imaplib.IMAP4_SSL("imap.gmail.com")

# Login to the email account
mail.login(username, password)

# Select the mailbox you want to read emails from (e.g., 'inbox')
mail.select("inbox")

# Search for all emails in the selected mailbox, starting from the latest
status, messages = mail.search(None, "ALL")
message_ids = messages[0].split()
message_ids.reverse()  # Reverse the order to start from the latest

# Fetch and print the content of each email
for message_id in message_ids:
    _, msg_data = mail.fetch(message_id, "(RFC822)")
    raw_email = msg_data[0][1]
    msg = email.message_from_bytes(raw_email)

    # Decode and print the subject


    # If the email is multipart, extract the text content
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body=part.get_payload(decode=True).decode("utf-8")
                body=body.split('<br>')
                ft=''
                ft=body[0]+'\n'+body[1]
                print(ft)
                break
    else:
        # If the email is not multipart, directly extract the text content
        print("Body2:", msg.get_payload(decode=True).decode("utf-8"))

# Logout and close the connection
mail.logout()
