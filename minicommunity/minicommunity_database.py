# -*- coding: utf-8 -*-
'''
Created on 2015. 4. 13.
DB연결 및 사용을 위한 연결 모듈

@author: Soobin
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from minicommunity.minicommunity_logger import Log

class DBManager(object):
    '''
    database를 담당하는 공통 클래스
    '''
    __engine = None
    __session = None
    
    @staticmethod
    def init(db_url, db_log_flag=True):
        DBManager.__engine = create_engine(db_url, echo=db_log_flag)
        DBManager.__session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=DBManager.__engine))
        
        Log.debug("-----------------")
        Log.debug(DBManager.__session)
        Log.debug(DBManager.__engine)
        global dao
        dao = DBManager.__session
        Log.debug(str(dao))
        
    @staticmethod
    def init_db():
        from minicommunity.model import *
        from minicommunity.model import Base
        Base.metadata.create_all(bind=DBManager.__engine)

    def __init__(self, params):
        '''
        Constructor
        '''
dao = None