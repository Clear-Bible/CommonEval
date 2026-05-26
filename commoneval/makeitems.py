"""Given a list of questions and answers, output JSONL for Items.

This is for bootstrapping benchmarks from existing data.

Example usage:
>>> from commoneval import ROOT, makeitems
>>> questions = ["What does the Bible say is God’s purpose for my life?",
  "Who am I in Christ, and how does that shape my identity?",
  "How do I find meaning in Christ apart from my accomplishments?",]
>>> destpath = ROOT.parent / "eval-Larson/data/eng/larson-commonchristian"
>>> writer = makeitems.QuestionWriter(questions=questions,
  identifier_prefix="lcc", outpath=destpath / f"{destpath.name}.jsonl")

"""

from collections import UserDict
from pathlib import Path
from typing import Optional

import unicodecsv

import item


class QuestionWriter:
    """Write items to a JSONL file.

    This assumes you have questions (prompts) but no answers (responses).
    """

    def __init__(
        self,
        questions: list[str],
        identifier_prefix: str,
        outpath: Path,
        modality: item.Modality = item.Modality.LONGPROSE,
        otherargs: Optional[tuple[str, str]] = (),
    ) -> None:
        """Initialize the writer."""
        self.id_index: int = 0
        with outpath.open("w", encoding="utf-8") as f:
            for question in questions:
                itm = item.OpenEndedItem(
                    identifier=f"{identifier_prefix}{self.id_index:04d}",
                    prompt=question,
                    modality=modality,
                    response="",
                    otherargs=dict(otherargs) if otherargs else {},
                )
                itm.write_jsonline(f)
                self.id_index += 1


class SubjectQuestionWriter:
    """Write items to a JSONL file.

    This assumes you have pairs of questions (prompts) with subjects,
    but no answers (responses).

    """

    def __init__(
        self,
        items: list[str],
        identifier_prefix: str,
        outpath: Path,
        modality: item.Modality = item.Modality.LONGPROSE,
    ) -> None:
        """Initialize the writer."""
        self.id_index: int = 0
        with outpath.open("w", encoding="utf-8") as f:
            for subject, question in items:
                itm = item.OpenEndedItem(
                    identifier=f"{identifier_prefix}{self.id_index:04d}",
                    prompt=question,
                    modality=modality,
                    response="",
                    otherargs={"subject": subject},
                )
                itm.write_jsonline(f)
                self.id_index += 1


class CSVMCQuestionWriter(UserDict):
    """Read multiple questions from CSV and write items to a JSONL file.

    Assumes some standard column headers and 4 answer choices.

    """

    # this will depend on the CSV format
    header_map: dict[str, str] = {
        "A": "0",
        "B": "1",
        "C": "2",
        "D": "3",
        "Correct_Answer": "response",
        "Option_A": "0",
        "Option_B": "1",
        "Option_C": "2",
        "Option_D": "3",
        "Question_Number": "identifier",
        "Question_Text": "prompt",
        "correct_answer": "response",
        "id": "identifier",
        "question": "prompt",
    }

    letter_answers: tuple[str, ...] = ("A", "B", "C", "D")

    def __init__(
        self,
        inpath: Path,
        outpath: Path,
        # these depend on the CSV format
        id_key: str = "id",
        prompt_key: str = "question",
        response_key: str = "correct_answer",
        choices_keys: tuple[str, ...] = ("0", "1", "2", "3"),
        other_fields: tuple[str, ...] = ("rationale", "difficulty"),
        modality: item.Modality = item.Modality.CHOICEOF4,
    ) -> None:
        """Initialize the writer."""
        super().__init__()
        with inpath.open("rb") as f:
            reader = unicodecsv.DictReader(f)
            self.rowitems = [row for row in reader]
        with outpath.open("w", encoding="utf-8") as f:
            for itemdict in self.rowitems:
                assert id_key in itemdict, f"Missing id key: {id_key}"
                assert prompt_key in itemdict, f"Missing prompt key: {prompt_key}"
                assert response_key in itemdict, f"Missing response key: {response_key}"
                response = itemdict.get(response_key)
                try:
                    # if the response is a number, use it directly
                    ans_index = int(response)
                except ValueError:
                    try:
                        # this assumes single letters, with A = first choice
                        # and computes the offset from there
                        assert (
                            response in self.letter_answers
                        ), f"Expected letter answer: {response}"
                        ans_index = ord(itemdict[response_key].lower()) - ord("a")
                    except ValueError:
                        raise ValueError(
                            f"Unable to derive response value from {response}."
                        )
                itemargs = {
                    # identifier
                    self.header_map[id_key]: itemdict[id_key],
                    "modality": modality,
                    # prompt
                    self.header_map[prompt_key]: itemdict[prompt_key],
                    # response
                    self.header_map[response_key]: ans_index,
                    "choices": [itemdict[choice] for choice in choices_keys],
                }
                for field in other_fields:
                    if "otherargs" not in itemargs:
                        itemargs["otherargs"]: dict[str, str] = {}
                    if field in itemdict:
                        itemargs["otherargs"][field] = itemdict[field]
                itm = item.ClosedSetItem(**itemargs)
                self.data[itm.identifier] = itm
                itm.write_jsonline(f)
