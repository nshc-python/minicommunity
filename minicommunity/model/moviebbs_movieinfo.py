# -*- coding: utf-8 -*-
'''
Created on 2015. 4. 6.

@author: Soobin
'''

from sqlalchemy import Column, Integer, String

# from minicommunity.model.user import User

from minicommunity.model import Base


class MovieBBSMovieInfo(Base):
    __tablename__ = 'moviebbs_movieinfo'

    movieid = Column(Integer, primary_key=True) #영화 할당 아이디
    title_ko = Column(String(30)) #타이틀(한글)
    title_en = Column(String(50)) #타이틀(영어)
    genre = Column(String(20)) #장르
    publishyear = Column(Integer) #개봉연도
    poster_thumbfile = Column(String(30)) #포스터썸네일

    def __init__(self, movieid, title_ko, title_en, genre, publishyear, poster_thumbfile):
        '''
        MovieBBSMovieInfo 클래스를 초기화한다.
        '''
        self.movieid = movieid
        self.title_ko = title_ko
        self.title_en = title_en
        self.genre = genre
        self.publishyear = publishyear
        self.poster_thumbfile = poster_thumbfile
        
    def __repr__(self):
        """모델의 주요 정보를 출력한다."""        
        
        return '<MovieBBSMovieInfo %r %r %r>' % (self.movieid, self.title_ko, self.publishyear)