# icinga2 integration pack v0.5.0

> Icinga2 Monitoring
Igor Cherkaev <emptywee@protonmail.ch>

### Contributors
- Lindsay Hill <lindsay@stackstorm.com>


## Description

Icinga2 version 2.4.0 introduced an API, making it possible to subscribe to Icinga2. So far only `StateChange` event type is supported. Read http://docs.icinga.org/icinga2/latest/doc/module/icinga2/toc#!/icinga2/latest/doc/module/icinga2/chapter/icinga2-api#icinga2-api for more information on Icinga2 API. 

**NOTE**: This pack has had a major overhaul as of version 0.4.0. Some options have changed, and the sensor has been rewritten. This may break existing workflows. Note the sensor now uses the same username/password as actions. You can also use certificates for authentication.


## Configuration

The following options are required to be configured for the pack to work correctly.

| Option | Type | Required | Secret | Description |
|---|---|---|---|---|
| `api_url` | string | True | False | URL to the API stream, e.g. 'https://localhost:5665/v1' |
| `api_user` | string | False | False | API user name to query Icinga2 host for objects |
| `api_password` | string | False | True | API password for querying Icinga2 for objects |
| `certificate` | string | False | False | Path to client certificate if using certificate authentication instead of username/password |
| `key` | string | False | False | Path to client private key if using certificate authentication instead of username/password |
| `ca_file` | string | False | False | Optional path to CA bundle for validating server-side certificate |


You can also use dynamic values from the datastore. See the [docs](https://docs.stackstorm.com/reference/pack_configs.html) for more info.

## Actions


The pack provides the following actions:

### get_filtered_component
_Get all Icinga2 hosts or services objects, filtered_

| Parameter | Type | Required | Secret | Description |
|---|---|---|---|---|
| `object_type` | string | False | default | _Type of object._ |
| `filters` | string | False | default | _Filters matched object(s)._ |
| `filter_vars` | object | False | default | _Variables used in the filters expression._ |
### get_status
_Get Icinga2 status_

| Parameter | Type | Required | Secret | Description |
|---|---|---|---|---|
| `component` | string | False | default | _Specific component to get status for. If not specified, complete status is returned._ |
### get_service
_Get Icinga2 service object_

| Parameter | Type | Required | Secret | Description |
|---|---|---|---|---|
| `service` | string | False | default | _Specific service object to return. If not specified, all services are returned._ |
### get_host
_Get all Icinga2 host objects, or individual host_

| Parameter | Type | Required | Secret | Description |
|---|---|---|---|---|
| `host` | string | False | default | _Specific host object to return. If not specified, all hosts are returned._ |



## Sensors

The following sensors and triggers are provided:

### Class Icinga2StateChangeSensor
_Sensor for Icinga2 StateChange events._

| Trigger Name | Description |
|---|---|
| `event.state_change` | _Icinga2 State Change event._ |





## Sensor payload

As of now, sensor is configured to catch only `StateChange` events from Icinga2 host. Typical event of such would consist of:

```
{
  "check_result": {
    "active": true,
    "check_source": "hostname01",
    "command": [
      "/usr/lib64/nagios/plugins/check_disk",
      "-c",
      "10%",
      "-w",
      "20%",
      "-K",
      "10%",
      "-W",
      "20%",
      "-X",
      "none",
      "-X",
      "tmpfs",
      "-X",
      "sysfs",
      "-X",
      "proc",
      "-X",
      "devtmpfs",
      "-X",
      "devfs",
      "-X",
      "mtmfs",
      "-m"
    ],
    "execution_end": 1458668863.9526860714,
    "execution_start": 1458668863.9508030415,
    "exit_status": 0.0,
    "output": "DISK OK - free space: / 3064 MB (54% inode=84%); /boot 78 MB (42% inode=99%); /home 1845 MB (99% inode=99%); /opt 18002 MB (99% inode=99%); /tmp 1846 MB (99% inode=99%); /var 3417 MB (89% inode=98%); /var/log 2089 MB (56% inode=99%);",
    "performance_data": [
      "/=2547MB;4735;5327;0;5919",
      "/boot=105MB;154;173;0;193",
      "/home=3MB;1560;1755;0;1951",
      "/opt=111MB;15268;17177;0;19086",
      "/tmp=3MB;1560;1755;0;1951",
      "/var=409MB;3224;3627;0;4031",
      "/var/log=1609MB;3122;3512;0;3903"
    ],
    "schedule_end": 1458668863.9528689384,
    "schedule_start": 1458668863.9528689384,
    "state": 0.0,
    "type": "CheckResult",
    "vars_after": {
      "attempt": 1.0,
      "reachable": true,
      "state": 0.0,
      "state_type": 0.0
    },
    "vars_before": {
      "attempt": 2.0,
      "reachable": true,
      "state": 1.0,
      "state_type": 0.0
    }
  },
  "host": "hostname01",
  "service": "disk",
  "state": 0.0,
  "state_type": 0.0,
  "timestamp": 1458668870.328537941,
  "type": "StateChange"
}
```

Currently, sensor takes the `host`, `service`, `state`, `state_type`, `type` and `check_result` variables and passes it as a payload to the trigger. All that data can be used in the rule and passed to actions as well.




<sub>Documentation generated using [pack2md](https://github.com/nzlosh/pack2md)</sub>