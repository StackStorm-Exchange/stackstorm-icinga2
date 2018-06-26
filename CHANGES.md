# Change Log

## 0.4.0

- Rewrite to remove pycurl, use icinga2api library
- Incorporate Requests-based sensor from https://github.com/twalk6/icinga2req
- Note: actions, parameters, results and triggers have all changed. You will need to update workflows

## 0.3.3

- Minor linting

## 0.3.1

- Force encoding of api\_user, api\_password, api\_url to `utf-8` to work with
  older pycurl versions

## 0.3.0

- Rename `config.yaml` to `config.schema.yaml` and update to use schema.
