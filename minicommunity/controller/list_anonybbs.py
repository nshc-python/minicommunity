# -*- coding: utf-8 -*-

"""-----------------------------------------------

calls out anonymous bulletin board system 

copyright: (c) 2015 by Soobin Park and Po La Rhee 

--------------------------------------------------"""


from flask import render_template, session, request
from minicommunity.controller.login import login_required
from minicommunity.minicommunity_blueprint import minicommunity
from minicommunity.minicommunity_logger import Log
from wtforms import Form, TextField, validators
from datetime import datetime
from minicommunity.model.anonybbs import AnonyBBS
from minicommunity.minicommunity_database import dao



@minicommunity.route('/anonybbs/list')
@login_required
def list_anonybbs(): #익명게시판 화면을 호출

    form = ContentForm(request.form)
    sess = session['member_info']
    if sess:
        nickname = session['member_info'].nickname  #layout에 들어갈 nickname을 세션에서 얻어옴 
        Log.info("nickname : "+nickname);
        Log.debug('anony1')
    else:
        nickname = "None"
        Log.info("sess is none!");

    return render_template('list_anonybbs.html', form=form, nickname=nickname)

@minicommunity.route('/anonybbs/write', methods=['post'])
@login_required
def write_content(): #게시글을 DB에 저장하기
    Log.debug('anony2')
    form = ContentForm(request.form)

    # HTTP POST로 요청이 오면 사용자 정보를 등록
    if form.validate():
        #: Session에 저장된 사용자 정보를 셋팅
        writeremail = session['user_info'].email
        
        # Form으로 넘어온 변수들의 값을 셋팅함
        content = form.content.data
        written_date = datetime.today()
        picturefile = ''
#         upload_photo = request.files['picturefile']
#         filename = None
#         filesize = 0
#         filename_orig = upload_photo.filename

        try : #DB에 저장 #anonybbs=0은 임시 
            BBSdata = AnonyBBS(0, writeremail, content, written_date, picturefile) #BBS의 약자는 bulletin board system 
            dao.add(BBSdata)
            dao.commit()
            
        except Exception as e:
            dao.rollback()
            Log.error("Upload DB error : " + str(e))
            raise e
    
        return render_template('list_anonybbs.html', form=form)

    else:
        return render_template('list_anonybbs.html', form=form)

# def upload_photo
        
class ContentForm(Form):
    content = \
        TextField('content',[validators.Required('비밀번호를 입력하지 않으셨습니다.'),
                             validators.Length(
                                min=10,
                                max=1000,
                                message='글을 10자 이상 입력해주세요')])