from flask import Flask
import os, orjson, logging, signal
from logging.config import dictConfig
from .config import app_config
import yaml
from .utils import build_config_from_env
from app import engine

DEFAULT_CONFIG_NAME = os.getenv('ENV', 'production')
_engine = None

def handle_sigterm(signum, frame):
    if _engine:
        _engine.disconnect()
    logging.info('Gracefully exit')
    logging.info('System exit')
    raise SystemExit

def create_app(config_name=DEFAULT_CONFIG_NAME):
    global _engine
    app = Flask(__name__, instance_relative_config=True)

    # ensure the logs folder exists
    os.makedirs('./logs', exist_ok=True)

    # load common & default config values
    app.config.from_object(app_config[config_name])
    with open('%s/config.yml' % app.root_path) as fp:
        app.config.from_mapping(yaml.load(fp, Loader=yaml.FullLoader))

    # Override configs by ENV variables
    app.config.from_mapping(build_config_from_env(app))

    from . import authentication
    authentication.init_app(app)

    # init logging
    dictConfig(app.config.get('LOGGING'))

    # init engine
    _engine = engine.init_engine(app)

    # init controller
    from . import controller
    controller.init_app(app)

    # /ping
    @app.route('/healthz')
    def ping():
        return app.response_class(
            orjson.dumps({'message': 'ok'}),
            mimetype=app.config['JSONIFY_MIMETYPE'],
        ), 200

    signal.signal(signal.SIGINT, handle_sigterm)
    signal.signal(signal.SIGTERM, handle_sigterm)

    return app