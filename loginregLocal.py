from flask import Flask, render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
from mysqlconnection import connectToMySQL
from pwd import Passwords
import re

# from PWD import isPWDValid


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ROUTTES:
# "/" - CHECKS IF LOGGED IN - AND RENDERS WALL OR REDIRECT TO REGISTRATION
# '/login'
# /success
# '/register' - validates pwd, hashes pwd, email, checks for existence of user, 
#               then creates user and redirects to wall
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#ROOT ROUTE REDIRECTS CHECKS IF LOGGED IN
#IF LOGGED IN RENDERS WALL OTHERWISE REGISTRATION 
app = Flask(__name__)
app.secret_key = 't3rc35'
bcrypt = Bcrypt(app)     # we are creating an object called bcrypt, 
@app.route("/")
def rootroute():
    if not (0): #logged in
        # render_template()
        # isValid= isPWDValid("/.&~")

        # EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # if not EMAIL_REGEX.match("vincelavellO@gmail.com"):
        #     print("no match")
        # else:
        #     print("email is valid")
        return render_template("register.html")
    else:    
        return redirect("/users")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# L O G I N
#
@app.route('/login', methods=['POST'])
def login():
#this code is not "dry" copied from register - should be part of another module
    # C H E C K  IF U S E R  A L R E A D Y  E X I S T S
    # see if the username provided exists in the database
    mysql = connectToMySQL("LoginReg")
    query = "SELECT * FROM users WHERE email = %(email)s;"
    data = { "email" : request.form["email"] }
    result = mysql.query_db(query, data)
    if len(result) > 0:
        # assuming we only have one user with this username, the user would be first in the list we get back
        # of course, we should have some logic to prevent duplicates of usernames when we create users
        # use bcrypt's check_password_hash method, passing the hash from our database and the password from the form
        # result[0]['password'], request.form['password']
        if bcrypt.check_password_hash(result[0]['pwd'], request.form['loginpwd']):
            # if we get True after checking the password, we may put the user id in session
            session['user_id'] =result[0]['user_id']
            session['first_name'] = result[0]['first_name']
            session['last_name'] = result[0]['last_name']
            session['email'] = result[0]['email']
            session['pwd'] = "just kidding!"
            # never render on a post, always redirect!
            return redirect('/success')
        else:
        # if we didn't find anything in the database by searching by username or if the passwords don't match,
        # flash an error message and redirect back to a safe route
            flash("You could not be logged in")
            print( "loggin failed" + str(result))
    return redirect("/")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#SHOW ONE USER:
# 
@app.route("/user/<id>/show") #user id is jpassed in from template shows notes
def show_user_form(id):
    db = connectToMySQL('LoginReg')
    showUser= db.query_db('SELECT users.*, user_notes.memo FROM users INNER JOIN user_notes ON users.user_id=user_notes.user_id where users.user_id=' + str(id) + ';') 
    return render_template("user.html", users=showUser)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#SHOW ONE USER after registering:
# 
@app.route("/success")  #user id is stored in session from login  -- no notes
def loggedin():

    db = connectToMySQL('LoginReg')
    showUser= db.query_db('SELECT * FROM users where user_id=' + str(session["user_id"]) + ';') 
    return render_template("user.html", users=showUser)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# L O G  O U T
@app.route("/logout", methods=['POST'])
def logoutuser():
    strfname = session['first_name']
    print(strfname)
    session.clear()
    return render_template("loggedout.html",  fname=strfname)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#SHOW ALL USERS:
@app.route("/users")
def showUsers():
    db = connectToMySQL('LoginReg')
    userlist= db.query_db('SELECT * FROM LoginReg.users;')
    return render_template("users.html", users=userlist)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#ADDS THE USERS SUBMITTED FROM THE ADD ROUTE:
# R E G I S T E R
@app.route('/register', methods=['POST'])
def createUser():
    pwdcheck = Passwords()
    flagInvalidField = False
    #
    #U S E R N A M E  V A L I D A T I O N -- not using; using email
    # strUserName = "Vincent1"
    # If (pwdcheck.isUserNameValid(strFName)):

    strFirstName = request.form["fname"]
    strLastName = request.form["lname"]
    strEmail = request.form["email"]
    #clean names by stripping leading and trailing spaces
    strCleanFName = re.sub(r"^\s+|\s+$", "", strFirstName) 
    strCleanLName = re.sub(r"^\s+|\s+$", "", strLastName)
    strCleanEmail = re.sub(r"^\s+|\s+$", "", strEmail)

    flagInvalidField=((len(strCleanFName)) * (len(strCleanLName)) * (len(strCleanEmail)) == 0)
    if(flagInvalidField):
        flash("Please fill out all fields", "nameemail")
        return redirect('/' )
    print("validating password")
    # P A S S W O R D  V A L I D A T I O N
    strPWD = request.form['pwd']
    # print(strPWD)
    flg = pwdcheck.IsPasswordValid(strPWD)
    # print("PWD FLag:" + str(flg))
    if not (flg == 1):
        print("password error")
        flash("Password requires 8 of upper, lower, number, special characters", "pwd")
        return redirect('/' )
    
    #P A S S W 0 R D  H A S H
    #
    pw_hash = bcrypt.generate_password_hash(strPWD)  
    # print(pw_hash)  
    # print("hashed password")
    # C H E C K  IF U S E R  A L R E A D Y  E X I S T S
    db = connectToMySQL('LoginReg')
    countSQL = 'SELECT Count(Users.email) as CountofUserID FROM Users WHERE (Users.email="' + strCleanEmail  +'");'
    # print(countSQL)
    userExists= db.query_db(countSQL) 
    # print(userExists)
    flgUserEmailExists=userExists[0]['CountofUserID']
    # print("user exists:" + str(flgUserEmailExists))
    if (flgUserEmailExists>0):
        flash("A user exists with the email: " + strCleanEmail)
        return redirect("/")

    # INSERT NEW USER
    #
    dbInsert = connectToMySQL('LoginReg')
    qdfAddUser="INSERT INTO users (first_name, last_name, pwd, email, created_at, updated_at) VALUES(%(fname)s, %(lname)s, %(pwd)s, %(email)s,  NOW(), NOW());"
    # # getform ={"fname": request.form["fname"],"lname": request.form["lname"],"email": request.form["email"]}
    getform ={"fname": strCleanFName,"lname": strCleanLName,"pwd": pw_hash, "email": strCleanEmail}
    newid=dbInsert.query_db(qdfAddUser,getform)
    if not (newid):
        print("figure this one out later.. insert failed")
    else:
        session['user_id'] =newid
        session['first_name'] = strFirstName
        session['last_name'] = strLastName
        session['email'] = strEmail
        session['pwd'] = "just kidding!"
    return redirect("/success")
 
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#PREPOPULATE EDIT USER FORM
@app.route("/users/<id>/edit")
def update_user_form(id):
    # userID = request.args.get('user_id', default = 0, type = int)
    print('SELECT * FROM users where user_id='+ str(id) + ";")
    db = connectToMySQL('LoginReg')
    showUser= db.query_db('SELECT * FROM users where user_id='+ str(id) + ";")
    print(showUser)
    return render_template("update.html", users=showUser)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#SHOW SUBMITTED FROM EDIT USER TO UPDATE USER:
@app.route("/users/<id>/update", methods=['POST'])
def update_user(id):
    db = connectToMySQL('LoginReg')
    getform ={"fname": request.form["fname"],"lname": request.form["lname"],"email": request.form["email"]}
    flgEmptyEntry=((len(request.form["fname"])) * (len(request.form["lname"])) * (len(request.form["email"])) == 0)
    getnotes ={"notes": request.form["notes"]}
    if(flgEmptyEntry):
        return redirect("/users/" + str(id) + "/edit")
    else:
        strsql = "UPDATE users SET users.first_name=%(fname)s,"+ " users.last_name=%(lname)s,"
        strsql +=" users.email=%(email)s WHERE (((users.user_id)=" + str(id) + "));"
        db.query_db(strsql,getform)

    if (len(request.form["notes"]) != 0):
            strnotessql = "INSERT INTO user_notes ( user_notes.user_id, user_notes.memo) VALUES (" + str(id) + ",%(notes)s);"
            dbname = connectToMySQL('LoginReg')
            dbname.query_db(strnotessql,getnotes)
    
    return redirect("/user/" + str(id) + "/show") #2/22

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#IMMEDIATELY AND SUMMARILY DESTROYS USER RECORD WITHOUT PROMPT:
@app.route("/users/<id>/destroy")
def delete_user_Form(id):
    db = connectToMySQL('LoginReg')
    # userID = request.args.get('user_id', default = 0, type = int)
    print("DELETE * FROM users WHERE user_id=" + str(id)+ ";")
    deleted= db.query_db("DELETE Users.* FROM Users WHERE Users.user_id=" + str(id)+ ";")
    print(deleted)
    return redirect("/users")

if __name__ == "__main__":
    app.run(debug=True)