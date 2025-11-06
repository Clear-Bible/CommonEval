"""Tests for commoneval/item.py.

Tests are organized by Item subclass:
- TestBooleanItem: Tests for BooleanItem
- TestTernaryItem: Tests for TernaryItem
- TestClosedSetItem: Tests for ClosedSetItem (CHOICEOF2-5)
- TestOpenEndedItem: Tests for OpenEndedItem
- TestItemFactory: Tests for the Item factory function
"""

from io import StringIO
import pytest

from commoneval.item import (
    BaseItem,
    BooleanItem,
    TernaryItem,
    Ternary,
    ClosedSetItem,
    OpenEndedItem,
    Modality,
)


class TestBaseItem:
    """Test the BaseItem class."""

    def test_cannot_instantiate_directly(self) -> None:
        """Test that BaseItem cannot be instantiated directly."""
        with pytest.raises(TypeError, match="BaseItem cannot be instantiated directly"):
            BaseItem(
                identifier="test.1",
                modality=Modality.BOOLEAN,
                prompt="Is this a test?",
            )


class TestBooleanItem:
    """Test the BooleanItem class."""

    def test_init_true(self) -> None:
        """Test initialization with True response."""
        item = BooleanItem(
            identifier="bool.1",
            modality=Modality.BOOLEAN,
            prompt="Is this a test?",
            response=True,
        )
        assert item.identifier == "bool.1"
        assert item.modality == Modality.BOOLEAN
        assert item.prompt == "Is this a test?"
        assert item.response is True
        assert item.support == ""
        assert item.taskPrompt == ""
        assert item.difficulty == 0.0

    def test_init_false(self) -> None:
        """Test initialization with False response."""
        item = BooleanItem(
            identifier="bool.2",
            modality=Modality.BOOLEAN,
            prompt="Is this false?",
            response=False,
        )
        assert item.response is False

    def test_init_with_optional_fields(self) -> None:
        """Test initialization with optional fields."""
        item = BooleanItem(
            identifier="bool.3",
            modality=Modality.BOOLEAN,
            prompt="Is this a test?",
            response=True,
            support="This is a test item",
            taskPrompt="Answer yes or no",
            difficulty=0.5,
        )
        assert item.support == "This is a test item"
        assert item.taskPrompt == "Answer yes or no"
        assert item.difficulty == 0.5

    def test_bad_response_string(self) -> None:
        """Test that non-boolean response raises error."""
        with pytest.raises(AssertionError, match="not a valid boolean"):
            BooleanItem(
                identifier="bool.bad",
                modality=Modality.BOOLEAN,
                prompt="Is this a test?",
                response="yes",  # type: ignore
            )

    def test_wrong_modality(self) -> None:
        """Test that non-BOOLEAN modality raises error."""
        with pytest.raises(ValueError, match="BooleanItem requires BOOLEAN modality"):
            BooleanItem(
                identifier="bool.bad",
                modality=Modality.TERNARY,
                prompt="Is this a test?",
                response=True,
            )

    def test_repr(self) -> None:
        """Test string representation."""
        item = BooleanItem(
            identifier="bool.1",
            modality=Modality.BOOLEAN,
            prompt="Is this a test?",
            response=True,
        )
        assert repr(item) == "<BooleanItem('bool.1', boolean): 'Is this a test?'->True>"

    def test_asdict(self) -> None:
        """Test conversion to dictionary."""
        item = BooleanItem(
            identifier="bool.1",
            modality=Modality.BOOLEAN,
            prompt="Is this a test?",
            response=True,
        )
        assert item.as_dict() == {
            "identifier": "bool.1",
            "prompt": "Is this a test?",
            "response": True,
            "modality": "boolean",
        }

    def test_write_jsonline(self) -> None:
        """Test writing to JSONL format."""
        item = BooleanItem(
            identifier="bool.1",
            modality=Modality.BOOLEAN,
            prompt="Is this a test?",
            response=True,
        )
        with StringIO() as buf:
            item.write_jsonline(buf)
            contents = buf.getvalue()
            assert contents == (
                '{"identifier": "bool.1", "prompt": "Is this a test?", '
                '"response": true, "modality": "boolean"}\n'
            )


class TestTernaryItem:
    """Test the TernaryItem class."""

    def test_init_true(self) -> None:
        """Test initialization with Ternary.TRUE response."""
        item = TernaryItem(
            identifier="tern.1",
            modality=Modality.TERNARY,
            prompt="Is this true?",
            response=Ternary.TRUE,
        )
        assert item.identifier == "tern.1"
        assert item.modality == Modality.TERNARY
        assert item.response == Ternary.TRUE

    def test_init_false(self) -> None:
        """Test initialization with Ternary.FALSE response."""
        item = TernaryItem(
            identifier="tern.2",
            modality=Modality.TERNARY,
            prompt="Is this false?",
            response=Ternary.FALSE,
        )
        assert item.response == Ternary.FALSE

    def test_init_unknown(self) -> None:
        """Test initialization with Ternary.UNKNOWN response."""
        item = TernaryItem(
            identifier="tern.3",
            modality=Modality.TERNARY,
            prompt="Is this unknown?",
            response=Ternary.UNKNOWN,
        )
        assert item.response == Ternary.UNKNOWN

    def test_init_with_string(self) -> None:
        """Test initialization with string value (should work via Ternary enum)."""
        item = TernaryItem(
            identifier="tern.4",
            modality=Modality.TERNARY,
            prompt="Is this true?",
            response="True",  # type: ignore
        )
        # String should be validated
        assert item.response == "True"

    def test_bad_response(self) -> None:
        """Test that invalid ternary response raises error."""
        with pytest.raises(AssertionError, match="not a valid ternary value"):
            TernaryItem(
                identifier="tern.bad",
                modality=Modality.TERNARY,
                prompt="Is this a test?",
                response="dunno",  # type: ignore
            )

    def test_wrong_modality(self) -> None:
        """Test that non-TERNARY modality raises error."""
        with pytest.raises(ValueError, match="TernaryItem requires TERNARY modality"):
            TernaryItem(
                identifier="tern.bad",
                modality=Modality.BOOLEAN,
                prompt="Is this a test?",
                response=Ternary.TRUE,
            )

    def test_repr(self) -> None:
        """Test string representation."""
        item = TernaryItem(
            identifier="tern.1",
            modality=Modality.TERNARY,
            prompt="Is this a test?",
            response=Ternary.TRUE,
        )
        # Enum repr includes the enum class name
        assert (
            repr(item)
            == "<TernaryItem('tern.1', ternary): 'Is this a test?'-><Ternary.TRUE: 'True'>>"
        )

    def test_asdict(self) -> None:
        """Test conversion to dictionary."""
        item = TernaryItem(
            identifier="tern.1",
            modality=Modality.TERNARY,
            prompt="Is this a test?",
            response=Ternary.UNKNOWN,
        )
        # The response should be serialized as the enum value
        result = item.as_dict()
        assert result["identifier"] == "tern.1"
        assert result["modality"] == "ternary"
        assert result["prompt"] == "Is this a test?"
        # Enum will be serialized as its value
        assert result["response"] in [Ternary.UNKNOWN, "Unknown"]


class TestClosedSetItem:
    """Test the ClosedSetItem class (CHOICEOF2-5)."""

    def test_choiceof2(self) -> None:
        """Test CHOICEOF2 with 2 choices."""
        item = ClosedSetItem(
            identifier="mcq.1",
            modality=Modality.CHOICEOF2,
            prompt="Is this a test?",
            response=0,  # Index into choices
            choices=["Yes", "No"],
        )
        assert item.identifier == "mcq.1"
        assert item.modality == Modality.CHOICEOF2
        assert item.response == 0
        assert item.choices == ["Yes", "No"]

    def test_choiceof3(self) -> None:
        """Test CHOICEOF3 with 3 choices."""
        item = ClosedSetItem(
            identifier="mcq.2",
            modality=Modality.CHOICEOF3,
            prompt="Choose one",
            response=1,
            choices=["Yes", "No", "Maybe"],
        )
        assert item.response == 1
        assert len(item.choices) == 3

    def test_choiceof4(self) -> None:
        """Test CHOICEOF4 with 4 choices."""
        item = ClosedSetItem(
            identifier="mcq.3",
            modality=Modality.CHOICEOF4,
            prompt="What is the capital?",
            response=2,
            choices=["London", "Paris", "Berlin", "Madrid"],
        )
        assert item.response == 2
        assert item.choices[2] == "Berlin"

    def test_choiceof5(self) -> None:
        """Test CHOICEOF5 with 5 choices."""
        item = ClosedSetItem(
            identifier="mcq.4",
            modality=Modality.CHOICEOF5,
            prompt="Rate this",
            response=4,
            choices=["Excellent", "Good", "Fair", "Poor", "Very Poor"],
        )
        assert item.response == 4
        assert len(item.choices) == 5

    def test_response_out_of_range(self) -> None:
        """Test that response index must be within choices range."""
        with pytest.raises(AssertionError, match="out of range"):
            ClosedSetItem(
                identifier="mcq.bad",
                modality=Modality.CHOICEOF2,
                prompt="Choose one",
                response=5,  # Out of range
                choices=["Yes", "No"],
            )

    def test_negative_response(self) -> None:
        """Test that response index must be non-negative."""
        with pytest.raises(AssertionError, match="must be non-negative"):
            ClosedSetItem(
                identifier="mcq.bad",
                modality=Modality.CHOICEOF2,
                prompt="Choose one",
                response=-1,
                choices=["Yes", "No"],
            )

    def test_wrong_number_of_choices(self) -> None:
        """Test that number of choices must match modality."""
        with pytest.raises(AssertionError, match="does not match"):
            ClosedSetItem(
                identifier="mcq.bad",
                modality=Modality.CHOICEOF2,
                prompt="Choose one",
                response=0,
                choices=["Yes", "No", "Maybe"],  # 3 choices for CHOICEOF2
            )

    def test_too_few_choices(self) -> None:
        """Test that there must be at least 2 choices."""
        with pytest.raises(AssertionError, match="at least 2 choices"):
            ClosedSetItem(
                identifier="mcq.bad",
                modality=Modality.CHOICEOF2,
                prompt="Choose one",
                response=0,
                choices=["Only one"],
            )

    def test_repr(self) -> None:
        """Test string representation."""
        item = ClosedSetItem(
            identifier="mcq.1",
            modality=Modality.CHOICEOF2,
            prompt="Is this a test? A) Yes B) No",
            response=0,
            choices=["Yes", "No"],
        )
        # Integer response is repr'd without quotes
        assert repr(item) == "<ClosedSetItem('mcq.1', choiceof2): 'Is this a test? A...'->0>"

    def test_asdict(self) -> None:
        """Test conversion to dictionary includes choices and formats response as letter."""
        item = ClosedSetItem(
            identifier="mcq.1",
            modality=Modality.CHOICEOF4,
            prompt="What is the capital?",
            response=1,  # Index 1 = "Paris" = letter "B"
            choices=["London", "Paris", "Berlin", "Madrid"],
        )
        result = item.as_dict()

        # Response should be converted to letter
        assert result["identifier"] == "mcq.1"
        assert result["modality"] == "choiceof4"
        assert result["prompt"] == "What is the capital?"
        assert result["response"] == "B"  # Letter, not index

        # taskPrompt should be added with choice instructions
        assert "taskPrompt" in result
        assert "Choose one of the following 4 options:" in result["taskPrompt"]
        assert "A) London B) Paris C) Berlin D) Madrid" in result["taskPrompt"]
        assert "A, B, C, or D" in result["taskPrompt"]

    def test_asdict_with_style_parameter(self) -> None:
        """Test that as_dict() accepts style parameter."""
        item = ClosedSetItem(
            identifier="mcq.2",
            modality=Modality.CHOICEOF3,
            prompt="Choose a color",
            response=2,  # Index 2 = "Blue" = letter "C"
            choices=["Red", "Green", "Blue"],
        )
        result = item.as_dict(style="letter")

        assert result["response"] == "C"
        assert "A) Red B) Green C) Blue" in result["taskPrompt"]


class TestOpenEndedItem:
    """Test the OpenEndedItem class."""

    def test_cloze(self) -> None:
        """Test CLOZE modality."""
        item = OpenEndedItem(
            identifier="open.1",
            modality=Modality.CLOZE,
            prompt="The capital of France is ___.",
            response="Paris",
        )
        assert item.identifier == "open.1"
        assert item.modality == Modality.CLOZE
        assert item.response == "Paris"

    def test_cloze_missing_blank(self) -> None:
        """Test that CLOZE without ___ raises error."""
        with pytest.raises(AssertionError, match="missing ___ cloze indicator"):
            OpenEndedItem(
                identifier="open.bad",
                modality=Modality.CLOZE,
                prompt="The capital of France is?",
                response="Paris",
            )

    def test_singlevalue(self) -> None:
        """Test SINGLEVALUE modality."""
        item = OpenEndedItem(
            identifier="open.2",
            modality=Modality.SINGLEVALUE,
            prompt="What is 2+2?",
            response="4",
        )
        assert item.modality == Modality.SINGLEVALUE
        assert item.response == "4"

    def test_shortprose(self) -> None:
        """Test SHORTPROSE modality."""
        item = OpenEndedItem(
            identifier="open.3",
            modality=Modality.SHORTPROSE,
            prompt="Describe a cat in one sentence.",
            response="A cat is a small, furry mammal.",
        )
        assert item.modality == Modality.SHORTPROSE

    def test_longprose(self) -> None:
        """Test LONGPROSE modality."""
        item = OpenEndedItem(
            identifier="open.4",
            modality=Modality.LONGPROSE,
            prompt="Write an essay about cats.",
            response="Cats are fascinating creatures...",
        )
        assert item.modality == Modality.LONGPROSE

    def test_wrong_modality(self) -> None:
        """Test that non-open-ended modality raises error."""
        with pytest.raises(ValueError, match="not an open-ended modality"):
            OpenEndedItem(
                identifier="open.bad",
                modality=Modality.BOOLEAN,
                prompt="Is this a test?",
                response="yes",
            )

    def test_repr(self) -> None:
        """Test string representation."""
        item = OpenEndedItem(
            identifier="open.1",
            modality=Modality.CLOZE,
            prompt="The capital of France is ___.",
            response="Paris",
        )
        assert repr(item) == "<OpenEndedItem('open.1', cloze): 'The capital of Fr...'->'Paris'>"

    def test_asdict(self) -> None:
        """Test conversion to dictionary."""
        item = OpenEndedItem(
            identifier="open.1",
            modality=Modality.SINGLEVALUE,
            prompt="What is 2+2?",
            response="4",
        )
        assert item.as_dict() == {
            "identifier": "open.1",
            "modality": "singlevalue",
            "prompt": "What is 2+2?",
            "response": "4",
        }
