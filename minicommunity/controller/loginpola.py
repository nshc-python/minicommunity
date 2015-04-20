# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, session
from wtforms import Form, TextField, validators
from minicommunity.minicommunity_logger import Log
from minicommunity.minicommunity_blueprint import minicommunity

@minicommunity.route('/member/login')
def login_form(): #로그인 화면을 호출 
    
    next_url = request.args.get('next','')
    regist_email = request.args.get('regist_email','')
    update_email = request.args.get('update_email','')
    Log.info("(%s)next_url is %s" % (request.method, next_url))
    form = LoginForm(request.form)
    
    return render_template('login_test.html', next_url=next_url, form=form, regist_email=regist_email, update_email=update_email)

#@minicommunity.route('/member/login', method=['post'])
# def login(): #로그인 프로세싱 
#     
#     form = LoginForm(request.form) #개체.속성
#     next_url = form.next_url.data
#     login_error = None
#     
#     if form.validate(): #로그인 인증의 성공할 경우 
#         session.permanent = True #서버측 세션 생성 
#         
#         email = form.email.data
#         password = form.password.data
#         next_url = form.next_url.data
#         
#         Log.info("(%s)next_url is %s" % (request.method, next_url))
# 
#         try:          

class LoginForm(Form): #로그인에 필요한 정보를 규정 
    email = \
        TextField('email',[
                validators.Required('이메일을 입력해주세요'),
                validators.Length(min=5,max=40,message='이메일 제대로 써주세요'),
                validators.Regexp(r'[A-Za-z0-9@-_.]', message='이메일 제대로 써주세요')])

    password = \
        TextField('password',[
                validators.Required('비밀번호를 입력해주세요'),
                validators.Length(min=6, max=20, message='비밀번호를 입력해주셈'),
                validators.Regexp(r'[A-Za-z0-9]', message='비밀번호를 입력해주셈')])