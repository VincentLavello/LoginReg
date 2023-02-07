from flask import Flask, render_template, redirect
import re
#from pwd import Passwords

app = Flask(__name__)
@app.route("/")
def rootroute():

    # strusername = "Vincent"
    #pwdcheck = Passwords()
    # s = " hello world "
    # mod = re.sub(r"^\s+|\s+$", "", s)
    # print ("mod =" + mod )
    # print('Remove leading and trailing spaces using RegEx:\n' + mod)  # | for OR condition


    # print("checking user name:" + str(pwdcheck.isUserNameValid(strusername)))
    # pwdcheck = Passwords()
    #flg = pwdcheck.IsPasswordValid("John3:!6")
    flg = True
    print(flg)
    return render_template("users.html")

if __name__ == "__main__":
    app.run(debug=True)