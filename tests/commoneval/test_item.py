"""Tests for src/item.py."""

from io import StringIO
import pytest

from commoneval.item import Item, Modality


class TestItem:
    """Test the Item class."""

    i0: Item = Item(
        identifier="testdata.1",
        modality=Modality.BOOLEAN,
        prompt="Is this a test?",
        response=True,
    )

    def test_init(self) -> None:
        """Test the initialization of the Item class."""
        assert self.i0.identifier == "testdata.1"
        assert self.i0.modality == Modality.BOOLEAN
        assert self.i0.prompt == "Is this a test?"
        assert self.i0.response
        # default values below here
        assert self.i0.support == ""
        assert self.i0.taskPrompt == ""

    def test_ternary(self) -> None:
        """Test the initialization of the Item class with a ternary modality."""
        _: Item = Item(
            identifier="testdata.1",
            modality=Modality.TERNARY,
            prompt="Is this a test?",
            response="True",
        )
        _: Item = Item(
            identifier="testdata.1",
            modality=Modality.TERNARY,
            prompt="Is this a test?",
            response="False",
        )
        _: Item = Item(
            identifier="testdata.1",
            modality=Modality.TERNARY,
            prompt="Is this a test?",
            response="Unknown",
        )

    def test_choiceof2(self) -> None:
        """Test the initialization of the Item class with a CHOICEOF2 modality."""
        item: Item = Item(
            identifier="testdata.1",
            modality=Modality.CHOICEOF2,
            prompt="Is this a test? A) Yes, it is. B) No, it isn't.",
            response="A",
        )
        assert (
            repr(item) == "<Item('testdata.1', choiceof2): 'Is this a test? A...'->'A'>"
        )
        assert item.asdict() == {
            "identifier": "testdata.1",
            "modality": "choiceof2",
            "prompt": "Is this a test? A) Yes, it is. B) No, it isn't.",
            "response": "A",
        }

    def test_choiceof3(self) -> None:
        """Test the initialization of the Item class with a CHOICEOF3 modality."""
        item: Item = Item(
            identifier="testdata.1",
            modality=Modality.CHOICEOF3,
            prompt="Is this a test? A) Yes, it is. B) No, it isn't. C) Maybe.",
            response="A",
        )
        assert (
            repr(item) == "<Item('testdata.1', choiceof3): 'Is this a test? A...'->'A'>"
        )
        assert item.asdict() == {
            "identifier": "testdata.1",
            "modality": "choiceof3",
            "prompt": "Is this a test? A) Yes, it is. B) No, it isn't. C) Maybe.",
            "response": "A",
        }

    def test_choiceof4(self) -> None:
        """Test the initialization of the Item class with a CHOICEOF4 modality."""
        item: Item = Item(
            identifier="testdata.1",
            modality=Modality.CHOICEOF4,
            prompt="Is this a test? A) Yes, it is. B) No, it isn't. C) Maybe. D) I don't know.",
            response="A",
        )
        assert (
            repr(item) == "<Item('testdata.1', choiceof4): 'Is this a test? A...'->'A'>"
        )
        assert item.asdict() == {
            "identifier": "testdata.1",
            "modality": "choiceof4",
            "prompt": "Is this a test? A) Yes, it is. B) No, it isn't. C) Maybe. D) I don't know.",
            "response": "A",
        }

    def test_choiceof5(self) -> None:
        """Test the initialization of the Item class with a CHOICEOF5 modality."""
        _: Item = Item(
            identifier="testdata.1",
            modality=Modality.CHOICEOF5,
            prompt="Is this a test? A) Yes, it is. B) No, it isn't. C) Maybe. D) I don't know. E) Absolutely!",
            response="E",
        )

    # def test_bad_identifier(self) -> None:
    #     """Test the initialization of the Item class with a bad identifier."""
    #     with pytest.raises(AssertionError):
    #         Item(
    #             # spaces not allowed in identifier
    #             identifier="testdata 1",
    #             modality=Modality.BOOLEAN,
    #             prompt="Is this a test?",
    #             response=True,
    #         )

    def test_bad_boolean(self) -> None:
        """Test the initialization of the Item class with a bad boolean modality."""
        with pytest.raises(AssertionError):
            Item(
                identifier="testdata.1",
                modality=Modality.BOOLEAN,
                prompt="Is this a test?",
                # response should be True or False
                response="yes",
            )

    def test_bad_choiceof2(self) -> None:
        """Test the initialization of the Item class with a bad choiceof2 modality."""
        with pytest.raises(AssertionError):
            Item(
                identifier="testdata.1",
                modality=Modality.CHOICEOF2,
                prompt="Is this a test?",
                # response should be "A" or "B"
                response="yes",
            )

    def test_bad_ternary(self) -> None:
        """Test the initialization of the Item class with a bad ternary modality."""
        with pytest.raises(AssertionError):
            Item(
                identifier="testdata.1",
                modality=Modality.TERNARY,
                prompt="Is this a test?",
                # response should be "True", "False", or "Unknown"
                response="dunno",
            )

    def test_repr(self) -> None:
        """Test the string representation of the Item class."""
        assert repr(self.i0) == "<Item('testdata.1', boolean): 'Is this a test?'->True>"
        i0: Item = Item(
            identifier="testdata.1",
            modality=Modality.TERNARY,
            prompt="Is this a test?",
            response="True",
        )
        assert repr(i0) == "<Item('testdata.1', ternary): 'Is this a test?'->'True'>"

    def test_asdict(self) -> None:
        """Test the asdict method of the Item class."""
        assert self.i0.asdict() == {
            "identifier": "testdata.1",
            "modality": Modality.BOOLEAN,
            "prompt": "Is this a test?",
            "response": True,
            # omits support and taskPrompt if empty
        }

    def test_write_jsonline(self) -> None:
        """Test the write_jsonline method of the Item class."""
        # write to a string buffer for comparison
        with StringIO() as buf:
            self.i0.write_jsonline(buf)
            contents = buf.getvalue()
            assert contents == (
                '{"identifier": "testdata.1", "modality": "boolean", '
                '"prompt": "Is this a test?", "response": true}\n'
            )
