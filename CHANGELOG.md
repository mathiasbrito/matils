# Changelog

Changes to the Matils library in its releases.

## [0.1.1] - 2017-11-16
### Reversion
- The code was reverted to support Python 3.5, version 0.1 worked only 
  with Python 3.6. This decision was made because the install base of 
  Python 3.6 still low.

### Fixed
- The signature of the method register from Observer.update method, that
  was missing `self` as first argument. 

## [0.1] - 2017-11-16
### Added
- Observer Pattern in sub-package patterns
