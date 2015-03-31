'''
Created on 2015. 4. 6.

@author: Soobin
'''

from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime

from minicommunity.model.moviebbs_movieinfo import MovieBBSMovieInfo

from minicommunity.model import Base


class MovieBBSComment(Base):
    __tablename__ = 'moviebbs_comment'

    comment_sno = Column(Integer, primary_key=True), #영화 코멘트순번
    movieid = Column(Integer, ForeignKey(MovieBBSMovieInfo.movieid)), #영화 아이디
    writer_email = Column(String(20)), #작성자 이메일
    content = Column(Text), #코멘트 내용
    rate = Column(Integer), #별점(10점만점)
    cdatetime = Column(DateTime) #코멘트작성 날짜시간

    def __init__(self, movieid, writer_email, content, rate, cdatetime):
        '''
        MovieBBSComment 클래스를 초기화한다.
        '''
        self.movieid = movieid
        self.writer_email = writer_email
        self.content = content
        self.rate = rate
        self.cdatetime = cdatetime
        
    def __repr__(self):
        """모델의 주요 정보를 출력한다."""        
        
        return '<MovieBBSComment %r %r %r>' % (self.movieid, self.rate, self.cdatetime)