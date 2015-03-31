'''
Created on 2015. 4. 5.

@author: Soobin
'''

from sqlalchemy import Column, Integer, String, DateTime

# from minicommunity.model.user import User

from minicommunity.model import Base


class Member(Base):
    '''
    member_table = Table('member', metadata,
    Column('sno', Integer, nullable=False, autoincrement=True), #순번
    Column('email', String(20), primary_key=True, nullable=False), #아이디(이메일)
    Column('password', String(40)), #비밀번호 SHA1 Hash
    Column('nickname', String(20), nullable=False), #닉네임
    Column('cdatetime', DateTime, nullable=False), #생성날짜시간
    Column('adatetime', DateTime) #최근 접속날짜 시간
    )
    '''
    __tablename__ = 'member'

    sno = Column(Integer, nullable=False, autoincrement=True, primary_key=False)
    email = Column(String(20), primary_key=True, nullable=False)
    password = Column(String(40))
    nickname = Column(String(20), nullable=False)
    cdatetime = Column(DateTime, nullable=False)
    adatetime = Column(DateTime)
        


    def __init__(self, email, password, nickname, cdatetime, adatetime):
        '''
        Member 클래스를 초기화한다.
        '''
        self.email = email
        self.password = password
        self.nickname = nickname
        self.cdatetime = cdatetime
        self.adatetime = adatetime
        
    def __repr__(self):
        """모델의 주요 정보를 출력한다."""        
        
        return '<Member %r %r>' % (self.email, self.cdatetime)