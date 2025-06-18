# Release Notes

## UNRELEASED

## 0.1.11

- Fixed bugs in `__post_init__()` for `Item` class; added tests. 

## 0.1.10

- Forgot to remove some dependencies.

## 0.1.9

- Added code to util for f1, precision, and recall.
- Added tests for the above and gleu. 

## 0.1.8

- Implemented fallback for Python < 3.11 and `StrEnum`. 

## 0.1.7

- Downgraded mkdocs* dependencies for broader compatibility: not sure
  what principled values to use. 

## 0.1.6

- Added documentation. 
- Came to my senses about checking characters in identifiers.
- Added `__len__()` to `Dataset` as number of `items`. 

## 0.1.5

- Fixed bug in `Dataset.read_items()`. 

## 0.1.4

- Bug fix: checking values in a StrEnum changed with Python 3.12, but
  i want to support 3.11. 
- Don't return values from `Dataset.read_items()`. 

## 0.1.3

- Loosen Python requirements down to 3.10. 

## 0.1.2

- Dropped some data files.

## 0.1.1

- First release, with dataclasses for Dataset and Item. 
