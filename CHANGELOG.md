# Changelog

## Unreleased

### Changed

- Asset searches now default to the compact sparse fieldset
  `asset.name,asset.asset_type,asset.status` instead of `fields=*`. Callers that
  require every serializer attribute and relationship can pass `fields="*"` or
  `fields="all"` explicitly.
- Asset, relationship, company, viewer-pad, and viewer-line field enums make
  supported sparse fieldsets discoverable while arbitrary strings remain
  available for forward compatibility.

In a production measurement of 100 otherwise identical asset results, the
compact fieldset reduced the serialized response from 435,118 bytes to 14,056
bytes (96.8%, or approximately 31 times smaller). Actual results depend on the
selected assets and relationships.
