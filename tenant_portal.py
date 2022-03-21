import os
import psycopg2

def connect_to_db():
    connection = None
     # Connect to database
    try:
        # get database URL dynamically from Heroku
        DATABASE_URL = os.environ['DATABASE_URL']
        
        # create connection with database
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')

    except:
        print('error connecting to database')
    
    return connection


def contact_form(fname, lname, eaddress, message):
    
    conn = connect_to_db()

    sql = f"INSERT INTO contacts(fname,lname,eaddress,message) VALUES('{fname}', '{lname}', '{eaddress}', '{message}');"
    try:

        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return False
    finally:
        if conn is not None:
            conn.close()

def add_user(user, password):
    """ insert a new user into the users table """
    sql = f"INSERT INTO users(username,password) VALUES('{user}','{password}') RETURNING user_id;"
    conn = None
    user_id = None

    conn = connect_to_db()
    try:
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql)
        # get the generated id back
        user_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return user_id

def get_user(user):

    conn = connect_to_db()

    sql = f"SELECT * FROM users WHERE username ='{user}';"

    try:

         # create a new cursor
        cur = conn.cursor()
        # execute the SELECT statement
        cur.execute(sql)
        # get the selected users back
        users = cur.fetchall()
        # close communication with the database
        cur.close()

        # check if user with same name already exists
        if len(users) >= 1:
            return False
        else:
            return True

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def login_user(user, password):
    
    conn = connect_to_db()

    sql = f"SELECT * FROM users WHERE username ='{user}' and password = '{password}';"

    try:

        # create a new cursor
        cur = conn.cursor()
        # execute the SELECT statement
        cur.execute(sql)
        # get the selected users back
        users = cur.fetchall()
        # close communication with the database
        cur.close()

        # check if user credentials were correct
        if len(users) == 1:
            return users[0][0]
        else:
            return False

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def get_records():
    conn = connect_to_db()

    sql = f"SELECT * FROM contacts ORDER BY message_id ASC;"

    try:

        # create a new cursor
        cur = conn.cursor()
        # execute the SELECT statement
        cur.execute(sql)
        # get the data back
        records = cur.fetchall()
        # close communication with the database
        cur.close()
        
        # return data
        return records

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def get_single_record(message_id):
    conn = connect_to_db()

    sql = f"SELECT * FROM contacts where message_id = '{message_id}';"

    try:

        # create a new cursor
        cur = conn.cursor()
        # execute the SELECT statement
        cur.execute(sql)
        # get the selected record back
        records = cur.fetchone()
        # close communication with the database
        cur.close()

        # return retieved record
        return records

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def edit_record(message_id, fname, lname, eaddress, message):
    conn = connect_to_db()

    sql = f"update contacts set fname='{fname}',lname='{lname}',eaddress='{eaddress}',message='{message}' where message_id='{message_id}';"

    try:

        # create a new cursor
        cur = conn.cursor()
        # execute the SELECT statement
        cur.execute(sql)
        # commit changes to database
        conn.commit()
        # close communication with the database
        cur.close()
        

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def delete_record(message_id):
    
    conn = connect_to_db()

    sql = f"DELETE FROM contacts WHERE message_id = {message_id};"

    try:

        # create a new cursor
        cur = conn.cursor()
        # execute the SELECT statement
        cur.execute(sql)
        # commit changes to database
        conn.commit()
        # close communication with the database
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    