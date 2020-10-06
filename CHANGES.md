# Change Log

## [0.6.1] 2020-10-05

### Added
  - Added a function to escape all backslashes in the JSON object before it is loaded

### Changed
  - Adjusted the JSON load with strict=false so that control characters are allowed in the strings

## [0.6.0] 2020-05-14

### Added
  - Added changestate event timestamp to stackstorm trigger payload.

### Changed
  - Updated documentation to use pack2md .
  - Formatted code using Black.
  - Pointed icinga2api python module to nzlosh upstream for python3.7 patches.
  - Made service field optional in changestate event.

## [0.5.0]

### Added
  - Add an action to retrieve objects with filters from icinga

## [0.4.1]

### Changed
  - Style cleanup from 0.4.0. No functionality changes

## [0.4.0]

### Changed
  - Major rewrite to remove pycurl dependency. Now built on top of icinga2api library, which uses `requests()`

## [0.3.3]

### Changed
  - Minor linting

## [0.3.1]

### Changed
  - Force encoding of api\_user, api\_password, api\_url to `utf-8` to work with
    older pycurl versions

## [0.3.0]

### Changed
  - Rename `config.yaml` to `config.schema.yaml` and update to use schema.
