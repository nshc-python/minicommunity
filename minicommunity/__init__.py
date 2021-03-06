# -*- coding: utf-8 -*-

import os
from flask import Flask

def create_app(config_filepath='resource/config.cfg'):
    minicommunity_app = Flask(__name__)

    # 기본 설정은 MinicommunityConfig 객체에 정의되있고 운영 환경 또는 기본 설정을 변경을 하려면
    # 실행 환경변수인 MINICOMMUNITY_SETTINGS에 변경할 설정을 담고 있는 파일 경로를 설정 
    from minicommunity.minicommunity_config import MinicommunityConfig
    minicommunity_app.config.from_object(MinicommunityConfig)
    minicommunity_app.config.from_pyfile(config_filepath, silent=True)
#     print_settings(photolog_app.config.iteritems())
        
    # 로그 초기화
    from minicommunity.minicommunity_logger import Log
    log_filepath = os.path.join(minicommunity_app.root_path, 
                                minicommunity_app.config['LOG_FILE_PATH'])
    Log.init(log_filepath=log_filepath)
    
    # 데이터베이스 처리 
    from minicommunity.minicommunity_database import DBManager
    from minicommunity.minicommunity_database import dao
    db_filepath = os.path.join(minicommunity_app.root_path, minicommunity_app.config['DB_FILE_PATH'])
    db_url = minicommunity_app.config['DB_URL'] + db_filepath
    DBManager.init(db_url, eval(minicommunity_app.config['DB_LOG_FLAG']))
    DBManager.init_db()
    Log.debug("DAO::::")
    Log.debug(str(dao))
       
    # 뷰 함수 모듈은 어플리케이션 객체 생성하고 블루프린트 등록전에 
    # 뷰 함수가 있는 모듈을 임포트해야 해당 뷰 함수들을 인식할 수 있음
    from minicommunity.controller import *
    
    from minicommunity.minicommunity_blueprint import minicommunity
    minicommunity_app.register_blueprint(minicommunity)
    
    # SessionInterface 설정.
    # Redis를 이용한 세션 구현은 cache_session.RedisCacheSessionInterface 임포트하고
    # app.session_interface에 RedisCacheSessionInterface를 할당
    from minicommunity.minicommunity_cache_session import SimpleCacheSessionInterface
    minicommunity_app.session_interface = SimpleCacheSessionInterface()
    
    # 공통으로 적용할 HTTP 404과 500 에러 핸들러를 설정
#     photolog_app.error_handler_spec[None][404] = not_found
#     photolog_app.error_handler_spec[None][500] = server_error
    
    # 페이징 처리를 위한 템플릿 함수
#     photolog_app.jinja_env.globals['url_for_other_page'] = \
#         url_for_other_page
    
    return minicommunity_app

