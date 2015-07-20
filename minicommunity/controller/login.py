# -*- coding: utf-8 -*-

from flask import request, render_template, session, url_for, redirect, current_app, jsonify
from werkzeug.security import check_password_hash
from minicommunity.minicommunity_logger import Log
from minicommunity.minicommunity_blueprint import minicommunity
from minicommunity.model.member import Member
from minicommunity.minicommunity_database import dao
from functools import wraps
from minicommunity.controller.register_form import RegisterForm
from minicommunity.controller.login_form import LoginForm
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
            if session.sid == session_key and session.__contains__('member_info') : is_login = True
             
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
    
    return render_template('login.html', next_url=next_url, form=form, 
                           rform=rform, regist_member=regist_member)

# 이것은 오직 테스트 멤버를 만들기 위해서만 쓰이는 함수임
@minicommunity.route('/member/ctest')
def create_members():
    # test code
    
    member_test = Member(6,
                         "test6", 
                    generate_password_hash("test6"),
                    "Pola no6",
                    datetime.today(),
                    datetime.today())
    
    dao.add(member_test)
    dao.commit()
    
    # test end
    return redirect(url_for('.login_form'))


@minicommunity.route('/member/login', methods=['post'])
def login(): #로그인 프로세싱 
    form = LoginForm(request.form) #개체.속성
    rform = RegisterForm(request.form)
    
    next_url = form.next_url.data
    login_error = None
    
    Log.debug(1)
    
    if form.validate(): #로그인 폼에 입력된 값이 유효하다고 판단될 경우
        Log.debug(2)
        session.permanent = True #세션에 영속성을 부여한다. 
        
        email = form.email.data
        password = form.password.data
        next_url = form.next_url.data
        
        Log.debug(3)
        #Log.info("(%s)next_url is %s" % (request.method, next_url))
        
        try:
            member = dao.query(Member). \
            filter_by(email=email). \
            first()
        
            Log.debug(str(4))
        
        except Exception as e:
            Log.error(str(e))
            raise e
    
        Log.debug(str(5))
        
        if member:
            Log.debug("Member passwd : "+member.password)
            Log.debug("Your   passwd : "+password)
            if not check_password_hash(member.password, password):
                login_error = "Invalid Password"
                Log.debug(str(6)+":"+login_error)
                return redirect(url_for('.login_form'))
            else:
                # 세션에 추가할 정보를 session 객체의 값으로 추가함
                # 가령, member 클래스 같은 사용자 정보를 추가하는 객체 생성하고
                # 사용자 정보를 구성하여 session 객체에 추가
                session['member_info'] = member
                
                Log.debug(str(7))
                
                if next_url != '': #다음에 이동할 주소 값이 있다면.. 그곳으로 이동한다.
                    Log.debug("8 next_url : "+next_url)
                    return redirect(next_url)     
                else:
                    Log.debug("9 go list_bbs") 
                    return render_template('list_anonybbs.html', next_url=next_url, error=login_error, form=form, rform=rform)
            
        else: #멤버가 조회되지 않았을 경우 로그인 화면으로 돌아간다.
            login_error = 'YOU do NOT exist'        
            Log.debug(str(8))
            return redirect(url_for('.login_form')) 
    else:
        Log.debug(1234567890)
        login_error = '이메일과 비밀번호를 확인해주세요.'
        return render_template('login.html',next_url=next_url, rform=rform, form=form, error=login_error)
#        return redirect(url_for('.login', form=form, error=login_error))

@minicommunity.route('/')
@login_required
def index():
    """로그인이 성공한 다음에 보여줄 초기 페이지"""
    return redirect(url_for('.login_form'))
                
@minicommunity.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('.index')) #로그인 끝나면 초기페이지로 돌아감 
  
@minicommunity.route('/member/login_check', methods=['POST'])
def login_check(): #로그인시 팝업창을 띄우기 위한 것
    email = request.json['email']
    password = request.json['password']
    
    Log.debug('email : '+email)
    Log.debug('password : '+password)
    
    #: DB에서 email 및 Password 중복 확인 
    if __get_member(email, password) :
        return jsonify(result = False)
    else:
        return jsonify(result = True)

def __get_member(email, password): #로그인 체크시 멤버 정보 가져오기 
    try:
        current_member = dao.query(Member) \
                            .filter_by(email=email, password=password) \
                            .first()
        
        Log.debug('aaaa'+current_member)
        return current_member
    except Exception as e:
        Log.error(str(e))
        raise e

             

