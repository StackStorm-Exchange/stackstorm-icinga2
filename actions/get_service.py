from lib.icinga2 import Icinga2Action


class Icinga2GetService(Icinga2Action):
    def run(self, service=""):
        if service == "":
            return self._client.objects.list("Service")
        return self._client.objects.list("Service", name=service)
