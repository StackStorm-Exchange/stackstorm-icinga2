from lib.icinga2 import Icinga2Action


class Icinga2GetHost(Icinga2Action):

    def run(self, host):
        if host is not None:
            return self.client.objects.get('Host', host)

        return self.client.objects.list('Host')
