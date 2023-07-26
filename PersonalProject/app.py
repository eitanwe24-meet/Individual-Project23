from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase


config = {
  "apiKey": "AIzaSyB6Sbyy_x6dFHsgZCwRIhrlrlcXeekQbrA",
  "authDomain": "project-335d9.firebaseapp.com",
  "projectId": "project-335d9",
  "storageBucket": "project-335d9.appspot.com",
  "messagingSenderId": "877748833029",
  "appId": "1:877748833029:web:292798b87cb9a7b35f856c",
  "databaseURL": "https://project-335d9-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here

@app.route('/', methods = ['POST','GET'] )
def home():
    if request.method == "POST":
      bio = request.form['shoe']
      price = request.form['price']
      image = request.form['image']
      try:
        UID = login_session['user']['localId']
        shoes = {'bio':bio, 'price':price,'image': image}
        db.child("Users").child(UID).child('Cart').push(shoes)
        return render_template("index.html")
      except:
        pass
    UID = login_session['user']['localId']
    return render_template("index.html", email = db.child('Users').child(UID).get().val()['email'])




@app.route('/sign_in', methods = ['POST','GET'])
def sign_in():
    erorr = ""
    if request.method == "POST":
        password = request.form['password']
        email = request.form['email']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user = {'password':password, 'email':email}
            db.child("Users").child(UID).set(user)
            return redirect(url_for('home'))
        except:
            error = "Authentication failed  "
    
    return render_template("signin.html")
@app.route('/sign_up', methods = ['POST','GET'])
def sign_up():
    erorr = ""
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user = {'name':name, 'name': name, 'email':email}
            db.child("Users").child(UID).set(user)
            return redirect(url_for('home'))
        except:
          error = "Authentication failed  "
    return render_template("signup.html",)

@app.route('/cart', methods = ['POST','GET'])
def cart():
  UID = login_session['user']['localId']
  products = db.child("Users").child(UID).child('Cart').get().val()
  return render_template('cart.html', products = products)


@app.route('/sign_out')
def signout():
    
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('sign_in'))

@app.route('/search', methods=['POST','GET'])
def search():
  if request.method == 'POST':
    search = request.form['search']
    bio = request.form['bio']
    

#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)