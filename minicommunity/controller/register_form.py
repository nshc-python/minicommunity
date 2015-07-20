# -*- coding: utf-8 -*-
'''
Created on 2015. 7. 13.

@author: Soobin
'''
from wtforms.form import Form
from wtforms.fields.simple import TextField, PasswordField, HiddenField
from wtforms import validators
from wtforms.validators import InputRequired, Email, Length, Required

class RegisterForm(Form):
    # 사용자 등록화면에서 입력값을 검증
    r_email = TextField('Email',
                      validators=[InputRequired('Email을 입력하세요.'),
                                  Length(
                                         min=5,
                                         max=40,
                                         message='5자 이상 40자 이하로 입력하세요.'),
                                  Email(message='이메일 형식에 맞지 않습니다.')])
    
    r_nickname = TextField('Nickname',
                         validators=[Required('화면에 표시될 닉네임을 입력하세요.'),
                                     Length(
                                            min=2,
                                            max=30,
                                            message='2자이상 30자 이하로 입력하세요.')])
    
    r_password = PasswordField('New password',
                             [validators.Required('비밀번호를 입력하세요.'),
                              validators.Length(
                                                min=4,
                                                max=20,
                                                message='4자이상 20자 이하로 입력하세요.'),
                              validators.EqualTo('r_password_confirm',
                                                 message='비밀번호가 일치하지 않습니다.')])
    
    r_password_confirm = PasswordField('Confirm password')
    
    r_email_check = HiddenField('Check email',
                                 [validators.Required('중복되는 이메일이 있습니다.')])
    
    r_nickname_check = HiddenField('Check nickname',
                                 [validators.Required('중복되는 닉네임이 있습니다.')])