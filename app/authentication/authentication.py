from . import blueprint
import logging
from flask import request
from app.utils import json_response

@blueprint.route('/register', methods=['POST'])
def register():
    logging.info(request.json)
    return json_response(data={'hello'})

@blueprint.route('/login', methods=['POST'])
def login():
    pass
@blueprint.route('/logout')
def logout():
    pass
@blueprint.route('/<int:user_id>', methods=['GET'])
def user_info():
    pass