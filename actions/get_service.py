from lib.icinga2 import Icinga2Action


class Icinga2GetService(Icinga2Action):

    def run(self, service):
        if service is not None:
            return self.client.objects.get('Service', service)

        return self.client.objects.list('Service')
