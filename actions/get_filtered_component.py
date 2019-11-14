from lib.icinga2 import Icinga2Action


class Icinga2GetHost(Icinga2Action):

    def run(self, object_type='Host', filters='', filter_vars=''):
        return self._client.objects.list(
            object_type,
            filters=filters,
            filter_vars=filter_vars)
