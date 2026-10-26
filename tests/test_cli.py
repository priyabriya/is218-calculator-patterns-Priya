import pytest

from calculator.cli import handle_line, main, parse_number


def run_cli(monkeypatch, capsys, lines):
    """Feed lines to input(); raise EOFError when they run out."""
    feed = iter(lines)

    def fake_input(prompt=""):
        try:
            return next(feed)
        except StopIteration:
            raise EOFError

    monkeypatch.setattr("builtins.input", fake_input)
    main()
    return capsys.readouterr().out


@pytest.mark.parametrize("line,expected", [
    ("add 5 3", "8"), ("subtract 5 3", "2"), ("multiply 5 3", "15"),
    ("divide 6 3", "2"), ("add 1.5 2.25", "3.75"), ("subtract 3 5", "-2"),
    ("multiply -4 2.5", "-10"), ("add -1 -2", "-3"), ("divide 1 4", "0.25"),
    ("ADD 5 3", "8"), ("  add   5   3  ", "8"), ("add 0 0", "0")])
def test_handle_line_success(line, expected):
    assert handle_line(line, []) == expected


@pytest.mark.parametrize("line,fragment", [
    ("power 2 3", "unknown command 'power'"),
    ("hello", "unknown command"),
    ("add", "needs exactly 2 numbers, got 0"),
    ("add 5", "needs exactly 2 numbers, got 1"),
    ("add 1 2 3", "needs exactly 2 numbers, got 3"),
    ("add a 3", "valid numbers"),
    ("add 5 b", "valid numbers"),
    ("add nan 3", "valid numbers"),
    ("add inf 3", "valid numbers"),
    ("divide 6 0", "Cannot divide by zero"),
    ("history now", "takes no operands")])
def test_handle_line_errors(line, fragment):
    output = handle_line(line, [])
    assert output.startswith("Error:")
    assert fragment in output


def test_blank_line_prints_nothing():
    assert handle_line("   ", []) is None


def test_failures_do_not_reach_history():
    history = []
    handle_line("divide 1 0", history)
    handle_line("add x 1", history)
    handle_line("add 1", history)
    assert history == []
    assert handle_line("history", history) == "History is empty"


def test_parse_number():
    assert parse_number("-2.5") == -2.5
    with pytest.raises(ValueError):
        parse_number("abc")
    with pytest.raises(ValueError):
        parse_number("inf")


def test_session_with_history_and_exit(monkeypatch, capsys):
    out = run_cli(monkeypatch, capsys, [
        "add 5 3", "multiply 2 2.5", "history", "exit", "add 9 9"])
    assert "8\n" in out
    assert "add 5 3 = 8\nmultiply 2 2.5 = 5" in out
    assert "Goodbye!" in out
    assert "18" not in out  # nothing runs after exit


def test_session_continues_after_errors(monkeypatch, capsys):
    out = run_cli(monkeypatch, capsys, [
        "bogus", "add 1", "add x y", "divide 1 0", "", "add 2 2",
        "history", "exit"])
    assert out.count("Error:") == 4
    assert "add 2 2 = 4" in out
    assert "divide 1 0 =" not in out  # failed calc never reaches history


def test_empty_history_message(monkeypatch, capsys):
    out = run_cli(monkeypatch, capsys, ["history", "exit"])
    assert "History is empty" in out


def test_eof_ends_cleanly(monkeypatch, capsys):
    out = run_cli(monkeypatch, capsys, ["add 1 1"])
    assert "2\n" in out  # processed the line, then EOF ended the loop


def test_exit_is_case_insensitive(monkeypatch, capsys):
    assert "Goodbye!" in run_cli(monkeypatch, capsys, ["EXIT"])
