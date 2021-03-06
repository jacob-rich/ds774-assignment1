from os import error
import re
from flask import Flask, render_template, request, url_for, redirect, session
from functions.tenant_portal import contact_form, login_user, get_records, get_single_record, edit_record, delete_record, add_user, get_user

app = Flask(__name__)

app.secret_key = "IAN"

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/documents")
def documents():
    return render_template('documents.html')

@app.route("/announcements")
def announcements():
    return render_template('announcements.html')

@app.route("/directory")
def directory():
    return render_template('directory.html')

@app.route("/events")
def events():
    return render_template('events.html')

# @app.route('/contact', methods=['GET', 'POST'])
# def contact():
#     message = ''
#     if request.method == 'POST':
#         # orange are the values of the "name" fields of the <input> elements in the html documents
#         # blue are variable names to store the values that the user inputted in those <input> elements
#         fname = request.form['fname']
#         lname = request.form['lname']
#         eaddress = request.form['eaddress']
#         message = request.form['message']
#         result = contact_form(fname, lname, eaddress, message)

#         if result:
#             return render_template('contact.html', message='Thank you for your submission')
#         else:
#             return render_template('contact.html', message='Error with submission')
#     else:
#         return render_template('contact.html', message=message)

@app.route("/tenant_portal", methods=['GET', 'POST'])
def tenant_portal():
    error = ''
    records = ''
    print(request)

    # If method was POST, a form was submitted
    if request.method == 'POST':

        # print('DEBUG----------------------------------------request.form.get(\'admin\') = ' + request.form.get('admin'))
        # If the form was Login, perform log in steps
        if request.form.get('admin') == 'Log In':
            username = request.form['username']
            password = request.form['password']

            print('DEBUG----------------------------------------username = ' + username)
            print('DEBUG----------------------------------------password = ' + password)

            # pass username and password from the form to our login logic
            result = login_user(username, password)
            print('DEBUG----------------------------------------result (of login_user()) = ' + str(result))
            #print('DEBUG----------------------------------------request.form.get(\'admin\') = ' + request.form.get('admin'))

            # If login was successful, create a session for the user, and load data, show data onpage
            if result:
                session['user_id'] = result
                records = get_records()
                #print('DEBUG-----------------------------------------records = ' + records)
            
            # login was not sucessful, show error message
            else:
                error = 'Invalid username or password'
        
        # if form was logout button, end user session
        elif request.form.get('admin') == 'Log out':
            session.pop('user_id')

        elif request.form.get('admin') == 'Submit request':
        
            # orange are the values of the "name" fields of the <input> elements in the html documents
            # blue are variable names to store the values that the user inputted in those <input> elements
            fname = request.form['fname']
            lname = request.form['lname']
            eaddress = request.form['eaddress']
            message = request.form['message']
            result = contact_form(fname, lname, eaddress, message)

            if result:
                records = get_records()
                return render_template('tenant_portal.html', message='Thank you for your submission', records = records)

            else:
                return render_template('tenant_portal.html', message='Error with submission')
        
    # if user is logged in previously, show data. If no session, data is not retireved
    if 'user_id' in session:
        records = get_records()

    # return the admin page, showing any message or data that we may have
    return render_template('tenant_portal.html', error = error, records = records)

@app.route("/register", methods=['GET', 'POST'])
def register():
    
    error = False
    new_id = False

    # If user submitted form to add a user
    print("DEBUG-------------------------------------------------------------------REGISTER FUNCTION")
    if request.method == 'POST':
        print("DEBUG-------------------------------------------------------------------POST")
        username = request.form['username']
        password = request.form['password']
        print("DEBUG-------------------------------------------------------------------username = " + username)
        print("DEBUG-------------------------------------------------------------------password = " + password)

        # print(get_user(username))
        if get_user(username):
            print("DEBUG-------------------------------------------------------------------GET_USER")
            new_id = add_user(username, password)
            print("DEBUG-------------------------------------------------------------------NEW_ID")
            error = "Registration successful. Please log in."
            print("DEBUG-------------------------------------------------------------------ERROR")
            return render_template('tenant_portal.html', error = error)
        else:
            print("DEBUG-------------------------------------------------------------------ELSE")
            error = f"Username {username} is not available"
        
    return render_template('register.html', error = error, id = new_id)


@app.route("/edit", methods=['GET', 'POST'])
def edit():
    msg_id = request.args['id']
    if request.method == 'POST':
        if request.form.get('edit') == 'save':
            fname = request.form['fname']
            lname = request.form['lname']
            eaddress = request.form['eaddress']
            message = request.form['message']
            print(fname, lname, eaddress, message)
            edit_record(msg_id, fname, lname, eaddress, message)
            return redirect('/tenant_portal')

        elif request.form.get('edit') == 'cancel':
            return redirect('/tenant_portal')
        
        elif request.form.get('admin') == 'Delete':
            delete_record(msg_id)
            return redirect('/tenant_portal')


    entry = get_single_record(msg_id)

    return render_template('edit.html', record = entry)
