# Change Log

# 0.5.1

- Add a variable in the payload sensor to easily differenciate host and service type for a state change

# 0.5.0

- Add an action to retrieve objects with filters from icinga

# 0.4.1

- Style cleanup from 0.4.0. No functionality changes

# 0.4.0

- Major rewrite to remove pycurl dependency. Now built on top of icinga2api library, which uses `requests()`

# 0.3.3

- Minor linting

# 0.3.1

- Force encoding of api\_user, api\_password, api\_url to `utf-8` to work with
  older pycurl versions

# 0.3.0

- Rename `config.yaml` to `config.schema.yaml` and update to use schema.
