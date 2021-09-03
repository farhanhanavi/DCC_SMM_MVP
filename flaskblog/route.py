from flask import render_template, url_for, flash, redirect, request
from flaskblog.__innit__ import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, IssueKeywordForm, GejalaForm
from flaskblog.models import User, ContactHistory, Symptoms
from flask_login import login_user, logout_user, current_user, login_required
import requests as req
import json
import os
import pickle

from get_data import convert_tweets

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
        query           = request.form['query']
        fromdate        = request.form['fromdate']
        todate          = request.form['todate']
        result_dict     = {'query':query, 'fromDate':fromdate, 'toDate':todate}
        #Convert to specified json format
        result_dict    = convert_tweets(result_dict)
        result_dict    = json.dumps(result_dict)
        #Save cookie and redirect to /show_result
        response = redirect(url_for('show_result'))
        response.set_cookie('YourSessionCookie', result_dict)
        return response

    return render_template('main_page.html', title = 'Cek resiko infeksi online', form = form)


@app.route('/result', methods = ['POST'])
def result():

    #Jsonify body post
    json     =   request.get_json()
    return convert_tweets(json)


@app.route('/show_result', methods = ['GET'])
def show_result():

    result = request.cookies.get('YourSessionCookie')
    result = json.loads(result)

    #print(os.getcwd())
    #with open('./flaskblog/static/dummy.pickle','rb') as f:
    #    result = pickle.load(f)
    

    return render_template('result_page.html', title = 'Halaman Hasil', result=result)

















@app.route('/profile')
@login_required
def profile():
   post = ContactHistory.query.all()
   return render_template('profile.html', title = ' Profil', posts=post)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))