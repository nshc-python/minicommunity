'''
Created on 2015. 4. 6.

@author: Soobin
'''

from sqlalchemy import Column, Integer, DateTime, Text, ForeignKey

from minicommunity.model.anonybbs import AnonyBBS

from minicommunity.model import Base


class AnonyBBSDelReq(Base):
    __tablename__ = 'anonybbs_delreq'

    bbssno = Column(Integer, ForeignKey(AnonyBBS.sno)), #게시판아이디(순번)
    reason = Column(Text), #삭제요청사유
    rdatetime = Column(DateTime) #삭제요청날짜시간

    def __init__(self, bbssno, reason, rdatetime):
        '''
        AnonyBBSDelReq 클래스를 초기화한다.
        '''
        self.bbssno = bbssno
        self.reason = reason
        self.rdatetime = rdatetime
        
    def __repr__(self):
        """모델의 주요 정보를 출력한다."""        
        
        return '<AnonyBBSDelReq %r %r>' % (self.bbssno, self.rdatetime)