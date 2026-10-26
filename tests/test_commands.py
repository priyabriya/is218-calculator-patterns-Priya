import pytest

from calculator.calculation import ArithmeticCalculation, Calculation
from calculator.commands import CalculateCommand, HistoryCommand, format_number
from calculator.operations import Operations


def make(a, b, op):
    return ArithmeticCalculation.create(a, b, op)


def test_calculate_returns_answer_and_records_history():
    history = []
    result = CalculateCommand(make(5, 3, Operations.add), history).execute()
    assert result == 8
    assert history == ["add 5 3 = 8"]


def test_explicit_label_is_used():
    history = []
    CalculateCommand(make(6, 3, Operations.divide), history, "div").execute()
    assert history == ["div 6 3 = 2"]


def test_history_keeps_order_and_decimals():
    history = []
    CalculateCommand(make(1.5, 2, Operations.multiply), history).execute()
    CalculateCommand(make(-5, 3, Operations.subtract), history).execute()
    assert history == ["multiply 1.5 2 = 3", "subtract -5 3 = -8"]


def test_failed_calculation_is_not_recorded():
    history = []
    with pytest.raises(ValueError):
        CalculateCommand(make(1, 0, Operations.divide), history).execute()
    assert history == []


def test_command_accepts_any_calculation_with_execute():
    class Constant(Calculation):
        def execute(self):
            return 42.0

    history = []
    result = CalculateCommand(Constant(1, 2, lambda a, b: 0), history).execute()
    assert result == 42.0
    assert history == ["<lambda> 1 2 = 42"]


def test_history_command_empty():
    assert HistoryCommand([]).execute() == []


def test_history_command_returns_copy():
    history = ["add 1 1 = 2"]
    returned = HistoryCommand(history).execute()
    assert returned == history
    returned.append("fake")
    returned.clear()
    assert history == ["add 1 1 = 2"]


@pytest.mark.parametrize("value,text", [
    (8.0, "8"), (-2.0, "-2"), (2.5, "2.5"), (0.0, "0"),
    (1e20, "1e+20"), (float("inf"), "inf")])
def test_format_number(value, text):
    assert format_number(value) == text
