# Release Notes

## UNRELEASED

### 0.2.0 (Breaking Changes)

**Major Refactoring: Item Class Hierarchy**

The `Item` class has been refactored into a proper class hierarchy with type-safe response fields. This is a **breaking change** for code that directly instantiates `Item` objects.

**New Class Structure:**
- `BaseItem`: Abstract base class (cannot be instantiated directly)
- `BooleanItem`: For true/false questions (`response: bool`)
- `TernaryItem`: For true/false/unknown questions (`response: Ternary`)
- `ClosedSetItem`: For multiple-choice questions (`response: int` as index)
- `OpenEndedItem`: For open-ended text responses (`response: str`)

**ClosedSetItem API Changes:**
- Response is now an integer index (0-based) into the `choices` list
- Uses `choices: list[str]` instead of `_choiceofNvalues: set[str]`
- `asdict()` now converts response to letter (A/B/C/D/E) and adds formatted `taskPrompt`
- Added `_choicetext()` method to format choices for display
- Added optional `style` parameter to `asdict()` (currently only supports "letter")

**Documentation:**
- Added comprehensive module docstring with examples for each Item type
- Created `CLAUDE.md` for Claude Code AI assistant guidance
- Added examples showing instantiation, serialization, and usage patterns

**Tests:**
- Completely refactored test suite from 12 to 47 tests
- Separate test classes for each Item subclass:
  - `TestBaseItem`: Tests that BaseItem cannot be instantiated directly
  - `TestBooleanItem`: 8 tests for boolean items
  - `TestTernaryItem`: 8 tests for ternary items
  - `TestClosedSetItem`: 11 tests for multiple-choice items
  - `TestOpenEndedItem`: 8 tests for open-ended items
  - `TestItemFactory`: 9 tests for backward compatibility
- All 58 tests pass (47 item + 5 dataset + 6 utility)

**Type Safety Improvements:**
- Each subclass has properly typed response field
- BaseItem checks prevent direct instantiation
- All dataclasses use `kw_only=True` for proper field ordering
- Subclasses validate modality matches expected type

**Other Changes:**
- Fixed typo in `BaseItem._choicetext()` method signature
- Updated imports in `dataset.py` to include `BaseItem`
- Enhanced `__repr__()` to handle different response types gracefully

## 0.1.12

- Minor updates to item.py: warn, not error, for empty response;
  `asdict()` now outputs `_otherargs`. 
- Added makeitems.py for easier generation of benchmark files


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
