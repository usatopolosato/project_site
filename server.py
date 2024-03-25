from flask import Flask, render_template, redirect, request, make_response
from flask import session, abort
from data import db_session
import os
import datetime as dt
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_login import current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = '&&&&&&&&&&'
app.config['PERMANENT_SESSION_LIFETIME'] = dt.timedelta(days=1)
# login_manager = LoginManager()
# login_manager.init_app(app)


@app.route('/')
@app.route('/index')
def index():
    return render_template("base.html")


def main():
    db_session.global_init('db/datebase.db')
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()
