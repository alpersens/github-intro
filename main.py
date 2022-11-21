import psycopg2
connection = psycopg2.connect(user="postgres",password="12345",host="localhost", port="5432",database="deneme")
# Create a cursor to perform database operations
cursor = connection.cursor()
# Print PostgreSQL details
print("PostgreSQL server information")
print(connection.get_dsn_parameters(), "\n")
# Executing a SQL query
while(1):
    order=input("What do you want? Barrow or list books :")
    if(order=="list"):#Listing all books
        cursor.execute("SELECT book_id,book_name,writer,type_id  FROM book")
        row = cursor.fetchall()
        for r in row:
            print(f"id:{r[0]} name: {r[1]} writer: {r[2]}")
    elif(order=="barrow"):
        Student_id=input("Student_id: ")
        Book_id=input("Book_id: ")
        print("Checking Book is available:")
        cursor.execute("SELECT book_name FROM book WHERE book_id={0}".format(Book_id))#Find Book name
        Book_Name = cursor.fetchall()
        cursor.execute("SELECT student_id  FROM book_student WHERE book_id={0}".format(Book_id))#Search if book is barrow by someone
        Student_info=cursor.fetchall()
        if(len(Book_Name)!=0):#Check wheter Bookname is correct or not
            print("Book name is ",Book_Name[0][0])
        else:
            print("There is no book with such that name...")#If it is not, then continue
            print("Please Enter again...")
            continue
        if(len(Student_info)==0):#Check book is barrowed by someone else and if there exist student with that ID
            print("Book is available and added to student profile with id ",Student_id)#If it is not, add book to the students profile
            cursor.execute("INSERT into book_student(book_id,student_id) values({0},{1})".format(Book_id,Student_id))
            connection.commit()
            continue
        else:
            print("Student does not exist or book is not available  please try again...")
            continue
    elif(order=="profile"):#list students profile
        Student_id=input("Student ID:")
        cursor.execute("SELECT book_id  FROM book_student WHERE student_id={0}".format(Student_id))
        profile=cursor.fetchall()
        for i in profile:
            cursor.execute("SELECT book_name,writer  FROM book WHERE book_id={0}".format(i[0]))
            book_info=cursor.fetchall()
            print("Book ID :",i[0], "//Book Name : ",book_info[0][0],"//Writer : ",book_info[0][1])
    elif(order=="deliver"):#Deliver Book
        found=0
        Student_id = input("Student ID:")
        Book_id = int(input("Book_id: "))
        cursor.execute("SELECT book_id  FROM book_student WHERE student_id={0}".format(Student_id))
        deliver=cursor.fetchall()
        for i in deliver:#Check book name is deliverable
            if(Book_id==i[0]):
                found=1

        if(found==1):#if it is deliverable, then do it
            cursor.execute("DELETE  from book_student WHERE book_id={0}".format(Book_id))
            print("Delivery is completed successfully ...")
            connection.commit()
        else:
            print("There is no book with that name belongs to someone...")
    elif(order=="quit"):#Close program
        connection.close()

        break
