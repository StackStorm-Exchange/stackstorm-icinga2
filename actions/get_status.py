from lib.icinga2 import Icinga2Action


class Icinga2GetStatus(Icinga2Action):

    def run(self, component=''):
        if component == '':
            return self._client.status.list()
        return self._client.status.list(component)
