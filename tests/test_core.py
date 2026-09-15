from prompt_master.core import classify, optimize


def test_classify_sql():
    assert classify("make this SQL query faster") == "sql"


def test_optimizer_preserves_request():
    result = optimize("Write a Python function that validates an email")
    assert "Write a Python function" in result.rendered
    assert result.prompt.mode == "coding"
    assert "Do not invent" in result.rendered


def test_empty_request():
    try:
        optimize("   ")
    except ValueError:
        return
    assert False, "Expected ValueError"
