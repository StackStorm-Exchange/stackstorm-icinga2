from lib.icinga2 import Icinga2Action


class Icinga2GetStatus(Icinga2Action):

    def run(self, component=None):
        if component:
            return self.client.status.list(component)

        return self.client.status.list()
