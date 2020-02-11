from lib.icinga2 import Icinga2Action


class Icinga2GetHost(Icinga2Action):
    def run(self, host=""):
        if host == "":
            return self._client.objects.list("Host")
        return self._client.objects.list("Host", name=host)
