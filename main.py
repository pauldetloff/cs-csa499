from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from mongo_db import account_create, user_checker, get_user, username_checker, leaderboard, check_score
from flask_session import Session
import operator

app = Flask(__name__, 
            static_url_path='',
            static_folder='static',
            template_folder='templates')

app.secret_key = 'a_secret_key'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



# default gamemode
game_mode = "Symbol => Name (1.00x)"

#home page
@app.route('/', methods=["GET", "POST"])
def index():
    leaderboardArray = leaderboard()
    leaderboardScores = []
    leaderboardNames = []
    sorted_leaderboard = sorted(leaderboardArray, key=operator.itemgetter('highscore'))
    sorted_leaderboard.reverse()

    if request.method == "POST":
        game_mode = request.form.get('gm')
        print(game_mode)
        return render_template('index.html', game_mode = game_mode, sorted_leaderboard = sorted_leaderboard[:50])

    return render_template('index.html', game_mode = "Symbol => Name (1.00x)", sorted_leaderboard = sorted_leaderboard[:50])

@app.route('/endGame', methods=["GET", 'POST'])
def endGame():
    score = int(request.form.get('score_output'))
    game_completed = request.form.get('game_completed')
    print(type(game_completed))
    print("COMPLETE? ", game_completed)

    if session["name"]:
        check_score(session["name"], score, game_completed)
    return redirect('/')

#study page
@app.route('/study')
def study():
    return render_template('study.html')

#account page
@app.route('/account')
def account():
    try:
        if session["name"]:
            user = get_user(session["name"])

            username = user['username']
            email = user['email']
            highscore = user['highscore']
            game_count = user['game_count']
            completed_game_count = user['completed_game_count']
            return render_template('account.html', email = email, username=username, highscore = highscore, game_count = game_count, completed_game_count = completed_game_count)
        else:
            return render_template('login.html')
    except:
        return render_template('login.html')

#login page
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username_login = request.form.get('login_username')
        password_login = request.form.get('login_password')

        # check if input credentials match a stored account
        target_user = user_checker(username_login, password_login)
        if target_user:
            session["name"] = username_login

            return redirect('/account')
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')

# logout
@app.route('/logout')
def logout():
    # reset session name to None
    session["name"] = None
    return redirect('/account')

# register
@app.route('/register')
def register():
    return render_template('register.html')

# register checker
@app.route('/register_pass_fail', methods=["GET", "POST"])
def register_pass_fail():
    matched_username = ""
    passed = True
    output = "Username Taken"

    # check if username is taken and password meets requirements
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        if username_checker(username):
            passed = False

        if passed:
            account_create(username, password, email)
            return redirect('/login')
        else:
            return render_template('register.html', output = output)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
