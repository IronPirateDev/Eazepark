import mysql.connector as ms
import random
from datetime import datetime, timedelta

# Connect to the database
db = ms.connect(
    host="localhost",
    user="root",
    password="dpsbn",
    database="cars"
)
cursor = db.cursor()

# Generate 20 random Indian car numbers
def generate_car_number():
    state_code = random.choice(['AP', 'AR', 'AS', 'BR', 'CG', 'GA', 'GJ', 'HR', 'HP', 'JH', 'KA', 'KL', 'MP', 'MH', 'MN', 'ML', 'MZ', 'NL', 'OR', 'PB', 'RJ', 'SK', 'TN', 'TG', 'TR', 'UP', 'UK', 'WB'])
    district_code = random.randint(10, 99)
    letters = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(2))
    number = random.randint(1000, 9999)
    return f"{state_code} {district_code} {letters} {number}"

# Generate random timestamp between 21-09-2023 and 28-09-2023
def generate_random_timestamp():
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    return random_date.strftime("%Y-%m-%d %H:%M:%S")

# Generate random amount paid (assuming it's in INR)
def generate_random_amount():
    return round(random.uniform(100, 2000), 2)

# Create a list of 20 random entries
entries = []

for _ in range(1000):
    car_number = generate_car_number()
    timestamp = generate_random_timestamp()
    amount_paid = generate_random_amount()
    entries.append((car_number, timestamp, amount_paid))

# Insert data into the database
for entry in entries:
    cursor.execute("INSERT INTO rep (car_number, timestamp, money_paid) VALUES (%s, %s, %s)", entry)

# Commit changes and close the connection
db.commit()
db.close()