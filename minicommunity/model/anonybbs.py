# -*- coding: utf-8 -*-
'''
Created on 2015. 4. 6.

@author: Soobin
'''

from sqlalchemy import Column, Integer, String, DateTime, Text

# from minicommunity.model.user import User

from minicommunity.model import Base


class AnonyBBS(Base): 
    __tablename__ = 'anonybbs'

    sno = Column(Integer, nullable=False, autoincrement=False, primary_key=True) #시리얼넘버
    writeremail = Column(String(20), nullable=False) #작성자 아이디(이메일)
    content = Column(Text) #내용
    picturefile = Column(String(30), nullable=True) #사진파일이름
    cdatetime = Column(DateTime, nullable=False) #생성날짜시간

    def __init__(self, sno, writeremail, content, picturefile, cdatetime):
        '''
        AnonyBBS 클래스를 초기화한다.
        '''
        self.sno = sno
        self.writeremail = writeremail
        self.content = content
        self.picturefile = picturefile
        self.cdatetime = cdatetime
        
    def __repr__(self):
        """모델의 주요 정보를 출력한다."""        
        
        return '<AnonyBBS %r %r %r %r>' % (self.writeremail, self.content, self.picturefile, self.cdatetime)
    
    def getSno(self):
        return self.sno
    
    def getContent(self):
        return self.content
    
    def getWriteremail(self):
        return self.writeremail

    def getPicturefile(self):
        return self.picturefile
    
    def getCdatetime(self):
        return self.cdatetime