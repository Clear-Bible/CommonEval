# Repository Philosophy and Structure

Our intention is to collect and share a large number of benchmarks
through this repository. To this end, we use standard structures and
metadata standards to provide consistency and reduce friction. 

Several aspects of the data needed for a complete evaluation process
are not included here by design:

- Data may need some transformation for individual evaluation
  frameworks (like [promptfoo](https://www.promptfoo.dev/)). While
  some methods are provided for those transformations, we have opted
  not to standardize on these specific formats, to ensure the data is
  both as general as possible and well-described. 
- Likewise, the particular scoring approach used for evaluation (LLM as judge,
  human review, etc.) or scoring metrics are not included in the
  attributes of datasets. 

## Code

The `commoneval` directory contains Python code that defines the
metadata formats. These are documented on their own pages:

* [the `Dataset` Class](dataset.md) defines metadata for a dataset as
  a while.
* [the `Item` Class](item.md) defines metadata for individual
  evaluation items.
* [the `util` package](util.md) provides other helpful utility code. 

### Installing

You can install this code as a Python library with `pip install
commoneval` (or the usual variants with `poetry` or `uv`). 

## Data

The `data` directory contains multiple benchmark datasets, organized
first by language (e.g., English datasets are under `eng`), then by
dataset identifier. Each dataset directory includes several files:

* Dataset metadata is in `(dataset id).yaml` ([YAML](https://yaml.org/) format)
* Dataset items are in `(dataset id).jsonl` ([JSON
  Lines](https://jsonlines.org/) format), or multiple such files. 

We have chosen to include many smaller benchmarks rather than bundling
items together, to allow for more fine-grained evaluation. 

## Release History

Deveopers who are interested in a history of releases should see
[Release Notes](ReleaseNotes.md). 
