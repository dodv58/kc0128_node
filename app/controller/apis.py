from flask import request
from app.utils import json_response
from app import suri
from . import (
    blueprint
)

@blueprint.route('/running-status', methods=['GET'])
def get_engine_running_status():
    status = suri.running_status()
    return json_response(data={
        'status': status
    })