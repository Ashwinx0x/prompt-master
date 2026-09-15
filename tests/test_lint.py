from prompt_master.lint import lint


def codes(text):
    return {issue.code for issue in lint(text)}


def test_lint_detects_missing_output_instruction():
    assert "PM002" in codes("Tell me something about databases")


def test_lint_detects_secret_like_value():
    issues = lint("Create a report. api_key=sk-1234567890abcdef")
    assert any(issue.code == "PMSEC001" and issue.severity == "error" for issue in issues)


def test_clean_prompt_has_no_security_error():
    issues = lint("Write a concise SQL query. Do not invent schema details.")
    assert not any(issue.severity == "error" for issue in issues)


def test_lint_detects_duplicate_instruction():
    text = "Output a concise answer.\nOutput a concise answer.\nDo not invent facts."
    assert "PM005" in codes(text)


def test_lint_detects_conflicting_length():
    text = "Write the answer. Be detailed but keep it to one sentence. Do not invent facts."
    assert "PM006" in codes(text)
