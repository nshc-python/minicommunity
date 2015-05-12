# -*- coding: utf-8 -*-

"""-----------------------------------------------

calls out anonymous bulletin board system 

copyright: (c) 2015 by Soobin Park and Po La Rhee 

--------------------------------------------------"""


from flask import render_template, session
from minicommunity.controller.login import login_required
from minicommunity.minicommunity_blueprint import minicommunity




@minicommunity.route('/anonybbs/list')
@login_required
def list_anonybbs(): #익명게시판 화면을 호출

    sess = session['member_info']
    if sess:
        nickname = session['member_info'].nickname  #layout에 들어갈 nickname을 세션에서 얻어옴 
    else:
        nickname = "None"

    return render_template('list_anonybbs.html', nickname=nickname)


#yes