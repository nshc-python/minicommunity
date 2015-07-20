# -*- coding: utf-8 -*-
'''
Created on 2015. 7. 13.

@author: Soobin
'''
from wtforms.form import Form
from wtforms.fields.simple import TextField, PasswordField, HiddenField
from wtforms import validators

class LoginForm(Form): #로그인에 필요한 정보를 규정 
    email = \
        TextField('email',[
                validators.Required('이메일을 입력해주세요'),
                validators.Length(min=5,max=40,message='이메일 제대로 써주세요')])

    password = \
        PasswordField('password',[
                validators.Required('비밀번호를 입력해주세요'),
                validators.Length(min=5, max=20, message='비밀번호를 입력해주셈')])
    
    next_url = HiddenField('next_url')