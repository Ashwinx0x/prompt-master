from prompt_master.lint import lint


def test_lint_detects_missing_output_instruction():
    issues = lint("Tell me something about databases")
    assert any(issue.code == "PM002" for issue in issues)


def test_lint_detects_secret_like_value():
    issues = lint("Create a report. api_key=sk-1234567890abcdef")
    assert any(issue.code == "PMSEC001" and issue.severity == "error" for issue in issues)


def test_clean_prompt_has_no_security_error():
    issues = lint("Write a concise SQL query. Do not invent schema details.")
    assert not any(issue.severity == "error" for issue in issues)
