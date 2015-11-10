# -*- coding: utf-8 -*-
'''
Created on 2015. 4. 6.

@author: Soobin
'''

from sqlalchemy import Column, Integer, DateTime, String, ForeignKey

from minicommunity.model.anonybbs import AnonyBBS

from minicommunity.model import Base


class AnonyBBSDelReq(Base):
    __tablename__ = 'anonybbs_delreq' #삭제요청 

    bbssno = Column(Integer, ForeignKey(AnonyBBS.sno), primary_key='True') #게시판아이디(순번)
    memberid = Column(String(20)) #삭제요청자
    rdatetime = Column(DateTime, primary_key='True') #삭제요청날짜시간
    deletestatus = Column(String(1)) #삭제요청후삭제여부 

    def __init__(self, bbssno, memberid, rdatetime):
        '''
        AnonyBBSDelReq 클래스를 초기화한다.
        '''
        self.bbssno = bbssno
        self.memberid = memberid
        self.rdatetime = rdatetime
        self.deletestatus = 'N'
        
    def getDeleteStatus(self):
        return self.deletestatus
    
    def setDeleteStatus(self, status):
        self.deletestatus = status
        
    def __repr__(self):
        """모델의 주요 정보를 출력한다."""        
        
        return '<AnonyBBSDelReq %r %r>' % (self.bbssno, self.rdatetime)
    