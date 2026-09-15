import pytest

from prompt_master import MODES, classify, optimize


def test_classify_sql():
    assert classify("make this SQL query faster") == "sql"


def test_classify_image():
    assert classify("create a photorealistic portrait") == "image"


def test_optimizer_preserves_request():
    result = optimize("Write a Python function that validates an email")
    assert "Write a Python function" in result.rendered
    assert result.prompt.mode == "coding"
    assert "Do not invent" in result.rendered


def test_explicit_mode_overrides_auto():
    result = optimize("Explain this SQL query", mode="writing")
    assert result.prompt.mode == "writing"


def test_unknown_mode():
    with pytest.raises(ValueError):
        optimize("hello", mode="unknown")


def test_empty_request():
    with pytest.raises(ValueError):
        optimize("   ")


def test_all_modes_are_valid():
    assert "auto" in MODES
    assert "coding" in MODES
    assert "agent" in MODES
