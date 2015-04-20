# -*- coding: utf-8 -*-
'''
Created on 2015. 4. 6.

@author: Soobin
'''
from minicommunity.minicommunity_blueprint import minicommunity
from minicommunity.minicommunity_logger import Log
from minicommunity.minicommunity_database import dao
from minicommunity.model.member import Member

from flask import request, url_for, jsonify
from flask.templating import render_template
from wtforms.form import Form
from wtforms.fields.simple import TextField, PasswordField, HiddenField
from wtforms import validators
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect
from sqlalchemy.types import DateTime


@minicommunity.route('/member/register')
def register_member_form():
    form = RegisterForm(request.form)
    
    Log.debug('aaa')
    
    return render_template('register_sample.html', form=form)

@minicommunity.route('/member/register_proc',methods=['POST'])
def register_member():
    '''미니 커뮤니티 사용자 등록하는 액션'''
    form = RegisterForm(request.form)
    
    if form.validate():
        email = form.email.data
        nickname = form.nickname.data
        password = form.password.data
#         password_confirm = form.password_confirm.data
        
        try:
            member = Member(email, generate_password_hash(password), nickname, DateTime.datetime())
            dao.add(member)
            dao.commit()
            
            Log.debug(member)
            
        except Exception as e:
            error = "DB error occurs" + str(e)
            Log.error(error)
            dao.rollback()
            raise e
        
        else:
            # 성공적으로 사용자 등록이 되면 로그인 화면으로 이동한다.
            return redirect(url_for('.loginpola',
                                    register_member_name=nickname))
            
    else:
        return render_template('register_sample.html', form=form)
    

@minicommunity.route('/member/check_email', methods=['POST'])
def check_email():
    email = request.json['email']
    #: DB에서 email 중복 확인 
    if __get_member(email) :
        return jsonify(result = False)
    else:
        return jsonify(result = True)


def __get_member(email):
    try:
        current_member = dao.query(Member) \
                            .filter_by(email=email) \
                            .first()
        
        Log.debug(current_member)
        return current_member
    except Exception as e:
        Log.error(str(e))
        raise e
            

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