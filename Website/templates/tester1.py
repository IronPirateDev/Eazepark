import mysql.connector as ms
db=ms.connect(host='localhost',user='root',password='dpsbn',database='sanadi')
cursor=db.cursor()
q1='insert into ayaan (name,marks) values(%s,%s)'
q2=('hello',100)
cursor.execute(q1,q2)
db.commit()
cursor.execute('select * from ayaan')
a=cursor.fetchall()
for i in a:
    print(i)