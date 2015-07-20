# -*- coding: utf-8 -*-
'''
Created on 2015. 4. 6.

@author: Soobin
'''
from minicommunity.minicommunity_blueprint import minicommunity
from minicommunity.minicommunity_logger import Log
from minicommunity.minicommunity_database import dao
from minicommunity.model.member import Member
from minicommunity.controller.login import LoginForm
from minicommunity.controller.register_form import RegisterForm

from flask import request, url_for, jsonify
from flask.templating import render_template
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
    
    form = LoginForm(request.form)
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
            success = '회원가입이 정상처리되었습니다. 가입한 이메일로 로그인 하세요!'
            return render_template('login.html', 
                   register_success=success,
                   form=form,
                   rform=rform)
            # 성공적으로 사용자 등록이 되면 로그인 화면으로 이동한다.
#             return redirect(url_for('.login',
#                                     register_member_name=nickname,
#                                     register_success=success))
    else:
        login_error = '회원가입이 제대로 처리되지 않았습니다. 가입하기 버튼을 다시 눌러 이유를 확인하세요!'
        next_url=''
        form = LoginForm(request.form)
        
        return render_template('login.html', 
                   next_url=next_url, 
                   error=login_error,
                   form=form, 
                   rform=rform)

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