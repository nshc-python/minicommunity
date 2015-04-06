# -*- coding: utf-8 -*-
'''
Created on 2015. 4. 6.

@author: Soobin
'''
from minicommunity.minicommunity_blueprint import minicommunity

from flask import request
from flask.templating import render_template
from wtforms.form import Form
from wtforms.fields.simple import TextField, PasswordField, HiddenField
from wtforms import validators


@minicommunity.route('/user/register')
def register_user_form():
    form = RegisterForm(request.form)
    
    return render_template('register_sample.html', form=form)

class RegisterForm(Form):
    # 사용자 등록화면에서 입력값을 검증
    email = TextField('Email',
                      [validators.Required('Email을 입력하세요.'),
                       validators.Length(
                                         min=5,
                                         max=40,
                                         message='5자 이상 40자 이하로 입력하세요.'),
                       validators.Email(message='이메일 형식에 맞지 않습니다.')])
    
    nickname = TextField('Nickname',
                         [validators.Required('화면에 표시될 닉네임을 입력하세요.'),
                          validators.Length(
                                            min=2,
                                            max=30,
                                            message='2자이상 30자 이하로 입력하세요.')])
    
    password = PasswordField('New password',
                             [validators.Required('비밀번호를 입력하세요.'),
                              validators.Length(
                                                min=4,
                                                max=20,
                                                message='4자이상 20자 이하로 입력하세요.'),
                              validators.EqualTo('password_confirm',
                                                 message='비밀번호가 일치하지 않습니다.')])
    
    password_confirm = PasswordField('Confirm password')
    
    nickname_check = HiddenField('Check nickname',
                                 [validators.Required('중복되는 닉네임이 있습니다.')])