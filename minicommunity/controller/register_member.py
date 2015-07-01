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
#from sqlalchemy.types import DateTime
from datetime import datetime


@minicommunity.route('/member/register')
def register_member_form():
    form = RegisterForm(request.form)
    
    Log.debug('form good :')
    Log.debug(request)  
    return render_template('member_register.html', form=form)

@minicommunity.route('/member/register_proc',methods=['POST'])
def register_member():
    '''미니 커뮤니티 사용자 등록하는 액션'''
    
    rform = RegisterForm(request.form)

    if rform.validate():
        email = rform.r_email.data
        nickname = rform.r_nickname.data
        password = rform.r_password.data
        
        Log.debug('r_email : '+str(rform.r_email.data))    
        Log.debug('r_nickname : '+str(rform.r_nickname.data))    
        Log.debug('r_password_o : '+str(rform.r_password.data))    
        Log.debug('r_password_c : '+str(rform.r_password_confirm.data))
        Log.debug('r_email_check : '+str(rform.r_email_check.data))
        Log.debug('r_nickname_check : '+str(rform.r_nickname_check.data))
            
        try:
            member = Member(email, generate_password_hash(password), nickname, datetime.today(), datetime.today())
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
            return redirect(url_for('.login',
                                    register_member_name=nickname))
            
    else:
        return redirect(url_for('.login', form=rform))
    

@minicommunity.route('/member/check_email', methods=['POST'])
def check_email():
    email = request.json['email']
    
    Log.debug('email : '+email)
    
    #: DB에서 email 중복 확인 
    if __get_member(email) :
        return jsonify(result = False)
    else:
        return jsonify(result = True)
    

@minicommunity.route('/member/check_nickname', methods=['POST'])
def check_nickname():
    nickname = request.json['nickname']
    
    Log.debug('nickname : '+nickname)
    
    #: DB에서 nickname 중복 확인 
    if __get_member_from_nickname(nickname) :
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
    
def __get_member_from_nickname(nick):
    try:
        current_member = dao.query(Member) \
                            .filter_by(nickname=nick) \
                            .first()
        
        Log.debug(current_member)
        return current_member
    except Exception as e:
        Log.error(str(e))
        raise e
            

class RegisterForm(Form):
    # 사용자 등록화면에서 입력값을 검증
    r_email = TextField('Email',
                      [validators.Required('Email을 입력하세요.'),
                       validators.Length(
                                         min=5,
                                         max=40,
                                         message='5자 이상 40자 이하로 입력하세요.'),
                       validators.Email(message='이메일 형식에 맞지 않습니다.')])
    
    r_nickname = TextField('Nickname',
                         [validators.Required('화면에 표시될 닉네임을 입력하세요.'),
                          validators.Length(
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