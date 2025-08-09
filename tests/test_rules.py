from quality.rules import MaxLineLengthRule, NoTodoCommentsRule


def test_max_line_length_rule_detects_long_lines():
    rule = MaxLineLengthRule(max_length=10)
    code = "short\nthis line is definitely too long\n"
    violations = rule.check("dummy.py", code)
    assert len(violations) == 1
    v = violations[0]
    assert v.line == 2
    assert v.column == 11
    assert v.rule_name == "MaxLineLength"


def test_no_todo_comments_rule_detects_todo_and_fixme():
    rule = NoTodoCommentsRule()
    code = "# TODO: refactor\nprint('ok')\n# fixme: handle error\n"
    violations = rule.check("dummy.py", code)
    messages = [v.message for v in violations]
    assert len(violations) == 2
    assert any("TODO" in m or "tareas" in m for m in messages) 