# -*- coding: utf-8 -*-
"""
    minicommunity.blueprint
    ~~~~~~~~~~~~~~~~~~

    minicommunity 어플리케이션에 적용할 blueprint 모듈.

"""


from flask import Blueprint
from minicommunity.minicommunity_logger import Log

minicommunity = Blueprint('minicommunity', __name__,
                     template_folder='../templates', static_folder='../static')

Log.info('static folder : %s' % minicommunity.static_folder)
Log.info('template folder : %s' % minicommunity.template_folder)
