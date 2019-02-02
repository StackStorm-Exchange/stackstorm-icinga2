from time import sleep
import json
import requests
from icinga2api.client import Client
from st2reactor.sensor.base import Sensor
requests.packages.urllib3.disable_warnings()   # pylint: disable=no-member

try:
    import urllib3
    urllib3.disable_warnings()  # pylint: disable=no-member
except ImportError:
    pass


class Icinga2StateChangeSensor(Sensor):
    def setup(self):
        self.logger = self._sensor_service.get_logger(__name__)
        self.trigger_name = 'event.state_change'
        self.trigger_pack = 'icinga2'
        self.trigger_ref = '.'.join([self.trigger_pack, self.trigger_name])
        self.types = ['StateChange']
        self.queue = 'state_change'

        self.api_url = self._config['api_url']

        if ('api_user' in self._config and self._config['api_user'] is not None and  # noqa: W504
                self._config['api_user']):
            if 'api_password' in self._config and self._config['api_password'] is not None:
                self.api_user = self._config['api_user']
                self.api_password = self._config['api_password']
                self.client = Client(self.api_url, self.api_user, self.api_password)
                self.logger.info('Icinga2StateChangeSensor initialized with URL: %s User: %s',
                                 self.api_url, self.api_user)
            else:
                raise ValueError("Username defined with no password.")
        elif ('certificate' in self._config and self._config['certificate'] is not None
              and self._config['certificate']):  # noqa: W503
            self.certificate = self._config['certificate']
            self.key = self._config.get('key', '')
            self.ca_certificate = self._config.get('ca_certificate', '')
            self.client = Client(self.api_url, certificate=self.certificate, key=self.key,
                                 ca_certificate=self.ca_certificate)
            self.logger.info('Icinga2StateChangeSensor initialized with URL: %s Certificate: %s',
                             self.api_url, self.certificate)
        else:
            raise ValueError("Failed finding authentication method\n \
                     Please specify either username and password or certificate location")

    def run(self):
        while True:
            try:
                self.logger.info('Connecting to event stream API.')
                for event in self.client.events.subscribe(self.types, self.queue):
                    self.process_event(event)
            except Exception as ex:
                self.logger.info('Icinga2StateChangeSensor Exception %s', str(ex))

            # Wait between retries if Icinga API is disconnected
            sleep(5)

    def process_event(self, event):
        self.logger.info('Processing event: %s', event)
        payload = {}
        event = json.loads(event)
        payload['service'] = event['service']
        payload['host'] = event['host']
        payload['state'] = event['state']
        payload['state_type'] = event['state_type']
        payload['type'] = event['type']
        payload['check_result'] = event['check_result']
        self.dispatch_trigger(payload)

    def dispatch_trigger(self, payload):
        self.logger.info('Dispatching trigger: %s', self.trigger_ref)
        self._sensor_service.dispatch(self.trigger_ref, payload)

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def cleanup(self):
        pass
