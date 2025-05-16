"""Tests for src/dataset.py."""

from datetime import date
from pathlib import Path
import pytest

from commoneval.dataset import Dataset


class TestDataset:
    """Test the Dataset class."""

    ds: Dataset = Dataset(
        identifier="testdata",
        created=date.fromisoformat("2023-10-01"),
        creator="Sean",
        description="This is a test",
        hasPart=["testdata.jsonl"],
        source="I made it up",
        subject="test subject",
    )

    def test_init(self) -> None:
        """Test the initialization of the Dataset class."""
        assert self.ds.identifier == "testdata"
        assert self.ds.created == date.fromisoformat("2023-10-01")
        assert self.ds.creator == "Sean"
        assert self.ds.description == "This is a test"
        assert self.ds.hasPart == ["testdata.jsonl"]
        assert self.ds.source == "I made it up"
        assert self.ds.subject == "test subject"
        # default values below here
        assert self.ds.contributor is None
        assert self.ds.datePublished is None
        assert self.ds.language == "eng"
        assert self.ds.license == "CC-BY-NC-SA-4.0"
        assert float(self.ds.metadataVersion) >= 3.2
        assert self.ds.licenseNotes == ""
        assert self.ds.publisher is None
        assert self.ds.sourceProcess == ""
        assert self.ds.taskPrompt == ""
        assert self.ds.title == ""
        assert self.ds.version == "1.0"

    def test_bad_identifier(self) -> None:
        """Test the initialization of the Dataset class with a bad identifier."""
        with pytest.raises(AssertionError):
            Dataset(
                identifier="testdata 1",
                created=date.fromisoformat("2023-10-01"),
                creator="Sean",
                description="This is a test",
                hasPart=["testdata.jsonl"],
                source="I made it up",
                subject="test subject",
            )

    def test_repr(self) -> None:
        """Test the string representation of the Dataset class."""
        assert repr(self.ds) == ("<Dataset('testdata', 'test subject')>")

    def test_asdict(self) -> None:
        """Test the asdict method of the Dataset class."""
        assert self.ds.asdict() == {
            "identifier": "testdata",
            # now a string
            "created": "2023-10-01",
            "creator": "Sean",
            "description": "This is a test",
            "hasPart": ["testdata.jsonl"],
            "source": "I made it up",
            "subject": "test subject",
            # default values below here
            "contributor": None,
            "datePublished": None,
            "language": "eng",
            "license": "CC-BY-NC-SA-4.0",
            "licenseNotes": "",
            "metadataVersion": "3.2",
            "publisher": None,
            "sourceProcess": "",
            "taskPrompt": "",
            "title": "",
            "version": "1.0",
        }

    def test_write_yaml(self, thispath: Path = Path(__file__).parent) -> None:
        """Test the write_yaml method of the Dataset class."""
        with (thispath / "testdata.yaml").open("w") as f:
            self.ds.write_yaml(f)
        # Read the file back in and check that it matches the original data
        with (thispath / "testdata.yaml").open("r") as f:
            thisds = Dataset.read_yaml(f)
        assert thisds == self.ds
