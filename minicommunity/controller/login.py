# -*- coding: utf-8 -*-

from flask import request, render_template, session, url_for, redirect, current_app
from werkzeug.security import check_password_hash
from wtforms import Form, TextField, validators
from minicommunity.minicommunity_logger import Log
from minicommunity.minicommunity_blueprint import minicommunity
from minicommunity.model.member import Member
from minicommunity.minicommunity_database import dao
from functools import wraps
from wtforms.fields.simple import HiddenField, PasswordField
from minicommunity.controller.register_member import RegisterForm
#test import#
from datetime import datetime
from werkzeug import generate_password_hash

   
   
def login_required(f):
     
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try: 
            session_key = \
                request.cookies.get(current_app.config['SESSION_COOKIE_NAME'])
             
            is_login = False
            if session.sid == session_key and session.__contains__('user_info') : is_login = True
             
            if not is_login:
                return redirect(url_for('.login_form', next=request.url))
             
            return f(*args, **kwargs)
         
        except Exception as e:
            Log.error("Minicommunity error occurs : %s" % str(e))
            raise e
         
    return decorated_function
    


@minicommunity.route('/member/login')
def login_form(): #로그인 화면을 호출 
    
    next_url = request.args.get('next','')
    regist_member = request.args.get('regist_member','') #welcome user message popup 
    Log.info("(%s)next_url is %s" % (request.method, next_url))
    form = LoginForm(request.form)
    rform = RegisterForm(request.form)
    
    return render_template('login.html', next_url=next_url, form=form, rform=rform, regist_member=regist_member)

@minicommunity.route('/member/login', methods=['post'])
def login(): #로그인 프로세싱 
    form = LoginForm(request.form) #개체.속성
    rform = RegisterForm(request.form)
    
    next_url = form.next_url.data
    login_error = None
    
    if form.validate(): #로그인 인증의 성공할 경우 
        #session.permanent = True #서버측 세션 생성 
        
        email = form.email.data
        password = form.password.data
        next_url = form.next_url.data
        
        Log.debug(1)
        #Log.info("(%s)next_url is %s" % (request.method, next_url))
        
        # test code
        '''
        member_test = Member(1,
                             "test1", 
                        generate_password_hash("test1"),
                        "nickname1",
                        datetime.today(),
                        datetime.today())
        
        dao.add(member_test)
        dao.commit()
        '''
        # test end
        
        try:
            member = dao.query(Member). \
            filter_by(email=email). \
            first()
        
            Log.debug(str(1))
        
        except Exception as e:
            Log.error(str(e))
            raise e
    
        Log.debug(str(2))
        
        if member:
            if not check_password_hash(member.password, password):
                login_error = "Invalid Password"
         
                Log.debug(str(3))
        
            else:
                # 세션에 추가할 정보를 session 객체의 값으로 추가함
                # 가령, member 클래스 같은 사용자 정보를 추가하는 객체 생성하고
                # 사용자 정보를 구성하여 session 객체에 추가
                session['member_info'] = member
                
                Log.debug(str(4))
                
                if next_url != '':
                    return redirect(next_url)
                
                    Log.debug(str(5))
                
                else: 
                    return redirect(url_for('.index'))
            
            Log.debug(str(6))   
                
        else:
            login_error = 'YOU do NOT exist'        
            Log.debug(str(7))
            
    return render_template('list_anonybbs.html', next_url=next_url, error=login_error, form=form, rform=rform)
    
    Log.debug(str(8))
                
@minicommunity.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('.index')) #로그인 끝나면 초기페이지로 돌아감 
    
    
           

class LoginForm(Form): #로그인에 필요한 정보를 규정 
    email = \
        TextField('email',[
                validators.Required('이메일을 입력해주세요'),
                validators.Length(min=5,max=40,message='이메일 제대로 써주세요'),
                validators.Regexp(r'[A-Za-z0-9@-_.]', message='이메일 제대로 써주세요')])

    password = \
        PasswordField('password',[
                validators.Required('비밀번호를 입력해주세요'),
                validators.Length(min=6, max=20, message='비밀번호를 입력해주셈'),
                validators.Regexp(r'[A-Za-z0-9]', message='비밀번호를 입력해주셈')])
    
    next_url = HiddenField('next_url')