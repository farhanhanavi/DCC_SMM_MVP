from flask import render_template, url_for, flash, redirect, request
from flaskblog.__innit__ import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, IssueKeywordForm, GejalaForm
from flaskblog.models import User, ContactHistory, Symptoms
from flask_login import login_user, logout_user, current_user, login_required
import requests as req

#MAIN LOGIN PAGE
@app.route('/')
@app.route('/home')
def home():
    return render_template('main_login.html', title = 'Home')

#LOGIN PAGE
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    #Validation for user
    #String validation
    if form.validate_on_submit():
        return redirect(url_for('main_page'))
    return render_template('login.html', title='Login', form=form)

#MAIN PAGE
@app.route('/main_page', methods = ['GET','POST'])
def main_page():
    form = IssueKeywordForm()
    #Save submitted file
    if form.validate_on_submit():
        query   = request.form['query']
        fromdate= request.form['fromdate']
        todate  = request.form['todate']
        result_dict =   {'query':query, 'fromdate':fromdate, 'todate':todate}
        #Kirim dict hasil result ke /result
        req.post('http://127.0.0.1:5000/result', params=result_dict)
        #Redirect to /result
        return redirect(url_for('result'))
    return render_template('main_page.html', title = 'Cek resiko infeksi online', form = form)


@app.route('/result', methods = ['GET','POST'])
def result():
    if request.method == 'POST':
        json     =   request.get_json()
        return json
    if request.methods == 'GET':
        return 'hehe'


@app.route('/register', methods = ['GET','POST'])
def register():
   form = RegistrationForm()
   if form.validate_on_submit(): 
       hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
       user = User(ktp = form.ktp.data, nama = form.nama.data, jenis_kelamin = form.jenis_kelamin.data, alamat = form.alamat.data, email = form.email.data, nomor_hp = form.nomor_hp.data, umur = form.umur.data, password = hashed_password)
       db.session.add(user)
       db.session.commit()
       flash(f'Akun berhasil terdaftar untuk {form.nama.data}', 'success')
       return redirect(url_for('login'))
   return render_template('pendaftaran.html', title = 'Halaman Pendaftaran', form = form)

@app.route('/profile')
@login_required
def profile():
   post = ContactHistory.query.all()
   return render_template('profile.html', title = ' Profil', posts=post)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))