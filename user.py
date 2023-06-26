import sqlite3
from sqlite3 import Error
import csv

COLUMNS=("first_name",
         "last_name",
         "company_name",
         "address",
         "city",
         "county",
         "state",
         "zip",
         "phone1",
         "phone2",
         "email",
         "web"
)
def create_connection():
    try:
        con=sqlite3.connect("user.sqlite3")
        return con
    except Error:
        print("connection error.")
    except Exception as e:
        print(e)
        

def create_table(con):
    CREATE_USER_TABLE_QUERY="""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name CHAR(255) NOT NULL,
            last_name CHAR(255) NOT NULL,
            company_name CHAR(255) NOT NULL,
            address CHAR(255) NOT NULL,
            city CHAR(255) NOT NULL,
            county CHAR(255) NOT NULL,
            state CHAR(255) NOT NULL,
            zip REAL NOT NULL,
            phone1 CHAR(255) NOT NULL,
            phone2 CHAR(255),
            email CHAR(255) NOT NULL,
            web text
        );
    
    """
    
    
    cur=con.cursor()
    cur.execute(CREATE_USER_TABLE_QUERY)
    print("successfulley create the table.")
    


INPUT_STRING="""
Enter the options:
    1. CREATE TABLE
    2. DUMP users from csv INTO users TABLE
    3. ADD new user INTO users TABLE
    4. QUERY all users from TABLE
    5. QUERY user by id from TABLE
    6. QUERY specified no. of records from TABLE
    7. DELETE all users
    8. DELETE users by id
    9. UPDATE user
    10. press any key to EXIT
"""


def read_csv():
    user_data=[]
    with open("sample_users.csv") as f:
        users=csv.reader(f)
        for user in users:
            user_data.append(tuple(user))
    return user_data[1:]  


def insert_users(con,users):
    user_add_query="""
    iNSERT INTO users
    (first_name,last_name,company_name,address,city,county,state,zip,phone1,phone2,email,web)
    vALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """ 
    
               
    cur=con.cursor()
    cur.executemany(user_add_query,users)
    con.commit()
    print(f"{len(users)} were imported successsfulley.")
    
    
    
def select_all_users(con, no_of_records=0):
    cur=con.cursor()
    user_query="SELECT * from users;"
    users=cur.execute(user_query)
    for i, user in enumerate(users):
        if no_of_records==i:
            break
        print(user)
        
        
        
def delete_all_users(con):
    cur=con.cursor()
    cur.execute("DELETE from users;")
    con.commit()
    print(" all users were deleted successfulley")
    

        
def select_user_by_id(con,user_id):
    cur=con.cursor()
    users=cur.execute("select * from users where id=?",(user_id,))
    for user in users:
        print(user)
        
        
def delete_user_by_id(con,user_id):
    cur=con.cursor()
    cur.execute("DELETE from users where id=?",(user_id,))
    con.commit()
    print(f"user with id{user_id} was deleted successfulley.")
    
    
def update_user(con,user_id,column_name,column_value):
    cur=con.cursor()
    cur.execute(
        f"UPDATE users set{column_name}=? where id=?;", (column_value,user_id)
    )
    con.commit()
    print(
        f"{column_name} of user with id{user_id} was updated with new value{column_value}"
    
    )
        
    
    

    

def main():
    con=create_connection()
    user_input=input(INPUT_STRING)
    if user_input=="1":
        create_table(con)
    elif user_input=="2":
        users=read_csv()
        insert_users(con,users)
    elif user_input=="3":
        column_data=[]
        for c in COLUMNS:
            c_value=input(f"enter the value of {c}:")
            column_data.append(c_value)
        users=[tuple(column_data)]
        insert_users(con,users)
        
        
    
    elif user_input=="4":
        select_all_users(con)
        
        
        
    elif user_input=="5":
        user_id=input("enter the id of user:")
        select_user_by_id(con, user_id)
        
        
        
    elif user_input=="6":
        no_of_records=input("enter the number of records you want to fetch:")
        if no_of_records.isnumeric() and int(no_of_records)>0:
            select_all_users(con,int(no_of_records))
            
            
            
    elif user_input=="7":
        confirm=input("are you sure? please type y or yes to continue:")
        if confirm.lower() in ["y", "yes"]:
            delete_all_users(con) 
            
            
        
    elif user_input=="8":
        user_id=input("enter the id of user:")
        if user_id.isnumeric():
            delete_user_by_id(con,user_id)
            
            
            
    elif user_input=="9":
        user_id=input("enter the id of user:")
        if user_id.isnumeric():
            column_name=input(f"enter the name of column.please make sure column is within{COLUMNS}:")
            if column_name in COLUMNS:
                column_value=input(f"enter the value of column{column_name}")
                update_user(con,user_id,column_name,column_value)
                
    
            
# if run as main script
if __name__=="__main__":
    main()
