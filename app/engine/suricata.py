from .base_engine import BaseEngine
import json
import os
from app import utils

class Suricata(BaseEngine):
    config = None

    def init_app(self, app):
        # read configs from config file
        config_file = "./app/engine/suricata_centos.conf"
        with open(config_file) as c:
            self.config = json.load(c)

    def suri_path(self):
        path = self.config.get('suriPath')
        if not path:
            return False
        return os.path.exists(path)

    def suri_bin(self):
        command = self.config.get('suriBin')
        if not command:
            return False
        return_code, out, err = utils.system_execute(command.get('cmd'), command.get('params'))
        if not return_code and 'Suricata version' in out:
            return True
        else:
            return False

    def running_status(self):
        command = self.config.get('suriRunning')
        if not command:
            return False
        return_code, out, err = utils.system_execute(command.get('cmd'), command.get('params'))
        if not return_code and out.isnumeric():
            return True
        else:
            return False
