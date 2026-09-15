from prompt_master import compare, evaluate


def test_evaluation_rewards_explicit_structure():
    result = evaluate(
        """# Objective\nCreate a concise SQL query.\n\n## Constraints\n- Do not invent schema details.\n- Must preserve the requested result.\n\n## Output\nReturn only the optimized query and a brief explanation."""
    )
    assert result.score >= 70
    assert result.dimensions["output"] == 20
    assert not any("explicit output" in issue.lower() for issue in result.issues)


def test_evaluation_flags_underspecified_prompt():
    result = evaluate("Tell me about SQL")
    assert result.score < 70
    assert result.issues


def test_compare_prefers_better_structured_prompt():
    comparison = compare(
        "Tell me about SQL",
        "## Objective\nExplain SQL joins.\n## Constraints\nBe concise and accurate.\n## Output\nProvide examples.",
    )
    assert comparison.winner == "B"
    assert comparison.score_b > comparison.score_a
    assert comparison.margin > 0
