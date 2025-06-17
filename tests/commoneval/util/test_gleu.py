from commoneval.util import gleu


class TestGleu:
    """Test the GLEU score calculation."""

    def test_gleu_bigrams(self) -> None:
        """Test GLEU score calculation."""
        ref = tuple(["the", "cat", "sat", "on", "the", "mat"])
        hyp = tuple(["the", "cat", "sat", "on", "the", "rug"])
        gleudict = gleu(ref, hyp)
        assert gleudict["false_negative"] == 1
        assert gleudict["false_positive"] == 1
        assert gleudict["true_positive"] == 4

    def test_gleu_bigrams_empty_hyp(self) -> None:
        """Test GLEU score calculation."""
        ref = tuple(["the", "cat", "sat", "on", "the", "mat"])
        hyp = tuple([])
        gleudict = gleu(ref, hyp)
        assert gleudict["false_negative"] == 5
        assert gleudict["false_positive"] == 0
        assert gleudict["true_positive"] == 0

    def test_gleu_bigrams_empty_ref(self) -> None:
        """Test GLEU score calculation."""
        ref = tuple([])
        hyp = tuple(["the", "cat", "sat", "on", "the", "mat"])
        gleudict = gleu(ref, hyp)
        assert gleudict["false_negative"] == 0
        assert gleudict["false_positive"] == 5
        assert gleudict["true_positive"] == 0
