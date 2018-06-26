import json
from time import sleep
import requests
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import urllib3
from st2reactor.sensor.base import Sensor

__all__ = [
    'Icinga2ReqSensor'
]


class Icinga2ReqSensor(Sensor):
    def setup(self):
        self.logger = self._sensor_service.get_logger(__name__)
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # pylint: disable=no-member
        self.r = None
        self.buffer = ''
        self.eventstream_type = self._config['eventstream_type']
        self.url = self._config['api_url']
        self.url_index = 0
        self.api_user = self._config['api_user']
        self.api_password = self._config['api_password']
        self.api_queue = self._config['api_queue']
        self.cert = ''
        if 'cert_file' in self._config:
            self.cert = self._config['cert_file']
        self.filter = {}
        if 'filter' in self._config:
            self.filter = self._config['filter']
        self.logger.info('Filter: %s', self.filter)
        self.trigger_name = 'generic_event'
        self.trigger_pack = 'icinga2req'
        self.trigger_ref = '.'.join([self.trigger_pack, self.trigger_name])
        self.logger.info('Icinga2ReqSensor initialized: %s', self._config)

    def run(self):
        self.logger.info('Setting up Icinga2 API connection')
        while True:  # Handling reconnection logic here...
            try:
                if self.eventstream_type == 'StateChange':
                    url = (self.url[self.url_index] + '/events?queue=' + self.api_queue +
                           '&types=StateChange&filter=event.state_type==1.0')
                else:
                    url = (self.url[self.url_index] + '/events?queue=' + self.api_queue +
                           '&types=CheckResult' +
                           '&filter=event.check_result.vars_after.state_type==1.0')
                self.logger.info('Icinga2ReqSensor url: %s', url)
                if not self.cert:
                    self.logger.info('Icinga2ReqSensor: insecure')
                    # Turns off SSL validation (Required for python pre-2.7.9)
                    self.r = requests.post(url,
                                           auth=HTTPBasicAuth(self.api_user, self.api_password),
                                           stream=True, timeout=60, verify=False,
                                           hooks=dict(response=self.on_receive),
                                           headers={'Accept': 'application/json'})
                else:
                    self.logger.info('Icinga2ReqSensor: secure')
                    # We have a cert, much more secure
                    self.r = requests.post(url,
                                           auth=HTTPBasicAuth(self.api_user, self.api_password),
                                           stream=True, timeout=60, verify=self.cert,
                                           hooks=dict(response=self.on_receive),
                                           headers={'Accept': 'application/json'})
                self.logger.info('Icinga2ReqSensor status_code: %s', self.r.status_code)
            except Exception as ex:
                self.logger.info('Icinga2ReqSensor Exception %s', str(ex))
            sleep(2)
            self.url_index += 1
            if self.url_index >= len(self.url):
                self.url_index = 0

    def cleanup(self):
        if self.r:
            self.r.connection.close()

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def on_receive(self, r, *args, **kwargs):
        for line in r.iter_lines():
            linebuf = self.buffer + line
            self.buffer = ''
            linebuf = linebuf.replace('\n', '')
            try:
                event = json.loads(linebuf)
                self.dispatch_trigger(event)
            except Exception:
                self.buffer = linebuf

    def dispatch_trigger(self, event):
        # self.logger.info('Processing event: %s', event)
        ack = False
        address = ""
        address6 = ""
        var = {}
        if 'service' not in event:
            event['service'] = 'hostcheck'
        else:
            ack, address, address6, var = self.get_extra_info(event['host'], event['service'])
        payload = {}
        payload['service'] = event['service']
        payload['host'] = event['host']
        payload['access'] = {"address": address, "address6": address6}
        payload['monitoring_source'] = 'icinga2'
        payload['output'] = event['check_result']['output']
        payload['timestamp'] = event['timestamp']
        payload['state'] = event['state']
        if self.eventstream_type == 'CheckResult':
            payload['state'] = event['check_result']['state']

        # var is the place to put all the check specific stuff & misc stuff
        payload['var'] = {}
        payload['var']['ack'] = ack

        # Situationally specific in var
        # if 'stack' in var:
        #   payload['var']['stack'] = var['stack']
        # if 'severity' in var:
        #   payload['var']['severity'] = var['severity']
        # hardware check (fix later with hardware custom icinga2 var)
        if event['service'].lower().find("idrac") or event['service'].lower().find("ilo"):
            payload['var']['hardware'] = True
        # for key in var.keys():
        #   if key.find("idrac") or key.find("ilo"):
        #         payload['var'][key] = var[key]
        #         payload['var']['hardware'] = True
        for key, val in var.iteritems():
            payload['var'][key] = val
            if key.lower().find("idrac") or key.lower().find("ilo"):
                payload['var']['hardware'] = True

        if self.sfilter(payload):
            self.logger.info('Filtered event: %s', payload['service'])
            return
        self.logger.info('Dispatching event: %s', payload)
        self._sensor_service.dispatch(self.trigger_ref, payload)

    def get_extra_info(self, host, service):
        hostservice = host + "!" + service
        hostservice.replace(" ", "%20")
        # This join is the nasty thing that grabs all that extra event information, esp the custom
        # vars. Modify it based on need
        data = {
            "joins": ["host.name", "host.address", "host.address6", "host.vars"],
            "attrs": ["acknowledgement"]
            }
        text = ""
        ack = False
        j = {}
        url_index = 0
        while True:
            url = self.url[url_index] + '/objects/services?service=' + hostservice
            ok = False
            ok, text = self.call_api(url, data)
            if ok:
                break
            # ok, retry once more....
            sleep(5)
            ok, text = self.call_api(url, data)
            if ok:
                break
            # ok, tried twice, try the next url, else treat as a failure and return blank
            url_index += 1
            if url_index >= len(self.url):
                return 0.0, "", "", {}
        # and.., we probably have a good return result..
        try:
            j = json.loads(text)
        except ValueError:
            return 0.0, "", "", {}
        if j['results'][0]['attrs']['acknowledgement'] == 1.0:
            ack = True
        return (ack, j['results'][0]['joins']['host']['address'],
                j['results'][0]['joins']['host']['address6'],
                j['results'][0]['joins']['host']['vars'])

    def call_api(self, url, data):
        try:
            if not self.cert:
                # Pre python 2.7.9. Turns off SSL validation
                self.rapi = requests.post(url, auth=HTTPBasicAuth(self.api_user, self.api_password),
                                          stream=True, data=data, timeout=30, verify=False,
                                          headers={'Accept': 'application/json',
                                                   'X-HTTP-Method-Override': 'GET'})
            else:
                # We have a cert, much more secure
                self.rapi = requests.post(url, auth=HTTPBasicAuth(self.api_user, self.api_password),
                                          stream=True, data=data, timeout=30, verify=self.cert,
                                          headers={'Accept': 'application/json',
                                                   'X-HTTP-Method-Override': 'GET'})
        except Exception:
            return False, ""
        return self.rapi.ok, self.rapi.text

    def sfilter(self, payload):
        for f in self.filter:
            key = self.filter[f]['key']
            pattern = self.filter[f]['pattern']
            atype = self.filter[f]['type']
            # For exists and nexists, there's no need to check in other than var,
            # because all of the base payload keys always exist
            if atype == 'exists':
                if key in payload['var']:
                    return True
            if atype == 'nexists':
                if key not in payload['var']:
                    return True
            if key in payload:
                if atype == 'equals':
                    if payload[key] == pattern:
                        return True
                if atype == 'nequals':
                    if payload[key] != pattern:
                        return True
                if atype == 'contains':
                    if payload[key].find(pattern):
                        return True
                if atype == 'ncontains':
                    if not payload[key].find(pattern):
                        return True
            elif key in payload['var']:
                if atype == 'equals':
                    if payload['var'][key] == pattern:
                        return True
                if atype == 'nequals':
                    if payload['var'][key] != pattern:
                        return True
                if atype == 'contains':
                    if payload['var'][key].find(pattern):
                        return True
                if atype == 'ncontains':
                    if not payload['var'][key].find(pattern):
                        return True
        return False
