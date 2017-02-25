import flask
import flask_login
from flask_sqlalchemy import SQLAlchemy
from argon2 import PasswordHasher

app = flask.Flask(__name__)
app.debug = True

app.secret_key = "Y7L1xOBu2A0d08zUWO63753m3"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databases/main.db'
ph = PasswordHasher()
db = SQLAlchemy(app)

login_manager = flask_login.LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

class User(db.Model):

   __tablename__ = 'users'

   email = db.Column(db.String(80), primary_key=True, nullable=False)
   password = db.Column(db.String(256), nullable=False)
   # 0 - organization
   # 1 - small business
   # 2 - individual
   accountType = db.Column(db.Integer, nullable=False)
   authenticated = db.Column(db.Boolean, default=False)


   def __init__(self, email, password, accountType):
      self.email = email
      self.fullName = fullName
      self.password = password
      self.authenticated = False
      self.accountType = accountType

   def __repr__(self):
        return '<User e:{0}, u:{1}>'.format(self.email, self.username)

   def is_active(self):
        return True

   def get_id(self):
        return self.email

   def is_authenticated(self):
        return self.authenticated

   def is_anonymous(self):
        return False

def userExists(email):
    return User.query.filter_by(email=email).first()



@login_manager.user_loader
def user_loader(email):
   if userExists(email):
      usr = User.query.filter_by(email=email).first()
      usr.email = email
      return usr
   else:
      return

@login_manager.request_loader
def request_loader(request):
   email = request.form.get('email')
   passw = request.form.get('password')
   if userExists(email):
      user = User.query.get(email)
      if verify_password(user.password, passw):
         return user
   return

@app.route('/logout')
@flask_login.login_required
def logout():
    user = flask_login.current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    flask_login.logout_user()
    return flask.redirect(flask.url_for('index'))

@app.route('/')
def root():
    return flask.render_template('home.html', v1="Example Title", v2="Example Body Content")

def main():
    app.run()

if __name__ == '__main__':
    main()
