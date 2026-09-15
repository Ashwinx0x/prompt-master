from prompt_master import classify_detailed


def test_classification_exposes_signals_and_confidence():
    result = classify_detailed("Optimize this BigQuery SQL query for performance")
    assert result.mode == "sql"
    assert result.confidence > 0.5
    assert "bigquery" in result.matched_signals


def test_unknown_request_stays_auto():
    result = classify_detailed("hello there")
    assert result.mode == "auto"
    assert result.confidence == 0.0
