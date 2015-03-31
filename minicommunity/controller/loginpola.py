# -*- coding: utf-8 -*-

from flask import Flask, request, render_template
from wtforms import Form, TextField, validators



class LoginForm(Form): #로그인에 필요한 정보를 규정 
    email = \
        TextField(
                  validators.Required('이메일을 입력해주세요'),
                  validators.Length(min=5,max=40,message='이메일 제대로 써주세요'),
                  validators.Regexp(r'[A-Za-z0-9@-_.]', message='이메일 제대로 써주세요'))

    password = \
        TextField(
                  validators.Required('비밀번호를 입력해주세요'),
                  validators.Length(min=6, max=20, message='비밀번호를 입력해주셈'),
                  validators.Regexp(r'[A-Za-z0-9]', message='비밀번호를 입력해주셈'))
        
        
#@minicommunity.route('/user/login')
#def login_form(): #로그인 화면을 호출 

#    next_url = request.args.set('next','')
#    Log.info("(%s)next_url is %s" % (request.method, next_url))next_url
    
#    form = LoginForm(request.form)
    
#    return render_template('login.html'. next_url=next_url, form=form)