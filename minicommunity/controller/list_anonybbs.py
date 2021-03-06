# -*- coding: utf-8 -*-

"""-----------------------------------------------

calls out anonymous bulletin board system 

copyright: (c) 2015 by Soobin Park and Po La Rhee 

--------------------------------------------------"""

from flask import render_template, session, request, url_for, jsonify, current_app, send_from_directory
from werkzeug import redirect, secure_filename
from minicommunity.controller.login import login_required
from minicommunity.minicommunity_blueprint import minicommunity
from minicommunity.minicommunity_logger import Log
from wtforms import Form, TextField, validators
from datetime import datetime
from minicommunity.model.anonybbs import AnonyBBS
from minicommunity.model.anonybbs_delreq import AnonyBBSDelReq
from minicommunity.minicommunity_database import dao
from sqlalchemy import func, text
from sqlalchemy.sql.elements import Null
import os


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

        # Get the name of the uploaded file
        picturefile = request.files['myPhoto']
        Log.debug('pictureupload1')  
        # Check if the file is one of the allowed types/extensions
        if picturefile and __allowed_file(picturefile.filename): 
            #안전한 이름으로 바꾸기 
            securePicturefile = secure_filename(picturefile.filename)
            Log.debug('pictureupload2')
            picturefile.save(os.path.join(current_app.config['UPLOAD_FOLDER'], securePicturefile)) 
        else: 
            None
        # anonybbs table에서 sno값의 최대값을 구한다음, 구한 값에서 1을 더한 뒤, 그 값을 snocount로 지정하여, write할 때 활용한다.
                       

        try : #DB에 저장 #anonybbs=0은 임시 
            temp = dao.query(func.max(AnonyBBS.sno)).first()
            if temp[0] == None:
                snocount = 1
            else:
                snocount = int(temp[0]) + 1;
            Log.debug("snocount : "+str(snocount));
            BBSdata = AnonyBBS(snocount, writeremail, content, securePicturefile, written_date) #BBS의 약자는 bulletin board system 
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

@minicommunity.route('/anonybbs/uploads/<picturename>')
def uploaded_file(picturename):
    Log.debug('pictureupload3')
    return send_from_directory(current_app.config['UPLOAD_FOLDER'],
                               picturename)

#삭제요청하면 DB에 저장 
@minicommunity.route('/anonybbs/delreq', methods=['post']) 
@login_required 
def requestDeletes():
    bbsno = request.json['bbsno']
    memberid = session['member_info'].email
    rdatetime = datetime.today() #삭제요청한날짜
    s_or_f = 'fail'
    
    try:
        delreq = AnonyBBSDelReq(bbsno, memberid, rdatetime)
        dao.add(delreq)
        dao.commit()
        s_or_f = 'success'
    except Exception as e:
        dao.rollback()
        Log.error("Upload DB error : " + str(e))
        raise e
    
    
    #return redirect(url_for('.list_anonybbs'))
    if s_or_f == 'success':
        return jsonify(result = True)
    else:
        return jsonify(result = False)

@minicommunity.route('/anonybbs/showdelreq') 
@login_required  
def showDelreq(): #삭제 요청한 아이들을 보여준다. 
    
    admindata = session['adminyn']
    Log.debug('admindata' + admindata)
    #dao.query()
    '''
    select REQ.bbssno, count(REQ.bbssno), ORIGIN.content
    from anonybbs_delreq REQ, anonybbs ORIGIN
    where REQ.bbssno = ORIGIN.sno
    group by REQ.bbssno
    order by count(REQ.bbssno)
    desc
    '''

    #delreqData = dao.query(AnonyBBSDelReq).order_by(AnonyBBSDelReq.cdatetime.desc()).all() 
    queryStatement = text(
                          "select REQ.bbssno SNODATA, count(REQ.bbssno) SNOCOUNT, REQ.deletestatus DELETESTATUS"
                          +" from anonybbs_delreq REQ"
                          +" group by REQ.bbssno"
                          +" order by REQ.deletestatus, count(REQ.bbssno) "
                          +" desc"
                          )
    delreqData = dao.execute(queryStatement).fetchall()
    
    return render_template('requesteddeletes.html', 
                           adminyn=admindata, 
                           delreqList=delreqData)
    #return jsonify(adminyn = admindata)

@minicommunity.route('/anonybbs/deletePosting/<snodata>') 
@login_required  
def deleteDelreq(snodata): #선택된게시글db에서삭제 
    
    try:
        Log.debug('0error        ')
        selectedReq = dao.query(AnonyBBS).filter(AnonyBBS.sno == snodata).first()
        dao.delete(selectedReq)
        dao.commit()
        Log.debug('1error')
        
         
        want2UpdateData = dao.query(AnonyBBSDelReq).filter(AnonyBBSDelReq.bbssno == snodata)
        for data in want2UpdateData:
            data.setDeleteStatus('Y')
        dao.commit()
        Log.debug('2error')
        
        
    except Exception as e:
        dao.rollback()
        Log.error("DeleteBBS error : " + str(e))
        raise e
    
    return redirect(url_for('.showDelreq'))

@login_required
def searchData(searchtext, datefrom, dateto): #게시글을 검색한다
    
    searchContent = " select cdatetime CDATETIME, content CONTENT"
    searchContent += " from anonybbs"
    searchContent += " where 1=1 "
    
    if datefrom is not Null:
        searchContent += " and cdatetime >= '" + datefrom + "'"
    
    if dateto is not Null:
        searchContent += " and cdatetime <= '" + dateto + "'"
    
    if searchtext is not Null:
        searchContent += " and content like '%" + searchtext + "%'"
        
    searchContent += " order by cdatetime "
    searchContent += " desc"
                          
    queryStatement = text(searchContent)    
    searchedData = dao.execute(queryStatement).fetchall()
    
    return render_template('list_anonybbs.html', 
                       searchedData=searchedData)
    

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