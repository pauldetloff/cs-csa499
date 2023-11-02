from flask import Flask, render_template, redirect, request, session
from mongo_db import account_create, login_checker, username_checker
from flask_session import Session

app = Flask(__name__, 
            static_url_path='',
            static_folder='static',
            template_folder='templates')

app.secret_key = 'a_secret_key'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#home page
@app.route('/')
def index():
    return render_template('index.html')

#login page
# flask session: https://www.geeksforgeeks.org/how-to-use-flask-session-in-python-flask/#
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username_login = request.form.get('login_username')
        password_login = request.form.get('login_password')

        # check if input credentials match a stored account
        check_user = login_checker(username_login, password_login)
        print(username_login, password_login)
        if check_user:
            session["name"] = username_login
            return render_template('login.html')
        else:
            return render_template('login.html')
    
    else:
        return render_template('login.html')

# logout
@app.route('/logout')
def logout():
    # reset session name to None
    session["name"] = None
    return render_template('login.html')

# register
@app.route('/register')
def register():
    pass_len = "*Password must be 8 or more characters."
    numbers = "*Password must end in a number."
    upper = "*Password must contain uppercased character."
    lower = "*Password must contain lowercased character."
    usernameRQ = "*Username must be 5 or more characters."
    unique_user = "*Username must be unique."

    return render_template('register.html', 
                            output="Password Requirements", 
                            pass_len=pass_len,
                            numbers=numbers, 
                            lower=lower, 
                            upper=upper,
                            output2="Username Requirments",
                            usernameRQ=usernameRQ,
                            unique_user=unique_user)

# register checker
@app.route('/register_pass_fail', methods=["GET", "POST"])
def register_pass_fail():
    matched_username = ""
    passed = True

    # check if username is taken
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        #check_username = username_checker(username)
        #if check_username:
        #    passed = False
        #    matched_username = "*Username already in use"
        #else:
        #    passed = True

        #if passed:
        account_create(username,password,email)
        return render_template('successful.html', output="Account Creation Successful!")
        #else:
        #    'TODO'


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
