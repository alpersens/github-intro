import psycopg2
connection = psycopg2.connect(user="postgres",password="12345",host="localhost", port="5432",database="deneme")
# Create a cursor to perform database operations
cursor = connection.cursor()
# Print PostgreSQL details
print("PostgreSQL server information")
print(connection.get_dsn_parameters(), "\n")
# Executing a SQL query
#cursor.execute("INSERT into book(book_name,writer,type_id) values(%s,%s,%s)",('Don Kişot','Atatürk',1))
#cursor.execute("DELETE from book WHERE book_id=7;")
#cursor.execute("SELECT book_id,book_name  FROM book")
while(1):
    order=input("What do you want? Barrow or list books :")
    if(order=="list"):
        cursor.execute("SELECT book_id,book_name,writer,type_id  FROM book")
        row = cursor.fetchall()
        for r in row:
            print(f"id:{r[0]} name: {r[1]} writer: {r[2]}")
    elif(order=="barrow"):
        found=0
        available=0
        Student_id=input("Student_id: ")
        Book_id=input("Book_id: ")
        print("Checking Book is available:")
        cursor.execute("SELECT book_name FROM book WHERE book_id={0}".format(Book_id))
        Book_Name = cursor.fetchall()
        cursor.execute("SELECT student_id  FROM book_student WHERE book_id={0}".format(Book_id))
        Student_info=cursor.fetchall()
        if(len(Book_Name)!=0):
            print("Book name is ",Book_Name[0][0])
        else:
            print("There is no book with such that name...")
            print("Please Enter again...")
        if(len(Student_info)==0):
            print("Book is available...")
            cursor.execute("INSERT into book_student(book_id,student_id) values(%s,%s)", (Book_id,Student_id))
            connection.commit()
            continue
        else:
            print("Book is not available...")
            continue
    elif(order=="profile"):
        Student_id=input("Student ID:")
        cursor.execute("SELECT book_id  FROM book_student WHERE student_id={0}".format(Student_id))
        profile=cursor.fetchall()
        for i in profile:
            cursor.execute("SELECT book_name,writer  FROM book WHERE book_id={0}".format(i[0]))
            book_info=cursor.fetchall()
            print("Book ID :",i[0], "//Book Name : ",book_info[0][0],"//Writer : ",book_info[0][1])
    elif(order=="deliver"):
        found=0
        Student_id = input("Student ID:")
        Book_id = int(input("Book_id: "))
        cursor.execute("SELECT book_id  FROM book_student WHERE student_id={0}".format(Student_id))
        deliver=cursor.fetchall()
        for i in deliver:
            if(Book_id==i[0]):
                found=1

        if(found==1):
            cursor.execute("DELETE  from book_student WHERE book_id={0}".format(Book_id))
            print("Delivery is successfully complete...")
            connection.commit()
        else:
            print("Try again...")
    elif(order=="quit"):
        break
