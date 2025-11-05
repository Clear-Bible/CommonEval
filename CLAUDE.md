# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CommonEval is a Python library for staging LLM evaluation benchmarks focused on Christian faith and human flourishing. It provides structured classes for creating, managing, and serializing evaluation datasets and items. This work is a collaboration between Gloo Open and Biblica's Bible Technology Team.

**Important**: Data in this repository is intended for evaluation only, not for fine-tuning LLMs, to preserve fair measurement of LLM performance.

## Development Commands

### Environment Setup
```bash
# Install dependencies with Poetry
poetry install

# Activate virtual environment
poetry shell
```

### Testing
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=commoneval

# Run a single test file
pytest tests/commoneval/test_item.py

# Run a specific test
pytest tests/commoneval/test_item.py::TestItem::test_init
```

### Documentation
```bash
# Build documentation (uses mkdocs)
mkdocs build

# Serve documentation locally
mkdocs serve
```

## Architecture

### Core Data Model

The library uses a two-level hierarchy:

1. **Dataset** (`commoneval/dataset.py`): A collection of evaluation items with metadata
   - Stored as YAML metadata files (e.g., `data/eng/bible_qa-death-bool.yaml`)
   - References one or more JSONL files containing items via the `hasPart` field
   - Supports reading/writing items and metadata separately for efficiency

2. **Item** (`commoneval/item.py`): A single prompt-response pair with metadata
   - Each item has an identifier, modality, prompt, response, and optional support/taskPrompt
   - Items are serialized to JSONL format (one JSON object per line)
   - Items use dataclass validation to ensure consistency

### Modality System

Items support different response types via the `Modality` enum:
- **Closed-set**: `BOOLEAN`, `CHOICEOF2`/`3`/`4`/`5`, `TERNARY` (True/False/Unknown)
- **Open-ended**: `CLOZE`, `SINGLEVALUE`, `SHORTPROSE`, `LONGPROSE`

For choice-based modalities (`CHOICEOF*`), the valid choices are stored in private attributes like `_choiceof4values` and must match the response value.

### Data Organization

```
data/
  eng/                          # Language-specific directory (ISO 639-3 code)
    bible_qa-death-bool/        # Dataset directory (matches identifier)
      bible_qa-death-bool.yaml  # Dataset metadata
      bible_qa-death-bool.jsonl # Items (single file)
    another-dataset/
      another-dataset.yaml
      another-dataset_000.jsonl # Multiple files use _NNN suffix
      another-dataset_001.jsonl
```

### Path Constants

Key paths are defined in `commoneval/__init__.py`:
- `ROOT`: Project root directory
- `DATAPATH`: `data/` directory
- `DATAENGPATH`: `data/eng/` for English datasets
- `SRCPATH`: `src/` directory (note: may not exist in current structure)

### Item Creation Utilities

`commoneval/makeitems.py` provides helper classes for bootstrapping datasets:
- `QuestionWriter`: Create items from a list of prompts (no responses yet)
- `SubjectQuestionWriter`: Create items with prompts and subject metadata
- `CSVMCQuestionWriter`: Import multiple-choice questions from CSV files

These are intended for initial dataset creation, not runtime use.

### Validation and Constraints

Both Dataset and Item classes use `__post_init__` validation:
- **Identifiers** must match `[-a-zA-Z0-9_.]+` (no spaces or special chars)
- **Created dates** must be in the past
- **File naming** must follow conventions: `{identifier}.jsonl` for single files, `{identifier}_NNN.jsonl` for multiple
- **Response values** must match the modality type (e.g., boolean responses must be True/False)
- **Difficulty** must be between 0.0 and 1.0

### Serialization Patterns

- **Dataset metadata**: YAML format via `write_yaml()`/`read_yaml()`
- **Items**: JSONL format via `write_jsonline()` (no direct read method on Item)
- **Dataset items**: Use `dataset.read_items()` to load items from JSONL into a Dataset instance
- Items are stored in the `items` list attribute, populated by `read_items()`

### Metadata Version

The current metadata specification version is 3.2 (see `metadataVersion` field). This ensures datasets and items conform to expected schema standards.

## Python Version Compatibility

The codebase supports Python 3.10+ but includes compatibility shims:
- `StrEnum` fallback for Python < 3.11 (see `commoneval/item.py:16-23`)
- `is_valid_enum_value()` helper function handles enum checking differences between Python 3.11 and 3.12+
