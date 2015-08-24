# -*- coding: utf-8 -*-

"""-----------------------------------------------

calls out anonymous bulletin board system 

copyright: (c) 2015 by Soobin Park and Po La Rhee 

--------------------------------------------------"""

from flask import render_template, session, request, url_for #current_app
from werkzeug import redirect
from minicommunity.controller.login import login_required
from minicommunity.minicommunity_blueprint import minicommunity
from minicommunity.minicommunity_logger import Log
from wtforms import Form, TextField, validators
from datetime import datetime
from minicommunity.model.anonybbs import AnonyBBS
from minicommunity.minicommunity_database import dao
from sqlalchemy import func


@minicommunity.route('/anonybbs/list')
@login_required
def list_anonybbs(): #익명게시판 화면을 호출

    form = ContentForm(request.form)
    sess = session['member_info']
    if sess:
        nickname = session['member_info'].nickname  #layout에 들어갈 nickname을 세션에서 얻어옴 
        Log.info("nickname : "+nickname);
        Log.debug('anony1')
        
        selectedData = dao.query(AnonyBBS).order_by(AnonyBBS.cdatetime.desc()).all()
        Log.debug("********************************");
        Log.debug(selectedData)
        

 
            
    else:
        nickname = "None"
        Log.info("sess is none!");

    return render_template('list_anonybbs.html', 
                           form=form, 
                           nickname=nickname, 
                           anonylist=selectedData)


#사진을 올릴 때 어떤 확장자를 처리할 것인지 정의 
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png', 'gif', 'pdf'])
def __allowed_file(picturefile):
    
    return '.' in picturefile and \
        picturefile.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@minicommunity.route('/anonybbs/write', methods=['post'])
@login_required
def write_content(): #게시글을 DB에 저장하기
    Log.debug('anonywrite1')
    form = ContentForm(request.form)

    # HTTP POST로 요청이 오면 사용자 정보를 등록
    if form.validate(): #만일 폼이 있으면~~ 
        #: Session에 저장된 사용자 정보를 셋팅
        writeremail = session['member_info'].email
        
        # Form으로 넘어온 변수들의 값을 셋팅함
        content = form.content.data
        written_date = datetime.today()
        picturefile = ''
        # anonybbs table에서 sno값의 최대값을 구한다음, 구한 값에서 1을 더한 뒤, 그 값을 snocount로 지정하여, write할 때 활용한다.
        
        
    #아직 사진은 아무것도 없으므로 사진의 위치는 제외하고, 글을 담을 위치만 저장한다.
                       

        try : #DB에 저장 #anonybbs=0은 임시 
            temp = dao.query(func.max(AnonyBBS.sno)).first()
            snocount = int(temp[0]) + 1;
            Log.debug("snocount : "+str(snocount));
            BBSdata = AnonyBBS(snocount, writeremail, content, picturefile, written_date) #BBS의 약자는 bulletin board system 
            dao.add(BBSdata)
            dao.commit()
            
        except Exception as e:
            dao.rollback()
            Log.error("Upload DB error : " + str(e))
            raise e
    
#         return render_template('list_anonybbs.html', form=form, anonybbs1=BBSdata)
        return redirect(url_for('.list_anonybbs'))

    else:
#         return render_template('list_anonybbs.html', form=form)
        return redirect(url_for('.list_anonybbs'))
    

class ContentForm(Form):
    content = \
        TextField('content',[validators.Required('글을 입력하지 않으셨습니다.'),
                             validators.Length(
                                min=3,
                                max=1000,
                                message='글을 10자 이상 입력해주세요')])

# def content_info(): #db에서 게시판 정보를 다운로드 
#     content = dao.query(BBSdata).first()
#     return (BBSdata.content, BBSdata.written_date, BBSdata.picturefile)
# 
# @minicommunity.route('/anonybbs/list/', defaults={'page': 1})
# @minicommunity.route('/anonybbs/list/page/<int:page>')
# @login_required
# def show_all(page=1):
#     
#     per_page = current_app.config['PER_PAGE']
#     content_count = dao.query(BBSdata).count() #daoquery  BBSdata가 아니면 뭘가져와야하는가?
#     pagination = Pagination(page, per_page, content_count)
#     
#     if page != 1: #만약 페이지가 1이 아니라
#         offset = per_page * (page - 1)
#     else:
#         offset = 0 #페이지가 1일때 
#     
#     BBS_pages = dao.query(BBSdata). \
#                     order_by(BBSdata.written_date.desc()).limit(per_page).offset(offset).all()
#     
#     return render_template('list_anonybbs.html', pagination=pagination)
# 
# from math import ceil
# 
# class Pagination(object):
#     
#     def __init__(self, page, per_page, total_count):
#         self.page = page
#         self.per_page = per_page
#         self.total_count = total_count
#     
#     @property
#     def pagees(self):
#         return int(ceil(self.total_count / float(self.per_page)))
#     
#     @property
#     def has_prev(self):
#         return self.page>1
#     
#     @property
#     def has_next(self):
#         return self.page < self.pages
#     
# #     def iter_pages(self): #connects to _pagehelpers.html
# #         