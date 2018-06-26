from st2common.runners.base_action import Action
from icinga2api.client import Client


class Icinga2Action(Action):

    def __init__(self, config):
        super(Icinga2Action, self).__init__(config)
        self.api_url = config['api_url']
        self.api_user = config['api_user']
        self.api_password = config['api_password']
        self.cert = ''
        if 'cert_file' in config:
            self.cert = ['cert_file']
        self.client = Client(self.api_url, self.api_user, self.api_password)
