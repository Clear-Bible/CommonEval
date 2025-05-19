# The `Dataset` Class

*Version 3.3, 2025-05-19*

A **benchmark dataset** is a collection of prompts with gold standard
responses (“items”) that can be used for evaluation, along with the
metadata described here.

## Purpose

We define common attributes for benchmark datasets in order to

* Promote consistency and clarity for the broader community
* Help identify areas that are under- or over-represented in the
  evaluation data.

We assume here that datasets are composed around common attribute
values to a large degree, so the same information doesn’t have to be
repeated for each prompt/response item. 

This document does not cover metadata related to the *method of
evaluation* of the responses from a candidate LLM, since those may
vary across different evaluation scenarios.

### Audience

This information is most likely to be relevant to developers who are
creating benchmark datasets, or those developing programs to read
datasets. 

## Format

Metadata for a benchmark dataset is captured as YAML in a file named
`(dataset id).yaml`, located in the directory where the data is
accessed. Attributes in italics are optional: otherwise attributes are
required. Attribute names generally follow [DCMI Metadata
Terms](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#http://purl.org/dc/terms/source). [DCMI:
Using Dublin Core™ \- The
Elements](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/)
provides some practical guidance.

## Standard Attributes

### *`contributor`*

An entity responsible for making contributions to the resource. 

### `created`

A date stamp (YYYY-MM-DD) indicating when this data was initially created. 

### `creator`

An entity responsible for making the resource. Examples of a Creator
include a person, an organization, or a service. Typically the name of
the Creator should be used to indicate the entity.

### *`datePublished`*

Date on which the dataset is made public. 

### `description`

Typically a free-text account of the content of the resource. 

### `hasPart`

A dataset is composed of one or more files with benchmark items in the
current directory. This attribute names those files.

If there is a single file, the file should be named with the dataset
identifier, e.g. `sample.jsonl`. If there are multiple files, they
should be named with a zero-based three-digit index,
e.g. `sample_000.jsonl`, `sample_001.jsonl`, etc.

### `identifier`

An unambiguous reference to the resource within a given
context. Identifiers should be unique across all benchmark datasets,
and should be treated as immutable once published. Identifiers should
be composed of web-friendly characters, and should be matched
case-insensitively.

### *`items`*

A list of `Item` instances for this dataset. A `Dataset` can be
instantiated without any `items`.

### `language`

A language of the resource. Recommended practice is to use an
identifier from ISO 639-3 like `eng`.

### `license`

A legal document giving official permission to do something with the
resource. Recommended practice is an identifier for a [Creative
Commons
License](https://creativecommons.org/share-your-work/cclicenses/) or
another standard identifier.

### *`licenseNotes`*

Additional comments on the license or source of the data. 

### *`metadataVersion`*

The version of this spec that this data conforms to.

### `publisher`

An entity responsible for making the resource available. In this
repository, the `publisher` is likely to always be “Gloo”. Best
practice is not to repeat the name as `publisher` if already listed as
`creator`.

### `source`

A string that identifies a related resource from which the described
resource is derived. This should be the source of the content for the
evaluation items (prompts and gold responses). Preferred values are a
name, a URI, or some other formal identification system.

### *`sourceProcess`*

An optional string that describes the process used to generate the
evaluation items. For example, “Items were generated from the ACAI
person data using the … program”, or “Key terms were dropped from
items in {dataset} to generate cloze prompts”, etc. The intent is just
to provide enough information to distinguish the process: full
documentation is not required.

### `subject`

The topic of the content of the resource. Typically, a `subject` will
be expressed as keywords or key phrases or classification codes that
describe the topic of the resource. Recommended best practice is to
select a value from a controlled vocabulary or formal classification
scheme: we don’t yet have such a vocabulary for the evaluation domain
but we may develop one.

### *`taskPrompt`*

A string that directs a candidate LLM how to carry out a task. For
example, prompts that call for a multiple-choice response might have a
`taskPrompt` like “Choose the best answer from these choices.” The
`taskPrompt` might also provide background presuppositions for the
candidate LLM to incorporate, or personas to adopt (“You are an expert
biblical scholar…”). This would also be a place to add one-shot or
few-shot prompting examples.

The `taskPrompt` may include 

* Overall system characteristics, including factors like safety.
* Task-specific context
* Role prompting 

When specified here, the `taskPrompt` is applied to all items in the
dataset, unless an individual item has its over `taskPrompt` value
(which then takes precedence). To avoid confusion, however, it’s
probably best to either specify this on the dataset or on individual
items, but not both

### *`title`*

The name given to the resource. Typically, a `title` will be a name by
which the resource is formally known.

### *`version`*

The version of the dataset, its items, and all metadata. Recommended
practice is semantic versioning. This value may be more granular and
change more often than \`datePublished\`.


## Other Attributes

Other ad hoc attributes are optionally allowed in the metadata file,
but will not be validated or otherwise processed.

## Attribute Usage

* Preferred practice is to author these attribute names in the case given above, but to match case-insensitively when processing data (so `title`, `Title`, and `TITLE` would all be read the same). 

