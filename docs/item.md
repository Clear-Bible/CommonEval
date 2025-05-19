# The `Item` Class

*Version 3.3, 2025-05-19*

A **benchmark dataset item** represents an individual prompt/response
pair that will be sent to one or more LLMs to gauge their
performance. A benchmark dataset is composed of many instances of
items.

We assume that all the items in a dataset have a common set of
attributes that describe them. Individual LLM APIs are expected to
have their own requirements for formatting and attributes: the
attributes described here will therefore need to be mapped or
transformed to meet those requirements.

## Purpose

* Standardize item-level data for LLM benchmark interoperability.
* Enable performance tracking across content types and over time.
* Identify under- or over-represented subject areas.

### Audience

This information is most likely to be relevant to developers who are
creating benchmark datasets, or those developing programs to read
datasets. 

## Item Attributes

Attribute names in *italics* are optional: otherwise attributes are
required. 

### *`difficulty`*

A floating point number between 0.0 and 1.0 that represents the
difficulty of responding correctly to the prompt. Determining this
value is typically subjective, but you should attempt to use the same
approach within a dataset so that items can be compared with each
other. Comparison *across* datasets may not be feasible.

### `identifier`

An unambiguous reference to the resource within a given
context. Identifiers should be unique across all items with a dataset,
and should be treated as immutable once published. Identifiers should
be composed of web-friendly characters, and should be matched
case-insensitively.

A simple schema would be “\<subject slug\>.\<index\>”.

### `modality`

An identifier for the type of response that is expected, and that
matches the reference response. Ideally one of a closed set of values,
like `boolean`, `multiple-choice`, etc. See [Appendix: Modality
Identifiers](#appendix:-modality-identifiers) for proposed values.

The modality of the expected response will often need to be reflected in the `taskPrompt`. 

### `prompt`

The question or task being posed to the LLM. 

For a `multiple-choice` modality, the prompt must identify the
different choices with letters or numbers for use in the response.

### `response`

The expected “gold standard” response. For a `multiple-choice`
modality, this will just be the identifier of the correct answer.

We may want to support multiple responses with multiple levels of
correctness, e.g. A = correct, B = partially correct, but other
answers are incorrect.

### *`support`*

A link, data item (like a Bible reference), or brief string that
justifies or provides support for the reference answer.

For Bible facts, relevant support might be a selective list of Bible
references. 

### *`taskPrompt`*

A string that directs a candidate LLM how to carry out a task. For
example, prompts that call for a multiple-choice response might have a
`taskPrompt` like “Choose the best answer from these choices.” The
`taskPrompt` might also provide contextual instructions, background
presuppositions for the candidate LLM to incorporate, or personas to
adopt (“You are an expert biblical scholar…”).

If also specified on the dataset, `taskPrompt` values for individual
items take precedence. To avoid confusion, however, it’s probably best
to either specify this on the dataset or on individual items, but not
both.


## Appendix: Modality Identifiers {#appendix:-modality-identifiers}

### Closed-set Responses

### `boolean`

The response should be either “True” or “False”. 

### `choiceof2`

The response should be one of “A” or “B”. The prompt must define the
corresponding choices and indicate that only a letter should be
returned.

### `choiceof3`

The response should be one of “A”, “B”, or “C”. The prompt must define
the corresponding choices and indicate that only a letter should be
returned.

### `choiceof4`

The response should be one of “A”, “B”, “C”, or “D”. The prompt must
define the corresponding choices and indicate that only a letter
should be returned.

### `choiceof5`

The response should be one of “A”, “B”, “C”, “D”, or “E”. The prompt
must define the corresponding choices and indicate that only a letter
should be returned.

### `ternary`

The response should be “True”, “False”, or “I don’t know”. 

### Open-set Responses

### `cloze`

The response fills in a missing item in the prompt, but the value is not restricted. Example: “Three primary Christian virtues are \_\_\_, hope, and love.”

The “blank” is indicated with three underscore characters. The prompt or task prompt may need to specify that the answer should only provides the minimum words to fill in the blank: otherwise some LLMs will add other comments that will make the responses harder to judge. 

### `single-value`

The response provides a single word as response. The general
expectation is that the word can be tested for equality to one or a
small number of provided values (so using another LLM for evaluation
isn't required). 

### `short-prose`

The response provides only a few words as a response. In such cases
another LLM may then be neede to evaluate the correctness of the
response ("LLM as Judge").

### `long-prose`

The response is loger than a few words. Typically another LLM will
then be used to evaluate the correctness of the response ("LLM as
Judge").

