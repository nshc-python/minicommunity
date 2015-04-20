# -*- coding: utf-8 -*-

'''
Created on 2015. 4. 10.

@author: Soobin
'''

class MinicommunityConfig(object):
    #클래스 선언시 각 변수별 초기값은 미리 설정
    LOG_FILE_PATH = 'resource/mylog.log'
    DB_FILE_PATH = 'resource/database/minicommunity.db'
    DB_URL = 'sqlite:///'
    DB_LOG_FLAG = 'True'