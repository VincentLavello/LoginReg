from flask import Flask, render_template, redirect, request
from mysqlconnection import connectToMySQL
@app.route('/a')
def a():
    pass
    # session['my_var'] = 'my_value'
    # return redirect(url_for('b'))
# bcrypt.generate_password_hash(password_string)
# bcrypt.check_password_hash(hashed_password, password_string)
# generate_password_hash()

@app.route('/b')
def b():
    pass
    # my_var = session.get('my_var', None)
    # return my_var