from prompt_master import compress


def test_compression_removes_duplicate_lines():
    result = compress("Give a concise answer.\nGive a concise answer.\nDo not invent facts.")
    assert result.compressed.count("Give a concise answer.") == 1
    assert result.compressed_words < result.original_words
    assert result.reduction_percent > 0


def test_compression_preserves_empty_input():
    result = compress("   ")
    assert result.compressed == ""
    assert result.reduction_percent == 0.0
