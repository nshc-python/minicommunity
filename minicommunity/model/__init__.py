# -*- coding: utf-8 -*-
"""
    minicommunity.model
    ~~~~~~~~~~~~~~

    minicommunity 어플리케이션에 적용될 model에 대한 패키지 초기화 모듈.

    :copyright: (c) 2015 by sbpark.
    :license: MIT LICENSE 2.0, see license for more details.
"""


from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

__all__ = ['member', 'anonybbs', 'anonybbs_delreq', 'moviebbs_movieinfo', 'moviebbs_comment']
