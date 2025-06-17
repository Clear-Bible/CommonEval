"""Test functions in util."""

from math import isclose

from commoneval.util import f1, precision, recall


class TestPrecision:
    """Test precision function."""

    def test_precision(self) -> None:
        """Test precision calculation."""
        assert isclose(precision(10, 5), 0.66666666666)
        assert isclose(precision(0, 0), 0.0)
        assert isclose(precision(5, 10), 0.33333333333)
        assert isclose(precision(10, 0), 1.0)
        assert isclose(precision(1, 3), 0.25)


class TestRecall:
    """Test recall function."""

    def test_recall(self) -> None:
        """Test recall calculation."""
        assert isclose(recall(10, 5), 0.66666666666)
        assert isclose(recall(0, 0), 0.0)
        assert isclose(recall(5, 10), 0.33333333333)
        assert isclose(recall(10, 0), 1.0)
        assert isclose(recall(1, 3), 0.25)


class TestF1:
    """Test F1 function."""

    def test_f1(self) -> None:
        """Test F1 calculation."""
        assert isclose(f1(0.8, 0.6), 0.6857142857142857)
        assert isclose(f1(0.8, 0.0), 0.0)
        assert isclose(f1(0.0, 0.8), 0.0)
