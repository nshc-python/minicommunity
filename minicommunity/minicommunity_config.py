# -*- coding: utf-8 -*-

'''
Created on 2015. 4. 10.

@author: Soobin
'''

class MinicommunityConfig(object):
    #클래스 선언시 각 변수별 초기값은 미리 설정
    LOG_FILE_PATH = 'resource/mylog.log'  #: Default 로그 파일 경로
    DB_FILE_PATH = 'resource/database/minicommunity.db' #: 데이터베이스 파일 경로
    DB_URL = 'sqlite:///' #: 데이터베이스 연결 URL
    DB_LOG_FLAG = 'True' #: Default SQLAlchemy trace log 설정
    SESSION_COOKIE_NAME = 'minicommunity_session' #: 쿠기에 저장되는 세션 쿠키
    UPLOAD_FOLDER = 'resource/upload/'