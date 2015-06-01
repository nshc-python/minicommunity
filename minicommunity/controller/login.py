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
    next_url = form.next_url.data
    login_error = None
    
    if form.validate(): #로그인 인증의 성공할 경우 
        session.permanent = True #서버측 세션 생성 
        
        email = form.email.data
        password = form.password.data
        next_url = form.next_url.data
        
        Log.info("(%s)next_url is %s" % (request.method, next_url))
        
        try:
            member = dao.query(Member). \
            filter_by(email=email). \
            first()
        
        except Exception as e:
            Log.error(str(e))
            raise e
    
        if member:
            if not check_password_hash(member.password, password):
                login_error = "Invalid Password"
            
            else:
                session['member_info'] = member
                
                if next_url != '':
                    return redirect(next_url)
                else: 
                    return redirect(url_for('.index'))
                
                
        else:
            login_error = 'YOU do NOT exist'
            
    return render_template('login.html', next_url=next_url, error=login_error, form=form)

                
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