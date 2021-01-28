import requests
from icinga2api.client import Client
from st2common.runners.base_action import Action

requests.packages.urllib3.disable_warnings()  # pylint: disable=no-member

try:
    import urllib3

    urllib3.disable_warnings()
except ImportError:
    pass


class Icinga2Action(Action):
    def __init__(self, config):
        super(Icinga2Action, self).__init__(config)
        self.myconfig = config
        self._client = self._get_client()

    def _get_client(self):
        api_url = self.myconfig["api_url"]
        api_user = self.myconfig.get("api_user", None)
        api_password = self.myconfig.get("api_password", None)
        certificate = self.myconfig.get("certificate", None)

        if api_user is not None and api_user:
            if api_password is not None:
                return Client(api_url, api_user, api_password)
            else:
                raise ValueError("Username defined with no password.")
        elif certificate is not None and certificate:
            key = self.myconfig.get("key", "")
            ca_certificate = self.myconfig.get("ca_certificate", "")
            return Client(
                api_url, certificate=certificate, key=key, ca_certificate=ca_certificate
            )
        else:
            raise ValueError(
                "Failed finding authentication method\n \
                     Please specify either username and password or certificate location"
            )
