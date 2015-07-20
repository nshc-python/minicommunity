# -*- coding: utf-8 -*-
'''
Created on 2015. 7. 13.

@author: Soobin
'''
from wtforms.form import Form
from wtforms.fields.simple import TextField, PasswordField, HiddenField
from wtforms import validators
from wtforms.validators import InputRequired, Email, Length, Required

class LoginForm(Form): #로그인에 필요한 정보를 규정 
    email = \
        TextField('email',[
                InputRequired('이메일 적는걸 잊으셨나봐요.'),
                validators.Length(min=5,max=40,message='이메일을 5~40자 사이로 입력해주세요'),
                Email(message='이메일 형식에 맞지 않습니다.')])

    password = \
        PasswordField('password',[
                validators.Required('비밀번호를 입력하지 않으셨습니다.'),
                validators.Length(min=4, max=20, message='비밀번호를 4자 이상, 20자 미만 입력해주세요')])
    
    next_url = HiddenField('next_url')